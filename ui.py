from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QTextBrowser, QPushButton


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
