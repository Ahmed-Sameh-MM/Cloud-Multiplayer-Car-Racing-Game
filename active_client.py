from address_info import AddressInfo


class ActiveClient:

    def __init__(self, user_name: str, socket, address_info: tuple):
        self.user_name = user_name
        self.socket = socket
        self.address_info = AddressInfo.tuple_to_address_info(address_info)
