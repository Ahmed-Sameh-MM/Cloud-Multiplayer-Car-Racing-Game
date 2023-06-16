import socket
import sys
from threading import Thread
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QTextEdit, QMessageBox

from message import Message
from player import Player
from car_game_client import GameWindow
from game_signal import GameSignal


MAIN_HOST = 'localhost'
BACKUP_HOST = '20.51.244.35'
CHAT_PORT = 20000
GAME_PORT = 20001
# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

chat_listening_thread = Thread()
game_listening_thread = Thread()


def open_window2():
    global window2, username  # Use the global window2 object

    username = username_field.text()
    window1.hide()
    window2.show()


def listen_for_messages_from_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        print(message)
        if message != '':
            final_message = Message.from_json(message)
            add_message(final_message.format_message())

        else:
            print("Message received from server is empty")


def listen_for_movements_from_server(game_socket: socket.socket, game_window: GameWindow):
    while True:
        player_data = game_socket.recv(2048).decode('utf-8')
        if player_data != '':
            final_player_data = Player.from_json(player_data)

            print('x_coordinate', final_player_data.x_coordinate, 'y_coordinate', final_player_data.y_coordinate)

            # update the player data
            game_window.update_player_data(final_player_data)

        else:
            print("Player Data received from server is empty")


def add_message(message: str):
    global username
    chat_box.append(message)


def clear():
    chat_box.clear()


def send_message():
    message = text_editor.text()
    if message != '':
        chat_socket.sendall(message.encode())
        text_editor.clear()
    else:
        show_error_message("Empty message, Message cannot be empty")


def read_game_signal(game_window: GameWindow):
    global game_listening_thread

    game_signal = game_socket.recv(2048).decode('utf-8')

    print('game signal:', game_signal)

    if game_signal == GameSignal.START.name:
        game_movements_thread = Thread(target=game_window.handle_movements, args=(game_socket,))
        game_movements_thread.start()

        game_listening_thread = Thread(target=listen_for_movements_from_server, args=(game_socket, game_window))
        game_listening_thread.start()

        # race car game running thread
        race_game_thread = Thread(target=game_window.start_race)
        race_game_thread.start()


def connect():
    global chat_listening_thread, game_listening_thread

    # try except block
    username = username_field.text()
    if username != '':
        try:
            # Connect to the server
            chat_socket.connect((MAIN_HOST, CHAT_PORT))
            game_socket.connect((MAIN_HOST, GAME_PORT))
            print("Successfully connected to server")

            open_window2()
            gameWindow = GameWindow()

            add_message("[SERVER] Successfully connected to the server")
            chat_socket.sendall(username.encode())

            chat_listening_thread = Thread(target=listen_for_messages_from_server, args=(chat_socket,))
            chat_listening_thread.start()

            game_signal_thread = Thread(target=read_game_signal, args=(gameWindow, ))
            game_signal_thread.start()

        except:
            show_error_message(f"Unable to connect to server, Unable to connect to server {MAIN_HOST} {CHAT_PORT}")
    else:
        show_error_message("Invalid username, Username cannot be empty")


def close_event_handler(event):
    # Perform any cleanup or additional actions before closing the window
    close_connection()
    event.accept()


def close_connection():
    print("Window is closing")
    chat_socket.close()
    game_socket.close()


def show_error_message(message):

    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error")
    error_dialog.setText(message)
    error_dialog.setStandardButtons(QMessageBox.Ok)
    error_dialog.setWindowModality(Qt.ApplicationModal)  # Make the dialog modal
    error_dialog.exec_()


username = ''
app = QApplication(sys.argv)

window1 = QMainWindow()
window1.setWindowTitle("Chat Room - Window 1")
window1.setGeometry(100, 100, 300, 100)

username_field = QLineEdit(window1)
username_field.setGeometry(10, 10, 180, 25)
join_button = QPushButton("Join", window1)
join_button.setGeometry(200, 10, 80, 25)
join_button.clicked.connect(connect)

window2 = None  # Declare window2 object globally
text_editor = QLineEdit(window2)
window2 = QWidget()
window2.setWindowTitle("Chat Room - Window 2")
window2.setGeometry(100, 100, 400, 300)
window2.closeEvent = close_event_handler
layout = QVBoxLayout(window2)

chat_box = QTextEdit(window2)
layout.addWidget(chat_box)

layout.addWidget(text_editor)

button_layout = QHBoxLayout()

send_button = QPushButton("Send", window2)
button_layout.addWidget(send_button)
send_button.clicked.connect(send_message)

clear_button = QPushButton("Clear", window2)
clear_button.clicked.connect(clear)
button_layout.addWidget(clear_button)

layout.addLayout(button_layout)


window1.show()

sys.exit(app.exec_())
