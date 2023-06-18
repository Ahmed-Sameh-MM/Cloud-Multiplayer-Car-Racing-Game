from game_signal import GameSignal


class ClientInitializer:

    def __init__(self, car_image: str, start_x: int, start_y: int = 500, ip_address: str = None, progress: int = 0):
        self.carImage = car_image

        self.start_x = start_x
        self.start_y = start_y

        self.gameSignal = GameSignal.START.name

        self.IpAddress = ip_address

        self.progress = progress
