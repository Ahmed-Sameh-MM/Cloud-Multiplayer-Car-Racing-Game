import socket
from threading import Thread
import pickle

from message import Message
from sql_db import SQL
from active_client import ActiveClient
from movement import Movement
from car_game_client import GameWindow
from client_initializer import ClientInitializer

from typing import List

MAIN_SERVER_HOST = 'localhost'
MAIN_SERVER_CHAT_PORT = 20000
MAIN_SERVER_GAME_PORT = 20001


BACKUP_SERVER_HOST = '20.51.244.35'
BACKUP_SERVER_CHAT_PORT = 40000
BACKUP_SERVER_GAME_PORT = 40001
backup_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

LISTENER_LIMIT = 5

active_clients: List[ActiveClient] = []
disconnected_clients: List[ActiveClient] = []
sql = SQL()

car_data = [
    ClientInitializer(car_image='img/car_2.png', start_x=200),
    ClientInitializer(car_image='img/car_3.png', start_x=400)
]


def receive_messages(active_client: ActiveClient):

    while True:
        try:
            message = active_client.chat_socket.recv(2048).decode('utf-8')
            if message:
                final_message = Message(user_name=active_client.user_name, body=message)
                broadcast_message(final_message)

                # write the received message to the SQL database
                sql.write_message(final_message)

                # send_message_to_backup_server(final_message)
            else:
                print(f"The message sent from client {active_client.user_name} is empty")

        except ConnectionResetError:
            active_client.chat_socket.close()
            for client in active_clients:
                if client.address_info.ip_address == active_client.address_info.ip_address:

                    # if a client disconnects, remove them from the list of active clients
                    active_clients.remove(active_client)

                    # then add them to the disconnected clients
                    disconnected_clients.append(active_client)
                    print(disconnected_clients)
            break


def send_message(client_socket, message: Message):
    client_socket.sendall(message.to_json().encode())


def send_message_to_backup_server(message: Message):
    backup_server_socket.sendall(message.to_json().encode())


def broadcast_message(message: Message):
    for client in active_clients:
        send_message(client.chat_socket, message)


def handle_client(active_client: ActiveClient):
    while True:
        username = active_client.chat_socket.recv(2048).decode('utf-8')
        if username:
            active_client.user_name = username
            active_clients.append(active_client)

            prompt_message = Message(user_name='SERVER', body=f'{username} has been added to the chat')
            broadcast_message(prompt_message)
            break
        else:
            print("Client username is empty")

    Thread(target=receive_messages, args=(active_client, )).start()


def receive_movements(game_socket: socket.socket):
    while True:
        movements = Movement.from_json(game_socket.recv(2048).decode('utf-8'))

        print('left', movements.left, 'right', movements.right, 'up', movements.up, 'down', movements.down)

        print('x_coordinate:', movements.x_coordinate, 'y_coordinate:', movements.y_coordinate)

        # some processing
        player = GameWindow.handle_movements_server(movements=movements)

        game_socket.sendall(player.to_json().encode())


def send_start_game_signal():
    while True:
        if len(active_clients) == 2:
            for index, active_client in enumerate(active_clients):
                carData = car_data[index]
                active_client.game_socket.sendall(pickle.dumps(carData))
            break


def main():
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        chat_socket.bind((MAIN_SERVER_HOST, MAIN_SERVER_CHAT_PORT))
        print(f"Running the chat socket on {MAIN_SERVER_HOST}:{MAIN_SERVER_CHAT_PORT}")

        game_socket.bind((MAIN_SERVER_HOST, MAIN_SERVER_GAME_PORT))
        print(f"Running the game socket on {MAIN_SERVER_HOST}:{MAIN_SERVER_GAME_PORT}")
    except:
        print(f"Unable to bind to host {MAIN_SERVER_HOST} and port {MAIN_SERVER_CHAT_PORT}")

    chat_socket.listen(LISTENER_LIMIT)

    game_socket.listen(LISTENER_LIMIT)

    # backup server socket connection

    # backup_server_socket.connect((BACKUP_SERVER_HOST, BACKUP_SERVER_CHAT_PORT))

    # checks if at least 2 players have joined the game
    Thread(target=send_start_game_signal).start()

    while True:
        client_chat_socket, chat_address_info = chat_socket.accept()
        client_game_socket, game_address_info = game_socket.accept()

        for x in disconnected_clients:
            if chat_address_info[0] == x.address_info.ip_address:
                print(f"Successfully Reconnected to client {chat_address_info[0]}:{chat_address_info[1]}")

                # player_data = sql.get_player(ip_address=ip_address)

                # sending all the player data before disconnection

                # client_socket.sendall(all_messages.to_json().encode())
                # client_socket.sendall(player_data)

        print(f"Successfully connected to client {chat_address_info[0]}:{chat_address_info[1]}")

        active_client = ActiveClient(user_name='', chat_socket=client_chat_socket, game_socket=client_game_socket, address_info=chat_address_info)

        Thread(target=handle_client, args=(active_client, )).start()

        Thread(target=receive_movements, args=(client_game_socket, )).start()


main()
