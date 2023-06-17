import pickle


class Player:
    def __init__(self, x_coordinate: int, y_coordinate: int, progress: int, tarteeb: int, ip_address=None):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        self.progress = progress
        self.tarteeb = tarteeb

        self.IpAddress = ip_address

    def to_pickle(self):
        return pickle.dumps(self.__dict__)

    @classmethod
    def from_pickle(cls, pickle_str):
        player = pickle.loads(pickle_str)
        return cls(player['x_coordinate'], player['y_coordinate'], player['progress'], player['tarteeb'], player['IpAddress'])

    def player_tuple(self) -> tuple:
        return self.x_coordinate, self.y_coordinate, self.progress, self.tarteeb
