import pyodbc

from credentials import *
from message import Message


class SQL:
    def __init__(self):
        # Establish the connection
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    # Read data from a table
    def read_all_messages(self):
        self.cursor.execute("SELECT * FROM Chat")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    # Write data to a table
    def write_message(self, message: Message):
        data = message.message_tuple()
        self.cursor.executemany("INSERT INTO Chat (UserName, Body) VALUES (?, ?)", data)
        self.conn.commit()

    def close_connection(self):
        # Close the connection
        self.conn.close()
