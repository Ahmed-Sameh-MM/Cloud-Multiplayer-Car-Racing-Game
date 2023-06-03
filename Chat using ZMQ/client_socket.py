import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('74.235.160.135', 20000)) # connect to server (block until accepted)
msg = "Hello World"     # compose a message
s.send(msg.encode())    # send the message
data = s.recv(2048)     # receive the response
print(data.decode())    # print the result
s.close()               # close the connection
