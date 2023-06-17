from game_signal import GameSignal


class ClientInitializer:

    def __init__(self, car_image: str, start_x: int):
        self.carImage = car_image

        self.start_x = start_x
        self.start_y = 500

        self.gameSignal = GameSignal.START.name
