class AddressInfo:

    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

    @classmethod
    def tuple_to_address_info(cls, address_info: tuple):
        return cls(ip_address=address_info[0], port=address_info[1])
