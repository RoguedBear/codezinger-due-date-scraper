import datetime
import json
from sys import stderr
from typing import List

from classes.Database import Database, EventAlreadyLockedException
from classes.QuestionData import QuestionData
from classes.Webhook import Webhook


def process_data(data: List[dict], database: Database, webhook: Webhook):
    new_questions: List[QuestionData] = []
    updated_questions: List[QuestionData] = []

    for question in data:
        question["class_name"] = question["class"]
        question["q_type"] = question["question_type"]
        del question["class"], question["question_type"]
        question = QuestionData(**question)

        # check if current event exists in database
        if question.primary_hash in database:
            continue
        # check if secondary hash exists in db
        elif question.secondary_hash in database:
            # if yes, then the event was updated
            updated_questions.append(question)
        else:
            # otherwise, this is a new event
            new_questions.append(question)

    process_updated_questions(updated_questions, database, webhook)
    process_new_questions(new_questions, database, webhook)


def process_updated_questions(events: List[QuestionData], database: Database, webhook: Webhook):
    if not events:
        return
    print("Processing updated events...")
    __processed = 0
    for event in events:
        old_q = database.get_via_secondary_hash(event.secondary_hash)
        diff = old_q.diff(event)

        # delete old message
        webhook.delete_message(old_q)
        # if this fails, skip and move to next
        try:
            # first lock this event
            database.lock(event)
            # Sanity check if another instance didn't do stuff
            assert old_q.primary_hash in database, "old question has been purged probably by another instance."
            event.message_id = webhook.send_message(event,
                                                    '`' + "—" * 30 + "`\nUPDATED: " + diff + "\n",
                                                    '\n`' + "—" * 30 + '`')
        except ValueError:
            print("no message id received, skipping over: ", event, file=stderr)
        except AssertionError as e:
            print(e, file=stderr)
        except EventAlreadyLockedException:
            print("Another instance already locked", event.question)
        else:
            # now delete old entry and add new entry
            database.remove(old_q)
            database.insert(event)
            __processed += 1
        finally:
            database.unlock(event)
    print("Processed", __processed, "updated events")


def process_new_questions(events: List[QuestionData], database: Database, webhook: Webhook):
    if not events:
        return
    print("Processing new events...")
    events.sort(key=lambda x: x.due_date)
    __sent = 0
    dashes = "" #"`" + "-" * 30 + "`"
    for event in events:
        # skip practise problems
        if event.q_type == "P":
            continue
        try:
            # Lock the current event first
            database.lock(event)
            # sanity check if another instance didn't send the message already
            assert event.primary_hash not in database, "Another instance already sent this event's webhook"
            event.message_id = webhook.send_message(event, dashes + "\n", "\n" + dashes)
        except ValueError:
            print("no message id recieved, skipping over: ", event, file=stderr)
        except AssertionError as e:
            print(e, file=stderr)
        except EventAlreadyLockedException:
            print("Another instance already locked", event.question)
        else:
            database.insert(event)
            __sent += 1
        finally:
            database.unlock(event)
    print("Sent", __sent, "new webhook messages")


def purge_old_questions(database: Database, webhook: Webhook):
    old_secondary_hashes = []
    purged = 0
    with database as cursor:
        query = "SELECT secondary_hash FROM question_data WHERE due_date < ?"
        for output in cursor.execute(query, (datetime.datetime.now(),)):
            old_secondary_hashes.append(output[0])

    for hash_ in old_secondary_hashes:
        old_event = database.get_via_secondary_hash(hash_)
        deleted = webhook.delete_message(old_event)
        if deleted:
            database.remove(old_event)
            purged += 1
    if purged > 0:
        print("Purged", purged, "expired events")


if __name__ == '__main__':
    import os, yaml
    from dotenv import load_dotenv

    load_dotenv()


    def date_hook(json_dict):
        for (key, value) in json_dict.items():
            if json_dict[key] == "0001-01-01 00:00:00":
                json_dict[key] = datetime.datetime.min
            else:
                try:
                    json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
        return json_dict


    with open("test_data.json") as file:
        data = json.load(file, object_hook=date_hook)
    # print(data)
    db = Database(folder="db/")
    webhook = Webhook(os.getenv("WEBHOOK_URL"),
                      avatar=os.getenv("AVATAR_URL"),
                      username="bone")
    process_data(data, db, webhook)

    purge_old_questions(db, webhook)

    # input("> press to delete all webhooks")
    # with db as cursor:
    #     for msg_id in cursor.execute("SELECT message_id FROM message_ids"):
    #         webhook.delete_message(str(msg_id))
