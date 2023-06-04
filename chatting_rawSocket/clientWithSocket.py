import socket
import sys
import threading
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QTextEdit, QMessageBox
print(sys.path)

HOST = '74.235.160.135'
PORT = 20000
# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def open_window2():
    global window2, username  # Use the global window2 object

    username = username_field.text()
    window1.hide()
    window2.show()


def listen_for_messages_from_server(client):
    while True:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")

        else:
            show_error_message("Error, Message recevied from client is empty")


def add_message(message):
    global username
    chat_box.append(f"{message}")


def clear():
    chat_box.clear()


def send_message():
    message = text_editor.text()
    if message != '':
        client.sendall(message.encode())
        text_editor.clear()
    else:
        show_error_message("Empty message, Message cannot be empty")


def connect():
    # try except block
    username = username_field.text()
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        show_error_message("Unable to connect to server, Unable to connect to server {HOST} {PORT}")
    if username != '':
        client.sendall(username.encode())

    else:
        show_error_message("Invalid username, Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
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
join_button.clicked.connect(open_window2)
join_button.clicked.connect(connect)

window2 = None  # Declare window2 object globally
text_editor = QLineEdit(window2)
window2 = QWidget()
window2.setWindowTitle("Chat Room - Window 2")
window2.setGeometry(100, 100, 400, 300)

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
