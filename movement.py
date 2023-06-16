import json


class Movement:

    def __init__(self, left: bool, right: bool, up: bool, down: bool, x_coordinate: int, y_coordinate: int):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        movement = json.loads(json_str)
        return cls(movement['left'], movement['right'], movement['up'], movement['down'], movement['x_coordinate'], movement['y_coordinate'])
