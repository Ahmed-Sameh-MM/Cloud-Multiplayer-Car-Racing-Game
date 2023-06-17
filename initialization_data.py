from typing import List
from client_initializer import ClientInitializer


class InitializationData:

    def __init__(self, car_data_list: List[ClientInitializer], index: int):
        self.car_data_list = car_data_list
        self.index = index
