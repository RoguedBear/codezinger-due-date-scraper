import datetime
import json
from typing import List

from classes.Database import Database
from classes.QuestionData import QuestionData


def process_data(data: List[dict], database: Database):
    new_questions: List[QuestionData] = []
    updated_questions: List[QuestionData] = []

    for question in data:
        question["class_name"] = question["class"]
        question["q_type"] = question["question_type"]
        del question["class"], question["question_type"]
        question = QuestionData(**question)
        print(question, question.primary_hash)


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
