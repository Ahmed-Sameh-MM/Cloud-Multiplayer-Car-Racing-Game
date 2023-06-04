import pyodbc

from credentials import *


# Establish the connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


# Read data from a table
def read_all_messages():
    cursor.execute("SELECT * FROM Message")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Write data to a table
def write_data():
    data = [('JohnDoe', 'Hello, how are you?'), ('Jane', 'Hello, how are you?')]  # Example data to be inserted
    cursor.executemany("INSERT INTO Message (UserName, Body) VALUES (?, ?)", data)
    conn.commit()


write_data()
read_all_messages()

# Close the connection
conn.close()
