import json


class Message:

    def __init__(self, user_name: str, text: str):
        self.user_name = user_name
        self.text = text

    def to_json(self):
        return json.dumps(self.__dict__)