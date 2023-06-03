import zmq

HOST = '127.0.0.1'
PORT = '8888'


context = zmq.Context()

p1 = "tcp://" + HOST + ":" + PORT

s = context.socket(zmq.REP)

s.bind(p1)

while True:
    message = s.recv().decode()
    if not "STOP" in message:
        s.send((message + "*").encode())
    else:
        break
