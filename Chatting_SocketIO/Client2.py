from socketio import Client

client = Client()

clientName = 'Client 2'


def construct_message(message, sender):
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
    client.connect('http://16.170.255.185:8888')
    while True:
        msg = input()
        client.emit('message', construct_message(msg, f"{clientName}"))
