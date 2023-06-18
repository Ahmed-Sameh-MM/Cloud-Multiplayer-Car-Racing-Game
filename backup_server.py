import socket
from threading import Thread
import pickle

from message import Message
from sql_db import SQL
from active_client import ActiveClient
from movement import Movement
from client_initializer import ClientInitializer
from player import Player
from initialization_data import InitializationData
from car_game_server import handle_movements_server

from typing import List

BACKUP_SERVER_HOST = ''
MAIN_SERVER_CHAT_PORT = 40000
MAIN_SERVER_GAME_PORT = 40001

BACKUP_SERVER_CHAT_PORT = 20000
BACKUP_SERVER_GAME_PORT = 20001
LISTENER_LIMIT = 5

active_clients: List[ActiveClient] = []
disconnected_clients: List[ActiveClient] = []
sql = SQL()

car_data = [
    ClientInitializer(car_image='img/car_2.png', start_x=200),
    ClientInitializer(car_image='img/car_3.png', start_x=400)
]

car_positions = {}

DISCONNECTED = False

DELETE_COUNTER = 0


def receive_messages(active_client: ActiveClient):

    while True:
        try:
            message = active_client.chat_socket.recv(2048).decode('utf-8')
            if message:
                final_message = Message(user_name=active_client.user_name, body=message)
                broadcast_message(final_message)

                # write the received message to the SQL database
                sql.write_message(final_message)
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


def receive_messages_from_main_server():

    main_chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        main_chat_socket.bind((BACKUP_SERVER_HOST, MAIN_SERVER_CHAT_PORT))
        print(f"Running the server on {BACKUP_SERVER_HOST}:{MAIN_SERVER_CHAT_PORT}")

    except:
        print(f"Unable to bind to host {BACKUP_SERVER_HOST} and port {MAIN_SERVER_CHAT_PORT}")

    main_chat_socket.listen(1)

    main_server_chat_socket, main_server_chat_address_info = main_chat_socket.accept()

    print(f"Successfully connected to the Main Server @ {main_server_chat_address_info[0]}:{main_server_chat_address_info[1]}")

    while True:
        try:
            message = main_server_chat_socket.recv(2048).decode('utf-8')
            if message:
                final_message = Message.from_json(message)

                # write the received message to the SQL database
                sql.write_message(final_message)
            else:
                print("The message sent from the main server is empty")
                main_server_chat_socket.close()
                break

        except ConnectionResetError:
            main_server_chat_socket.close()
            break


def receive_movements_from_main_server():

    main_game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        main_game_socket.bind((BACKUP_SERVER_HOST, MAIN_SERVER_GAME_PORT))
        print(f"Running the server on {BACKUP_SERVER_HOST}:{MAIN_SERVER_GAME_PORT}")
    except:
        print(f"Unable to bind to host {BACKUP_SERVER_HOST} and port {MAIN_SERVER_CHAT_PORT}")

    main_game_socket.listen(1)

    main_server_game_socket, main_server_game_address_info = main_game_socket.accept()

    print(f"Successfully connected to the Main Server @ {main_server_game_address_info[0]}:{main_server_game_address_info[1]}")

    sql.delete_all_players()

    while True:
        try:
            player = main_server_game_socket.recv(2048)
            if player:
                final_player = Player.from_pickle(player)

                # write the received message to the SQL database
                if final_player.CarImage == '':
                    sql.update_player(final_player)

                elif final_player.x_coordinate == -1000 and final_player.y_coordinate == -1000 and final_player.progress == -1000 and final_player.tarteeb == -1000 and final_player.CarImage == '-1000':
                    sql.delete_all_players()

                else:
                    sql.write_player(final_player)

            else:
                print("The message sent from the main server is empty")
                main_server_game_socket.close()
                break

        except ConnectionResetError:
            main_server_game_socket.close()
            break


def send_message(client_socket, message: Message):
    client_socket.sendall(message.to_json().encode())


def broadcast_message(message: Message):
    for client in active_clients:
        send_message(client.chat_socket, message)


def send_movement(client_socket, player: Player):
    client_socket.sendall(player.to_pickle())


def broadcast_movement(player: Player):
    for active_client in active_clients:
        send_movement(active_client.game_socket, player)


def recover_from_disconnection(recovered_ip: str, game_socket: socket.socket):
    car_data_recovered = []

    players = sql.get_all_players()

    recovered_player = None
    other_player = None

    for player in players:
        if recovered_ip == player.IpAddress:
            recovered_player = player
        else:
            other_player = player

    initializer_1 = ClientInitializer(car_image=recovered_player.CarImage, start_x=recovered_player.x_coordinate, start_y= recovered_player.x_coordinate, ip_address=recovered_ip, progress=recovered_player.progress)

    initializer_2 = ClientInitializer(car_image=other_player.CarImage, start_x=other_player.x_coordinate, start_y= other_player.x_coordinate, ip_address=other_player.IpAddress, progress=other_player.progress)

    car_data_recovered.append(initializer_1)
    car_data_recovered.append(initializer_2)

    initializationData = InitializationData(car_data_list=car_data_recovered, index=0)
    game_socket.sendall(pickle.dumps(initializationData))


def handle_client(active_client: ActiveClient):
    while True:
        username = active_client.chat_socket.recv(2048).decode('utf-8')
        if username:
            active_client.user_name = username
            active_clients.append(active_client)

            if DISCONNECTED:
                for active_client in active_clients:
                    print(f"Successfully Reconnected to client {active_client.address_info.ip_address} : {active_client.address_info.port}")
                    recover_from_disconnection(active_client.address_info.ip_address, active_client.game_socket)

            prompt_message = Message(user_name='SERVER', body=f'{username} has been added to the chat')
            broadcast_message(prompt_message)
            break
        else:
            print("Client username is empty")

    Thread(target=receive_messages, args=(active_client, )).start()


def receive_movements(game_socket: socket.socket, ip_address: str):
    global DELETE_COUNTER
    while True:
        movements = Movement.from_pickle(game_socket.recv(2048))

        if movements.left:
            print("LEFT")
        if movements.right:
            print("RIGHT")
        if movements.up:
            print("UP")
        if movements.down:
            print("DOWN")


        # some processing
        player = handle_movements_server(movements=movements, ip_address=ip_address)

        sql.update_player(player)

        if car_data[0].IpAddress == ip_address:
            print('Player 1')

            car_positions[ip_address]['x_coordinate'] = player.x_coordinate
            car_positions[ip_address]['y_coordinate'] = player.y_coordinate

            if car_positions[ip_address]['y_coordinate'] < car_positions[car_data[1].IpAddress]['y_coordinate']:
                player.tarteeb = 1

            else:
                player.tarteeb = 2

        elif car_data[1].IpAddress == ip_address:
            print('Player 2')

            car_positions[ip_address]['x_coordinate'] = player.x_coordinate
            car_positions[ip_address]['y_coordinate'] = player.y_coordinate

            if car_positions[ip_address]['y_coordinate'] < car_positions[car_data[0].IpAddress]['y_coordinate']:
                player.tarteeb = 1

            else:
                player.tarteeb = 2

        print('BEFORE:: ', 'x:', movements.x_coordinate, 'y:', movements.y_coordinate)

        print('AFTER:: ', 'x:', player.x_coordinate, 'y:', player.y_coordinate)

        print('\n\n')

        # send the returned movements to all the players
        broadcast_movement(player=player)

        if player.progress == 100:
            DELETE_COUNTER = DELETE_COUNTER + 1

        if DELETE_COUNTER == 2:
            DELETE_COUNTER = 0
            sql.delete_all_players()


def send_start_game_signal():
    while True:
        if len(active_clients) == 2:

            car_data[0].IpAddress = active_clients[0].address_info.ip_address
            car_data[1].IpAddress = active_clients[1].address_info.ip_address

            player_1 = Player(ip_address=car_data[0].IpAddress, x_coordinate=car_data[0].start_x, y_coordinate=car_data[0].start_y, progress=0, tarteeb=0, car_image='img/car_2.png')
            player_2 = Player(ip_address=car_data[1].IpAddress, x_coordinate=car_data[1].start_x, y_coordinate=car_data[1].start_y, progress=0, tarteeb=0, car_image='img/car_3.png')

            sql.delete_all_players()

            sql.write_player(player_1)
            sql.write_player(player_2)

            car_positions.clear()

            car_positions[player_1.IpAddress] = {'x_coordinate': player_1.x_coordinate, 'y_coordinate': player_1.y_coordinate}
            car_positions[player_2.IpAddress] = {'x_coordinate': player_2.x_coordinate, 'y_coordinate': player_2.y_coordinate}

            for index, active_client in enumerate(active_clients):
                initializationData = InitializationData(car_data_list=car_data, index=index)
                active_client.game_socket.sendall(pickle.dumps(initializationData))
            break


def main():
    global DISCONNECTED

    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        chat_socket.bind((BACKUP_SERVER_HOST, BACKUP_SERVER_CHAT_PORT))
        print(f"Running the chat socket on {BACKUP_SERVER_HOST}:{BACKUP_SERVER_CHAT_PORT}")

        game_socket.bind((BACKUP_SERVER_HOST, BACKUP_SERVER_GAME_PORT))
        print(f"Running the game socket on {BACKUP_SERVER_HOST}:{BACKUP_SERVER_GAME_PORT}")
    except:
        print(f"Unable to bind to host {BACKUP_SERVER_HOST} and port {BACKUP_SERVER_CHAT_PORT}")

    chat_socket.listen(LISTENER_LIMIT)

    game_socket.listen(LISTENER_LIMIT)

    Thread(target=receive_messages_from_main_server).start()

    Thread(target=receive_movements_from_main_server).start()

    players = sql.get_all_players()

    if len(players) != 0:
        DISCONNECTED = True

    if not DISCONNECTED:
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

        active_client = ActiveClient(user_name='', chat_socket=client_chat_socket, game_socket=client_game_socket, address_info=game_address_info)

        Thread(target=handle_client, args=(active_client, )).start()

        Thread(target=receive_movements, args=(client_game_socket, active_client.address_info.ip_address)).start()


main()
