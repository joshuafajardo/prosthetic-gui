import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 1024

# TODO: make sure, beforehand my_model.APERTURE_GAIN = 100,  my_model.DIST_GAIN = 0.01
#  Settings: [0.25, 0.05, 0.04, 0.7, 0.4, 10**4]

raw_readings = [[401, 0],
                [399, 0],
                [395, 0],
                [395, 0]]
readings = []
for reading in raw_readings:
    as_bytes = bytearray(str(reading[0]) + ' ' + str(reading[1]), 'utf-8')
    as_bytes.insert(0, len(as_bytes))
    readings.append(as_bytes)
true_normals = ['0', '0', '0.5', '2.5']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
received = s.recv(BUFFER_SIZE)
print("Received: ", received)
received = bytearray()
received_normals = []
for reading in readings:
    s.send(reading)
    print("Sent: ", reading)
    received.extend(s.recv(BUFFER_SIZE))
    expected_size = received[0]
    while expected_size < len(received):
        print("Normal: ", str(received[1:expected_size + 1], 'utf-8'))
        received_normals.append(str(received[1:expected_size + 1], 'utf-8'))
        if len(received) == expected_size + 1:
            received = bytearray()
        else:
            received = received[expected_size + 1:]
            expected_size = received[0]
s.shutdown(socket.SHUT_RDWR)
s.close()
print("True normals: ", true_normals)
print("Success!")
