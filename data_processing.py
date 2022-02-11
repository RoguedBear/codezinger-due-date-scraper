import datetime
import json
from sys import stderr
from typing import List

from classes.Database import Database
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
    process_new_questions(new_questions)


def process_updated_questions(events: List[QuestionData], database: Database, webhook: Webhook):
    if not events:
        return
    

def process_new_questions(events: List[QuestionData]):
    if not events:
        return
    pass


if __name__ == '__main__':
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
    process_data(data, db)
