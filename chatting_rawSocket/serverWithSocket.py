import socket
import threading

from message import Message
from sql_db import SQL

SERVER_HOST = ''
SERVER_PORT = 20000
LISTENER_LIMIT = 5
active_clients = []


def receive_messages(client, username):

    sql = SQL()

    while True:
        message = client.recv(2048).decode('utf-8')
        if message:
            final_message = Message(user_name=username, body=message)
            broadcast_message(final_message)

            # write the received message to the SQL database
            sql.write_message(final_message)
        else:
            print(f"The message sent from client {username} is empty")


def send_message(client, message: Message):
    client.sendall(message.to_json().encode())


def broadcast_message(message: Message):
    for user in active_clients:
        send_message(user[1], message)


def handle_client(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = Message(user_name='SERVER', body=f'{username} has been added to the chat')
            broadcast_message(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=receive_messages, args=(client, username)).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((SERVER_HOST, SERVER_PORT))
        print(f"Running the server on {SERVER_HOST}:{SERVER_PORT}")
    except:
        print(f"Unable to bind to host {SERVER_HOST} and port {SERVER_PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}:{address[1]}")

        threading.Thread(target=handle_client, args=(client,)).start()


main()
