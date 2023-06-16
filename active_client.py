import socket

from address_info import AddressInfo


class ActiveClient:

    def __init__(self, user_name: str, chat_socket: socket.socket, game_socket: socket.socket, address_info: tuple):
        self.user_name = user_name
        self.chat_socket = chat_socket
        self.game_socket = game_socket
        self.address_info = AddressInfo.tuple_to_address_info(address_info)
