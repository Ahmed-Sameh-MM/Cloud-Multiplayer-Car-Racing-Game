from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QTextEdit, QPushButton


# Create a QMainWindow object to load the UI into
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chat_widget = QWidget()

        # Load the .ui file
        uic.loadUi('ui/chat.ui', self.chat_widget)

    def return_chat_widget(self):
        return self.chat_widget
