#!/usr/bin/env python3
import socket
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000      # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'mm')
    while True:
        data = s.recv(1024)
        data = eval(data)
        data = list(map(eval, list(map(lambda x: x.decode('utf-8'), data))))
        print(data)
    s.close()