#!/usr/bin/env python3
import socket
from general import essences
from hero import Hero
from being import Being


class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.data = None
        self.your_hero_id = int(self.sock.recv(1024).decode('utf-8'))

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
                if es["type"] == "hero":
                    essences.append(Hero(es['health'],
                                         es['damage'],
                                         es['location'],
                                         es['texture'],
                                         5,
                                         10,
                                         es["code"] == self.your_hero_id))
                    essences[-1].essence_code = es["code"]
                else:
                    essences.append(Being(es['health'],
                                          es['damage'],
                                          es['location'],
                                          es['texture'],
                                          es["exp"],
                                          es['gold']))
                    essences[-1].essence_code = es["code"]
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
        data = eval(data.decode('utf-8'))
        if data[-1] is True:
            self.data = data[0]
            print(self.data)
            return True
        else:
            self.data = data
            print(self.data)
            return False

    def disconnect(self):
        self.sock.close()
