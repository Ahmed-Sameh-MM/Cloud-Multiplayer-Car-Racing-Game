import pickle


class Player:
    def __init__(self, x_coordinate: int, y_coordinate: int, progress: int, tarteeb: int, car_image: str, ip_address=None):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        self.progress = progress
        self.tarteeb = tarteeb

        self.CarImage = car_image

        self.IpAddress = ip_address

    def to_pickle(self):
        return pickle.dumps(self.__dict__)

    @classmethod
    def from_pickle(cls, pickle_str):
        player = pickle.loads(pickle_str)
        return cls(player['x_coordinate'], player['y_coordinate'], player['progress'], player['tarteeb'], player['CarImage'], player['IpAddress'])

    def player_tuple(self) -> tuple:
        return self.IpAddress, self.x_coordinate, self.y_coordinate, self.progress, self.CarImage

    def player_update_tuple(self) -> tuple:
        return self.x_coordinate, self.y_coordinate, self.progress, self.IpAddress

    @classmethod
    def from_sql(cls, sql_tuple):
        return cls(sql_tuple[1], sql_tuple[2], sql_tuple[3], 0, sql_tuple[4], sql_tuple[0])
