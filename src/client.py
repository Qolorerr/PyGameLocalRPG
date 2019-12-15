#!/usr/bin/env python3
import socket
from general import essences
from hero import Hero


class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.data = None

    def send_info(self, mes: bytes):
        self.sock.sendall(mes)
        return True

    def change_essences(self):
        print(self.data)
        for ind, es in enumerate(self.data):
            essence_ind = None
            for i, b in enumerate(essences):
                if b.essence_code == es['code']:
                    essence_ind = i
            if essence_ind is None:
                if essences == [] and ind == 0:
                    essences.append(Hero(es['health'],
                                         es['damage'],
                                         es['location'],
                                         es['texture'],
                                         es['code'],
                                         5,
                                         10,
                                         True))
                else:
                    essences.append(Hero(es['health'],
                                         es['damage'],
                                         es['location'],
                                         es['texture'],
                                         es['code'],
                                         5,
                                         10,
                                         False))
                continue
            essences[essence_ind].health = es['health']
            essences[essence_ind].damage = es['damage']
            essences[essence_ind].location = es['location']
            essences[essence_ind].exp = es['exp']
            essences[essence_ind].gold = es['gold']
            essences[essence_ind].live = es['live']
            essences[essence_ind].who_killed_me = es['who_killed']

    def get_info(self):
        data = b''
        while data == b'':
            data = self.sock.recv(1024)
        print(data)
        data = eval(data)
        self.data = list(map(eval, list(map(lambda x: x.decode('utf-8'), data))))
        print(self.data)

    def disconnect(self):
        self.sock.close()
