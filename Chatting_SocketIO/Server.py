from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


def construct_message(message, sender):
    return {
        'msg': message,
        'sender': sender
    }


@socketio.on('connect')
def handle_connect():
    emit('message', construct_message('Client Connected', "Server"), broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    emit('message', construct_message('Client Disconnected', "Server"), broadcast=True)


@socketio.on('message')
def handle_message(data: dict):
    emit('message', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, "localhost", 5050, allow_unsafe_werkzeug=True)
