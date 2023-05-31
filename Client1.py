from socketio import Client

client = Client()
clientName = 'Client 1'


def ConstructMessage(message, sender):
    return {
        'msg': message,
        'sender': sender
    }


@client.on('message')
def handle_message(data: dict):
    print(f"{data['sender']}: {data['msg']}")


@client.on('disconnect')
def handle_disconnect():
    print('Disconnected from the server')


@client.on('connect')
def handle_connect():
    print('Connected to the server')


if __name__ == '__main__':
    client.connect('http://localhost:5050')
    while True:
        msg = input()
        client.emit('message', ConstructMessage(msg, f"{clientName}"))

