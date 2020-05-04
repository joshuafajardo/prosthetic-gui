import socket
import os
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 1024

fileDir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(fileDir, 'script.txt'), 'r') as script:
    commands = script.readlines()
    print(commands)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print(str(s.recv(BUFFER_SIZE), 'utf-8'))

received = bytearray()
while True:
    for command in commands:
        command = command.strip()
        if not command:
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
        time.sleep(0.1)

s.shutdown(socket.SHUT_RDWR)
s.close()
