import pickle


class Movement:

    def __init__(self, left: bool, right: bool, up: bool, down: bool, x_coordinate: int, y_coordinate: int, progress: int):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        self.progress = progress

    def to_pickle(self):
        return pickle.dumps(self.__dict__)

    @classmethod
    def from_pickle(cls, pickle_str):
        movement = pickle.loads(pickle_str)
        return cls(movement['left'], movement['right'], movement['up'], movement['down'], movement['x_coordinate'], movement['y_coordinate'], movement['progress'])
