import socket
from threading import Thread

from message import Message
from sql_db import SQL
from active_client import ActiveClient

from typing import List

BACKUP_SERVER_HOST = ''
BACKUP_SERVER_PORT = 40000
SERVER_PORT = 20000
LISTENER_LIMIT = 5

active_clients: List[ActiveClient] = []
disconnected_clients: List[ActiveClient] = []
sql = SQL()


def receive_messages(active_client: ActiveClient):

    while True:
        try:
            message = active_client.socket.recv(2048).decode('utf-8')
            if message:
                final_message = Message(user_name=active_client.user_name, body=message)
                broadcast_message(final_message)

                # write the received message to the SQL database
                sql.write_message(final_message)
            else:
                print(f"The message sent from client {active_client.user_name} is empty")

        except ConnectionResetError:
            active_client.socket.close()
            for client in active_clients:
                if client.address_info.ip_address == active_client.address_info.ip_address:

                    # if a client disconnects, remove them from the list of active clients
                    active_clients.remove(active_client)

                    # then add them to the disconnected clients
                    disconnected_clients.append(active_client)
                    print(disconnected_clients)
            break


def receive_from_main_server():

    backup_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    backup_socket.bind((BACKUP_SERVER_HOST, BACKUP_SERVER_PORT))

    backup_socket.listen(1)

    connection_socket, address_info = backup_socket.accept()

    while True:
        try:
            message = connection_socket.recv(2048).decode('utf-8')
            if message:
                final_message = Message.from_json(message)

                # write the received message to the SQL database
                sql.write_message(final_message)
            else:
                print("The message sent from the main server is empty")

        except ConnectionResetError:
            connection_socket.close()
            break


def send_message(client_socket, message: Message):
    client_socket.sendall(message.to_json().encode())


def broadcast_message(message: Message):
    for client in active_clients:
        send_message(client.socket, message)


def handle_client(client_socket, address_info):
    while True:
        username = client_socket.recv(2048).decode('utf-8')
        if username:
            active_client = ActiveClient(user_name=username, socket=client_socket, address_info=address_info)
            active_clients.append(active_client)

            prompt_message = Message(user_name='SERVER', body=f'{username} has been added to the chat')
            broadcast_message(prompt_message)
            break
        else:
            print("Client username is empty")

    Thread(target=receive_messages, args=(active_client, )).start()
    Thread(target=receive_from_main_server).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((BACKUP_SERVER_HOST, SERVER_PORT))
        print(f"Running the server on {BACKUP_SERVER_HOST}:{SERVER_PORT}")
    except:
        print(f"Unable to bind to host {BACKUP_SERVER_HOST} and port {SERVER_PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client_socket, address_info = server.accept()

        for x in disconnected_clients:
            if address_info[0] == x.address_info.ip_address:
                print(f"Successfully Reconnected to client {address_info[0]}:{address_info[1]}")

                # player_data = sql.get_player(ip_address=ip_address)

                # sending all the player data before disconnection

                # client_socket.sendall(all_messages.to_json().encode())
                # client_socket.sendall(player_data)

        print(f"Successfully connected to client {address_info[0]}:{address_info[1]}")

        Thread(target=handle_client, args=(client_socket, address_info)).start()


main()
