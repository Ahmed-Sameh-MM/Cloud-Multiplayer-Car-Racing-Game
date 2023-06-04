from constants import *
from message import Message

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QTextBrowser, QPushButton
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread


# Create a QMainWindow object to load the UI into
class MyMainWindow(QMainWindow):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

        if hasattr(self, 'initialized'):
            return

        self.initialized = True

        # Load the .ui file
        uic.loadUi('ui/chat.ui', self)

        self.chatBox = self.findChild(QTextBrowser, 'chatBox')

        self.textEdit = self.findChild(QTextEdit, 'textEdit')

        self.sendButton = self.findChild(QPushButton, 'sendButton')

        self.consumer = ConsumerWrapper()
        self.consumer.messageReceived.connect(self.update_text_browser)

        self.consumer_thread = QThread()
        self.consumer.moveToThread(self.consumer_thread)
        self.consumer_thread.started.connect(self.consumer.consume_messages)
        self.consumer_thread.start()

    @pyqtSlot(str)
    def update_text_browser(self, message):
        self.chatBox.append(message)


class ConsumerWrapper(QObject):
    messageReceived = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def consume_messages(self):
        message = Message.from_json("{'user_name': 'Ahmed Sameh', }")

        print("User Name:", message.user_name)
        print("Message:", message.text)

        self.messageReceived.emit(message.format_message())
