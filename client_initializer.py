from game_signal import GameSignal


class ClientInitializer:

    def __init__(self, car_image: str, start_x: int, ip_address: str = None):
        self.carImage = car_image

        self.start_x = start_x
        self.start_y = 500

        self.gameSignal = GameSignal.START.name

        self.IpAddress = ip_address
