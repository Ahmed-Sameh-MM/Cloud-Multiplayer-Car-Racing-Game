import json


class Player:
    def __init__(self, user_name: str, ip_address: str, progress: int, coordinates: dict, car_image: str, position: int):
        self.user_name = user_name
        self.ip_address = ip_address
        self.progress = progress
        self.coordinates = coordinates
        self.car_image = car_image
        self.position = position

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        player = json.loads(json_str)
        return cls(player['user_name'], player['ip_address'], player['progress'], player['coordinates'], player['car_image'], player['position'])

    def player_tuple(self) -> tuple:
        return self.user_name, self.ip_address, self.progress, self.coordinates_to_json(), self.car_image, self.position

    def coordinates_to_json(self):
        return json.dumps(self.coordinates)

    @classmethod
    def coordinates_from_json(cls, coordinates_json_str):
        coordinates_dict = json.loads(coordinates_json_str)
        return coordinates_dict['coordinates'] 
