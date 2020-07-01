import socket
import csv
import os
import threading
from view import start_view
from controller import Controller

settings = []
fileDir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(fileDir, 'config.csv'), 'r') as config_csv:
    config_reader = csv.reader(config_csv)
    config_reader.__next__()
    for setting in config_reader:
        settings.append(setting)

"""
Server Stuff
https://www.youtube.com/watch?v=Lbfe3-v7yE0
https://www.youtube.com/watch?v=8A4dqoGL62E
Notes
A socket is an endpoint
"""
TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 1024

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPV4, SOCK_STREAM for TCP
s.bind((TCP_IP, TCP_PORT)) # localhost, port
s.listen(1) # Queue of 1
print("Waiting for user...")
client_s, address = s.accept()
print(f"Established connection to {address}.")
init_msg = bytearray("Connected to prosthetic-gui.", 'utf-8')
init_msg.insert(0, len(init_msg))
print(init_msg)
client_s.send(init_msg)

controller = Controller(settings)
view_thread = threading.Thread(target=start_view, args=(controller, controller.model), daemon=True)
view_thread.start()

msg = bytearray()
while True:
    chunk = client_s.recv(BUFFER_SIZE)
    if not chunk:
        print("Connection lost.")
        break
    msg.extend(chunk)
    expected_size = msg[0]
    while expected_size < len(msg):  # if we process at >= 2 at once, then we'll run into delta_t = 0
        result = controller.process_reading(str(msg[1:expected_size + 1], 'utf-8'))
        result = bytearray(result, 'utf-8')
        result.insert(0, len(result))
        client_s.send(result)
        if len(msg) == expected_size + 1:
            msg = bytearray()
        else:
            msg = msg[expected_size + 1:]
            expected_size = msg[0]

client_s.shutdown(socket.SHUT_RDWR)
client_s.close()
