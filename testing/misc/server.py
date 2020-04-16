import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 20

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPV4, SOCK_STREAM for TCP
s.bind((TCP_IP, TCP_PORT)) # localhost, port
s.listen(1) # Queue of 1

client_s, address = s.accept()
print(f"Established connection to {address}.")
client_s.send(bytes("Connected to prosthetic-testing-server.", "utf-8"))

while True:
    chunk = client_s.recv(BUFFER_SIZE)
    if not chunk:
        print("Connection lost.")
        break
    print(chunk) #TODO remove later
    client_s.send(bytes(chunk))

client_s.close()