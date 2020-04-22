import socket
import re

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print(str(s.recv(BUFFER_SIZE), 'utf-8'))
print("Enter /close to close the socket.")
message_format = re.compile('-?[0-9]+ -?[0-9]+')

received = bytearray()
while True:
    command = input()
    if command == "/close":
        break
    elif not re.search(message_format, command):
        print("Message not properly formatted. Please try again.")
        continue
    command = bytearray(command, 'utf-8')
    command.insert(0, len(command))
    s.send(command)
    received.extend(s.recv(BUFFER_SIZE))
    if not received:
        break
    expected_size = received[0]
    while expected_size < len(received):
        print("Normal: ", str(received[1:expected_size + 1], 'utf-8'))
        if len(received) == expected_size + 1:
            received = bytearray()
        else:
            received = received[expected_size + 1:]
            expected_size = received[0]

s.shutdown(socket.SHUT_RDWR)
s.close()
