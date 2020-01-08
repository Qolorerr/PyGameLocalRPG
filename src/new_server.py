import socket
import select
import random
import struct
import math


class Server:
    def __init__(self, map_size, players):
        self.map_size = map_size
        self.players = players
        self.essences = []
        self.create_all_coord()
        self.whose_move = 1
        self.listener = None
        self.end_connecting = False
        self.len_essecses = int(math.sqrt(self.map_size * 4))
        self.ip = socket.gethostbyname(socket.gethostname())
        print(self.ip)

    def create_all_coord(self):
        self.all_coord = []
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.all_coord.append(tuple([x, y]))

    def generate_location(self):
        A = list(map(lambda x: tuple(x["location"]), self.essences))
        A = list(set(self.all_coord) - set(A))
        new_location = random.choice(A)
        return new_location

    def generate_new_being(self, texture):
        info = {"name": "Bot",
                "health": 40,
                "damage": 5,
                "location": self.generate_location(),
                "texture": texture,
                "gold": 20,
                "code": self.generate_essence_code(),
                "live": 1,
                "maxHealth": 40,
                "shield": 0,
                "maxShield": 20,
                "exp": 20,
                "type": 'essence'}
        self.essences.append(info)

    def generate_essence_code(self):
        A = list(map(lambda x: x["code"], self.essences))
        if self.essences == []:
            return 0
        A = min(list(set([i for i in range(max(A) + 2)]) - set(A)))
        return A

    def server_step(self):
        for i in range(self.len_essecses - len(self.essences)):
            self.generate_new_being('Being1')

    def generate_new_hero(self, texture):
        info = {"name": "Lox",
                "health": 100,
                "damage": 10,
                "location": self.generate_location(),
                "texture": texture,
                "gold": 100,
                "code": self.generate_essence_code(),
                "live": 1,
                "maxHealth": 100,
                "shield": 0,
                "maxShield": 20,
                "invise": 0,
                "move": 10,
                "maxGold": 100,
                "level": (1, 0, 100),
                "lvl_points": 1,
                "type": 'hero'}
        self.essences.append(info)

    def send_msg(self, msg, sock):
        # Каждое сообщение будет иметь префикс в 4 байта блинной(network byte order)
        msg = struct.pack('>I', len(msg)) + bytes(msg, encoding='utf-8')
        sock.send(msg)

    def recv_msg(self, sock):
        # Получение длины сообщения и распаковка в integer
        raw_msglen = self.recvall(4, sock)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Получение данных
        return self.recvall(msglen, sock)

    def recvall(self, n, sock):
        # Функция для получения n байт или возврата None если получен EOF
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def was_connected_all_clients(self, clients):
        for ind, sk in enumerate(clients):
            print('IND', ind)
            self.send_msg(str([self.essences, ind == 0]), sk)
        self.whose_move = self.whose_move % len(clients)

    def new_client(self, sock):
        self.generate_new_hero('Hero1')
        self.send_msg(str(self.essences[-1]["code"]), sock)
        self.send_msg(str(self.listener is None), sock)
        self.send_msg(str([self.essences, False]), sock)

    def setting(self, sock):
        self.listener = int(self.recv_msg(sock).decode('utf-8'))

    def start(self):
        sock_producer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_producer.bind((self.ip, 5000))
        sock_producer.listen(self.players)
        producers = []

        clients = []
        sock_consumer_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Note: different port to differentiate the clients who receive data from the one who sends messages
        sock_consumer_listener.bind((self.ip, 5001))

        rlist = [sock_producer, sock_consumer_listener]
        wlist = []
        errlist = []
        while True:
            if self.end_connecting is False and self.listener == len(rlist) - 2:
                self.was_connected_all_clients(rlist[2::])
                self.end_connecting = True
            if len(rlist) <= 2:
                self.listener = None
                self.essences.clear()
                self.end_connecting = False
            r, w, err = select.select(rlist, wlist, errlist)
            for sock in r:
                if sock == sock_producer:
                    prod, addr = sock.accept()
                    producers.append(prod)
                    self.new_client(prod)
                    if self.listener is None:
                        rlist.append(prod)
                        self.setting(prod)
                    elif self.listener > len(rlist) - 2:
                        rlist.append(prod)
                elif sock == sock_consumer_listener:
                    cons, addr = sock.accept()
                    clients.append(cons)
                    wlist.append(cons)
                elif self.listener is not None and self.end_connecting is True:
                    change = False
                    try:
                        info = self.recv_msg(sock)
                        out_buffer = list(map(lambda x: eval(x.decode('utf-8')), eval(info)))
                    except:
                        print("gg")
                        del(rlist[rlist.index(sock)])
                        out_buffer = []
                    if out_buffer != []:
                        self.essences = out_buffer
                        if self.whose_move == 0:
                            self.server_step()
                        for ind, s in enumerate(rlist[2::]):
                            if ind == self.whose_move:
                                change = True
                            mes = str([self.essences, bool(ind == self.whose_move)])
                            self.send_msg(mes, s)
                        self.whose_move = (self.whose_move + int(change)) % self.listener


server = Server(100, 8)
server.start()
