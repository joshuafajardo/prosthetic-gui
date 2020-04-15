import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
received = s.recv(BUFFER_SIZE)
print("received: ", received)
i = 0
#for letter in MESSAGE:
#    s.send(bytes(letter, "utf-8"))
s.send(bytes(MESSAGE, "utf-8"))
s.close()
