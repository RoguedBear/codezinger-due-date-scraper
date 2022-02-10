from time import sleep
from typing import Union

import requests.exceptions
from requests import Session

from classes.QuestionData import QuestionData


class Webhook:
    def __init__(self, url: str, avatar="", username=""):
        self.url = url
        self.session = Session()
        self.avatar = avatar
        self.username = username

    def __send(self, method: str, *args, **kwargs):
        methods = {"post": self.session.post, "delete": self.session.delete, "patch": self.session.patch}
        retries = 5
        while retries > 0:
            try:
                return methods[method](*args, **kwargs)
            except requests.exceptions.ConnectTimeout:
                print("Connection timeout, retrying in 10s...")
                sleep(10)
                retries -= 1
            except requests.exceptions.ConnectionError:
                print("Connection error, retrying in 5 minutes...")
                sleep(5 * 60)
                retries -= 1
        return None

    def send_message(self, question: Union[str, QuestionData]) -> str:
        """
        Sends the message passed or the string repr of QuestionData and returns the message id
        :param question:
        :return: message id
        """
        message = {
            "username": self.username,
            "avatar_url": self.avatar,
            "content": str(question)
        }
        res = self.__send("post", self.url, json=message, params={"wait": True})
        if res is None:
            return ""
        return res.json()["id"]

    def delete_message(self, question: Union[str, QuestionData]) -> bool:
        """
        Deletes the message id
        :param question:
        :return: True if deleted, False otherwise
        """
        if isinstance(question, str):
            message_id = question
        else:
            message_id = question.message_id

        res: requests.Response = self.__send("delete", self.url + "/messages/" + message_id)
        if res is None:
            return False
        else:
            return res.status_code == 204


if __name__ == '__main__':
    import os
    from datetime import datetime
    from dotenv import load_dotenv

    from classes.QuestionData import QuestionData

    load_dotenv("../.env")

    webhook = Webhook(os.getenv("WEBHOOK_URL"),
                      avatar=os.getenv("AVATAR_URL"),
                      username="bone")

    x = webhook.send_message("test2")
    print(type(x), x)
    print(webhook.delete_message(x))

    q = QuestionData("question", "os", "A", datetime(year=2022, month=2, day=10))
    q.message_id = webhook.send_message(q)
    sleep(5)
    webhook.delete_message(q)
