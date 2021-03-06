#!/usr/bin/env python3
import socket
from general import essences
from hero import Hero
from being import Being
import select
import struct


class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.data = None
        self.your_hero_id = int(self.recv_msg())
        self.you_main_client = bool(eval(self.recv_msg()))
        self.alive = False
        self.nick = None

    def change_essences(self):
        essences.clear()
        for es in self.data:
            if es["type"] == "hero":
                essences.append(Hero(es["name"],
                                     es['health'],
                                     es['damage'],
                                     es['location'],
                                     es['texture'],
                                     es["gold"]))
                essences[-1].mainHero = es["code"] == self.your_hero_id
                essences[-1].move_distance = es["move"]
                essences[-1].maxGold = es["maxGold"]
                essences[-1].invisible = es["invise"]
                essences[-1].level.level = es["level"][0]
                essences[-1].level.exp = es["level"][1]
                essences[-1].level.max_exp = es["level"][2]
                essences[-1].level.lvl_points = es["lvl_points"]
            elif es["type"] == "essence":
                essences.append(Being(es["name"],
                                      es['health'],
                                      es['damage'],
                                      es['location'],
                                      es['texture'],
                                      es['gold']))
            if es["code"] == self.your_hero_id:
                essences[-1].name = self.nick
                self.alive = True
                print("DHJLT YJHV")
            essences[-1].essence_code = es["code"]
            essences[-1].maxHealth = es["maxHealth"]
            essences[-1].shield = es["shield"]
            essences[-1].maxShield = es["maxShield"]

    def send_msg(self, msg):
        # Каждое сообщение будет иметь префикс в 4 байта блинной(network byte order)
        msg = struct.pack('>I', len(msg)) + bytes(msg, encoding='utf-8')
        self.sock.send(msg)

    def first_client(self, count_clients):
        self.send_msg(str(count_clients))

    def recv_msg(self):
        # Получение длины сообщения и распаковка в integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Получение данных
        return self.recvall(msglen)

    def recvall(self, n):
        # Функция для получения n байт или возврата None если получен EOF
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def get_info(self):
        r, w, err = select.select([self.sock], [self.sock], [], 0.1)
        if r != []:
            data = self.recv_msg()
            if data is None:
                return
            data = eval(data.decode('utf-8'))
            self.data = data[0]
            self.change_essences()
            return data[1]
        return None

    def disconnect(self):
        self.sock.close()
