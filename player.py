import json


class Player:
    def __init__(self, user_name: str, ip_address: str, progress: int, position: int):
        self.user_name = user_name
        self.ip_address = ip_address
        self.progress = progress
        self.position = position

    def player_tuple(self) -> tuple:
        return self.user_name, self.ip_address, self.progress, self.position

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        player = json.loads(json_str)
        return cls(player['user_name'], player['ip_address'], player['progress'], player['position'])
