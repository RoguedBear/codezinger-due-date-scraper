import datetime
from hashlib import md5


class QuestionData:
    mapping = dict()

    def __init__(self, question: str, class_name: str, q_type: str, due_date: datetime.datetime):
        self.question = question
        self.class_name = class_name
        self.q_type = q_type
        self.due_date = due_date
        self.__message_id = ""

    @property
    def short_name(self):
        if self.class_name in self.mapping:
            return self.mapping.get(self.class_name)
        else:
            return self.class_name

    def __repr__(self) -> str:
        if_exam = ""
        if self.q_type == "E":
            if_exam = "⚠⚠ EXAM: "
        if self.due_date != datetime.datetime.min:
            due = f"<t:{self.due_date.timestamp():.0f}:R>"
        else:
            due = "NEVAAAH <:nevah:785810983418593295>"
        return if_exam + f"{self.short_name} - {self.question} - due {due}"

    @classmethod
    def update_mapping_from_config(cls, config: dict):
        QuestionData.mapping = config.get("mapping", dict())

    @staticmethod
    def _calculate_md5(input_: str):
        return md5(input_.encode('utf-8')).hexdigest()

    @property
    def primary_hash(self) -> str:
        return self._calculate_md5(self.class_name + self.question + self.q_type + self.due_date.isoformat())

    @property
    def secondary_hash(self) -> str:
        return self._calculate_md5(self.class_name + self.question)

    @property
    def message_id(self) -> str:
        return self.__message_id

    @message_id.setter
    def message_id(self, value: str):
        if len(value) == 18:
            self.__message_id = value
        else:
            raise ValueError("message id aka snowflake is of length 18!")
