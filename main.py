import socket
import csv
from controller import Controller


settings = []
with open('config.csv', 'r') as config_csv:
    config_reader = csv.reader(config_csv)
    config_reader.next()
    for setting in config_reader:
        settings.append(setting)


"""
Server Stuff
https://www.youtube.com/watch?v=Lbfe3-v7yE0
https://www.youtube.com/watch?v=8A4dqoGL62E
Notes
A socket is an endpoint
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPV4, SOCK_STREAM for TCP
s.bind((socket.gethostname(), 7777)) # localhost, port
s.listen(5) # Queue of 5 jic we get too many signals

controller = Controller(settings)
controller.view.main()

#TODO: Make a script reader


while True:
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established.")
    client_socket.send(bytes("Welcome to the server!", "utf-8"))