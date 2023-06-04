from constants import *
from ui import MyMainWindow
from message import Message

from PyQt5.QtWidgets import QApplication

import sys


class Chat:

    def __init__(self):
        # Create the application instance
        self.app = QApplication(sys.argv)

        # Create an instance of your main window class
        self.chat_window = MyMainWindow()

        self.show_chat_dialog()

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

            self.chat_window.textEdit.setText('')

        else:
            chatBox = self.chat_window.chatBox

            red_text = '<span style="color: red;">Cant Send an Empty Message !</span><br>'
            chatBox.insertHtml(red_text)

    def receive_message(self):
        message = Message.from_json("{'user_name': 'Ahmed Sameh', }")

        print("User Name:", message.user_name)
        print("Message:", message.text)

        chatBox = self.chat_window.chatBox

        chatBox.append(message.format_message())
