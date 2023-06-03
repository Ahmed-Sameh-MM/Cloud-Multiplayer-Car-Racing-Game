import zmq

HOST = '16.170.255.185'
PORT = '20000'
context = zmq.Context()

p1 = "tcp://"+ HOST +":"+ PORT 
s  = context.socket(zmq.REQ)    

s.connect(p1)    
               
s.send("Hello world".encode())          
message = s.recv().decode()            
s.send("STOP".encode())                  
print(message)                   
