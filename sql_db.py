import pyodbc

from sql_server_credentials import *
from message import Message
from player import Player


class SQL:
    def __init__(self):
        # Establish the connection
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

    # Write data to a table
    def write_message(self, message: Message):
        data = message.message_tuple()
        self.cursor.execute("INSERT INTO Chat (UserName, Body) VALUES (?, ?)", data)
        self.conn.commit()

    def get_player(self, ip_address: str):
        self.cursor.execute("SELECT * FROM Player WHERE IpAddress = ?", (ip_address,))
        player = self.cursor.fetchone()
        if player:
            return player
        else:
            print('Player Not Found')
            return None

    def get_all_players(self):
        self.cursor.execute("SELECT * FROM Player")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    # Write data to a table
    def write_player(self, player: Player):
        data = player.player_tuple()
        self.cursor.execute("INSERT INTO Player (IpAddress, X_Coordinate, Y_Coordinate, Progress) VALUES (?, ?, ?, ?)", data)
        self.conn.commit()

    def update_player(self, player: Player):
        data = player.player_update_tuple()
        self.cursor.execute("UPDATE Player SET X_Coordinate=?, Y_Coordinate=?, Progress=? WHERE IpAddress=?;", data)
        self.conn.commit()

    def delete_all_players(self):
        self.cursor.execute("DELETE FROM Player")
        self.conn.commit()

    def close_connection(self):
        # Close the connection
        self.conn.close()
