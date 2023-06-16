import json


class Player:
    def __init__(self, x_coordinate: int, y_coordinate: int, progress: int, tarteeb: int):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.progress = progress
        self.tarteeb = tarteeb
        self.id = None

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        player = json.loads(json_str)
        return cls(player['X_Coordinate'], player['Y_Coordinate'], player['Progress'], player['Tarteeb'])

    def player_tuple(self) -> tuple:
        return self.x_coordinate, self.y_coordinate, self.progress, self.tarteeb
