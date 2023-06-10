import socket
import threading

from message import Message
from sql_db import SQL
from active_client import ActiveClient

SERVER_HOST = ''
SERVER_PORT = 20000
LISTENER_LIMIT = 5

active_clients = []


def receive_messages(client_socket, username):

    sql = SQL()

    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')

            if message:
                final_message = Message(user_name=username, body=message)
                broadcast_message(final_message)

                # write the received message to the SQL database
                sql.write_message(final_message)
            else:
                print(f"The message sent from client {username} is empty")

        except ConnectionResetError:
            client_socket.close()
            break


def send_message(client_socket, message: Message):
    client_socket.sendall(message.to_json().encode())


def broadcast_message(message: Message):
    for client in active_clients:
        send_message(client.socket, message)


def handle_client(client_socket, ip_address):
    while True:
        username = client_socket.recv(2048).decode('utf-8')
        if username:
            active_client = ActiveClient(user_name=username, socket=client_socket, ip_address=ip_address)
            active_clients.append(active_client)

            prompt_message = Message(user_name='SERVER', body=f'{username} has been added to the chat')
            broadcast_message(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=receive_messages, args=(client_socket, username)).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((SERVER_HOST, SERVER_PORT))
        print(f"Running the server on {SERVER_HOST}:{SERVER_PORT}")
    except:
        print(f"Unable to bind to host {SERVER_HOST} and port {SERVER_PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client_socket, ip_address = server.accept()

        for x in active_clients:
            if ip_address == x.ip_address:
                print(f"Successfully Reconnected to client {ip_address[0]}:{ip_address[1]}")

                sql = SQL()
                all_messages = sql.read_all_messages()

                player_data = sql.get_player(ip_address=ip_address)

                # sending all messages in the saved server chat and all the player data before disconnection
                client_socket.sendall(all_messages)
                client_socket.sendall(player_data)

        print(f"Successfully connected to client {ip_address[0]}:{ip_address[1]}")

        threading.Thread(target=handle_client, args=(client_socket, ip_address)).start()


main()
