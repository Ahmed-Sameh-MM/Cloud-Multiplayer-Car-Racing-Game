from constants import *
from ui import MyMainWindow
from message import Message

from kafka import KafkaProducer
from kafka import KafkaConsumer

from PyQt5.QtWidgets import QApplication, QTextEdit, QPushButton

import sys


class Chat:

    def __init__(self):
        self.producer = KafkaProducer(** producer_config, api_version=(0, 10, 1))

        self.consumer = KafkaConsumer(TOPIC_NAME, api_version=(0, 10, 1), **consumer_config)

        self.show_chat_dialog()

    def show_chat_dialog(self):
        # Create the application instance
        app = QApplication(sys.argv)

        # Create an instance of your main window class
        self.chat_window = MyMainWindow().return_chat_widget()

        self.textEdit = self.chat_window.findChild(QTextEdit, 'textEdit')

        sendButton = self.chat_window.findChild(QPushButton, 'sendButton')

        sendButton.clicked.connect(self.send_message)

        # Show the window on the screen
        self.chat_window.show()

        # Start the application event loop
        app.exec_()

    def send_message(self):
        text_message = self.chat_window.textEdit.toPlainText()

        if text_message != '':
            print(text_message)

            message = Message(user_name='Tera_Byte', text=text_message)

            self.producer.send(TOPIC_NAME, value=message.to_json())

            self.producer.flush()

            self.textEdit.setText('')

            self.receive_message()

    def receive_message(self):
        for message in self.consumer:
            print(message)
