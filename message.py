import json


class Message:

    def __init__(self, user_name: str, text: str):
        self.user_name = user_name
        self.text = text

    def format_message(self):
        return self.user_name + ': ' + self.text

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        message = json.loads(json_str)
        return cls(message['user_name'], message['text'])
