from constants import *
from ui import MyMainWindow
from message import Message

from kafka import KafkaProducer
from kafka import KafkaConsumer

from PyQt5.QtWidgets import QApplication, QTextEdit, QPushButton, QTextBrowser

import sys


class Chat:

    def __init__(self):
        self.producer = KafkaProducer(** producer_config, api_version=(0, 10, 1))

        self.consumer = KafkaConsumer(TOPIC_NAME, api_version=(0, 10, 1), **consumer_config)

        # Create the application instance
        self.app = QApplication(sys.argv)

        # Create an instance of your main window class
        self.chat_window = MyMainWindow()

        self.show_chat_dialog()

        self.receive_message()

    def show_chat_dialog(self):

        sendButton = self.chat_window.sendButton
        sendButton.clicked.connect(self.send_message)

        # Show the window on the screen
        self.chat_window.show()

        # Start the application event loop
        self.app.exec_()

    def send_message(self):
        text_message = self.chat_window.textEdit.toPlainText()

        if text_message != '':
            message = Message(user_name='Tera_Byte', text=text_message)

            self.producer.send(TOPIC_NAME, value=message.to_json())

            self.producer.flush()

            self.chat_window.textEdit.setText('')

    def receive_message(self):
        for consumer_message in self.consumer:
            message = Message.from_json(consumer_message.value)

            print("User Name:", message.user_name)
            print("Message:", message.text)

            chatBox = self.chat_window.chatBox

            chatBox.append(message.format_message())
