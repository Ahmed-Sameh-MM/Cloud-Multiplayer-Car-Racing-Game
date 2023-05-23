from constants import *
from message import Message

from kafka import KafkaConsumer

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

        self.kafka_consumer = KafkaConsumerWrapper()
        self.kafka_consumer.messageReceived.connect(self.update_text_browser)

        self.kafka_consumer_thread = QThread()
        self.kafka_consumer.moveToThread(self.kafka_consumer_thread)
        self.kafka_consumer_thread.started.connect(self.kafka_consumer.consume_messages)
        self.kafka_consumer_thread.start()

    @pyqtSlot(str)
    def update_text_browser(self, message):
        self.chatBox.append(message)


class KafkaConsumerWrapper(QObject):
    messageReceived = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def consume_messages(self):
        consumer = KafkaConsumer(TOPIC_NAME, api_version=(0, 10, 1), **consumer_config)
        consumer.subscribe([TOPIC_NAME])

        for consumer_message in consumer:
            message = Message.from_json(consumer_message.value)

            print("User Name:", message.user_name)
            print("Message:", message.text)

            self.messageReceived.emit(message.format_message())