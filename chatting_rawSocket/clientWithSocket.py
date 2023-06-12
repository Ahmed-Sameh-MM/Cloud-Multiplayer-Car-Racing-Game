import socket
import sys
import threading
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QTextEdit, QMessageBox

from message import Message


print(sys.path)

MAIN_HOST = 'localhost'
BACKUP_HOST = '20.51.244.35'
PORT = 1234
# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_thread = threading.Thread()


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


def add_message(message: str):
    global username
    chat_box.append(message)


def clear():
    chat_box.clear()


def send_message():
    message = text_editor.text()
    if message != '':
        client_socket.sendall(message.encode())
        text_editor.clear()
    else:
        show_error_message("Empty message, Message cannot be empty")


def connect():
    global listening_thread

    # try except block
    username = username_field.text()
    if username != '':
        try:
            # Connect to the server
            client_socket.connect((MAIN_HOST, PORT))
            print("Successfully connected to server")
            open_window2()
            add_message("[SERVER] Successfully connected to the server")
            client_socket.sendall(username.encode())
            listening_thread = threading.Thread(target=listen_for_messages_from_server, args=(client_socket,))
            listening_thread.start()

        except:
            show_error_message(f"Unable to connect to server, Unable to connect to server {MAIN_HOST} {PORT}")
    else:
        show_error_message("Invalid username, Username cannot be empty")


def close_event_handler(event):
    # Perform any cleanup or additional actions before closing the window
    close_connection()
    event.accept()


def close_connection():
    print("Window is closing")
    client_socket.close()


def show_error_message(m):

    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setWindowTitle("Error")
    error_dialog.setText(m)
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
