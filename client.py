import socket
import sys
from threading import Thread
from PyQt5.QtCore import Qt
import pickle

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QTextEdit, QMessageBox

from message import Message
from player import Player
from car_game_client import GameWindow
from game_signal import GameSignal


MAIN_HOST = '40.76.226.192'
BACKUP_HOST = '20.51.244.35'
CHAT_PORT = 20000
GAME_PORT = 20001
CHECKING_PORT = 20002
# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

chat_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
game_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

chat_listening_thread = Thread()
game_listening_thread = Thread()

SWITCH = False

gameWindow = None


def switch_to_backup():
    global SWITCH

    if SWITCH:
        return

    # Connect to the backup server
    chat_socket_2.connect((BACKUP_HOST, CHAT_PORT))
    game_socket_2.connect((BACKUP_HOST, GAME_PORT))
    SWITCH = True

    chat_socket_2.sendall(username.encode())

    print("Successfully connected to backup server")

    gameWindow.change_switch()


def open_window2():
    global window2, username  # Use the global window2 object

    username = username_field.text()
    window1.hide()
    window2.show()


def listen_for_messages_from_server():
    while True:
        try:
            message = None
            if SWITCH:
                message = chat_socket_2.recv(2048).decode('utf-8')
            else:
                message = chat_socket.recv(2048).decode('utf-8')
            print(message)
            if message != '':
                final_message = Message.from_json(message)
                add_message(final_message.format_message())

            else:
                print("Message received from server is empty")
        except:
            print('SOCKET ERROR listen_for_messages_from_server()')
            switch_to_backup()


def listen_for_movements_from_server():
    while True:
        try:
            if SWITCH:
                player_data = game_socket_2.recv(2048)
            else:
                player_data = game_socket.recv(2048)
            if player_data != '':
                final_player_data = Player.from_pickle(player_data)

                print('x_coordinate', final_player_data.x_coordinate, 'y_coordinate', final_player_data.y_coordinate)

                # update the player data
                gameWindow.update_player_data(final_player_data)

            else:
                print("Player Data received from server is empty")

        except:
            print('SOCKET ERROR listen_for_movements_from_server()')
            switch_to_backup()


def add_message(message: str):
    global username
    chat_box.append(message)


def clear():
    chat_box.clear()


def send_message():
    message = text_editor.text()

    try:
        if message != '':
            if SWITCH:
                chat_socket_2.sendall(message.encode())
            else:
                chat_socket.sendall(message.encode())
            text_editor.clear()
        else:
            show_error_message("Empty message, Message cannot be empty")

    except:
        print('SOCKET ERROR send_message()')
        switch_to_backup()


def read_game_signal():
    global game_listening_thread

    try:
        initializationData = pickle.loads(game_socket.recv(2048))

        game_signal = initializationData.car_data_list[initializationData.index].gameSignal

        gameWindow.client_initiliazation(initialization_data=initializationData)

        if game_signal == GameSignal.START.name:
            game_movements_thread = Thread(target=gameWindow.handle_movements, args=(game_socket, game_socket_2))
            game_movements_thread.start()

            game_listening_thread = Thread(target=listen_for_movements_from_server)
            game_listening_thread.start()

            # race car game running thread
            race_game_thread = Thread(target=gameWindow.start_race)
            race_game_thread.start()

    except:
        print('SOCKET ERROR read_game_signal()')
        switch_to_backup()


def connect():
    global chat_listening_thread, game_listening_thread, gameWindow

    # try except block
    username = username_field.text()
    if username != '':
        try:
            # Connect to the main server
            chat_socket.connect((MAIN_HOST, CHAT_PORT))
            game_socket.connect((MAIN_HOST, GAME_PORT))
            print("Successfully connected to main server")

            open_window2()
            gameWindow = GameWindow()

            add_message("[SERVER] Successfully connected to the main server")
            chat_socket.sendall(username.encode())

            chat_listening_thread = Thread(target=listen_for_messages_from_server)
            chat_listening_thread.start()

            game_signal_thread = Thread(target=read_game_signal)
            game_signal_thread.start()

            # checking_thread = Thread(target=check_main_server_connection)
            # checking_thread.start()

        except:
            show_error_message(f"Unable to connect to server, Unable to connect to the MAIN server at {MAIN_HOST}:{CHAT_PORT}")

            # Connect to the backup server
            chat_socket.connect((BACKUP_HOST, CHAT_PORT))
            game_socket.connect((BACKUP_HOST, GAME_PORT))
            print("Successfully connected to backup server")

            open_window2()
            gameWindow = GameWindow()

            add_message("[SERVER] Successfully connected to the backup server")
            chat_socket.sendall(username.encode())

            chat_listening_thread = Thread(target=listen_for_messages_from_server)
            chat_listening_thread.start()

            game_signal_thread = Thread(target=read_game_signal, args=(gameWindow,))
            game_signal_thread.start()
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
