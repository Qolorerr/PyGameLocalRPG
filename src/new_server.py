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
        self.end_session = False
        self.bots_lvl = 1

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

    def heroes_lvls(self):
        lvls_sum = 0
        heroes = 0
        for i in self.essences:
            if i["type"] == "hero":
                heroes += 1
                lvls_sum += i["level"][0]

        self.bots_lvl = max(lvls_sum // max(heroes, 1), 1)

    def generate_new_being(self, texture):
        self.heroes_lvls()
        info = {"name": "Bot",
                "health": min(40 + self.bots_lvl, 50),
                "damage": 5 + self.bots_lvl,
                "location": self.generate_location(),
                "texture": texture,
                "gold": 20,
                "code": self.generate_essence_code(),
                "live": 1,
                "maxHealth": min(40 + self.bots_lvl, 50),
                "shield": min(int(self.bots_lvl > 3) * int(1.5 ** self.bots_lvl), 40),
                "maxShield": 40,
                "exp": 15 + 5 * self.bots_lvl,
                "type": 'essence'}
        self.essences.append(info)

    def being_step(self, ind):
        x, y = self.essences[ind]["location"]
        step = []
        for i in range(max(0, x - 3), min(x + 4, 99)):
            for j in range(max(0, y - 3), min(y + 4, 99)):
                st = True
                for es in self.essences:
                    if es["location"] == (i, j):
                        st = False
                        if es["type"] == "hero":
                            es["health"] -= self.essences[ind]["damage"]

                if st:
                    step.append(tuple([i, j]))
        if step:
            self.essences[ind]["location"] = random.choice(step)

    def generate_essence_code(self):
        A = list(map(lambda x: x["code"], self.essences))
        if self.essences == []:
            return 0
        A = min(list(set([i for i in range(max(A) + 2)]) - set(A)))
        return A

    def server_step(self):
        for i in range(self.len_essecses - len(self.essences)):
            self.generate_new_being('Being1')
        for ind, i in enumerate(self.essences):
            if i["type"] == "essence":
                self.being_step(ind)

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
        self.whose_move = self.whose_move % self.listener

    def new_client(self, sock):
        self.generate_new_hero('Hero1')
        self.send_msg(str(self.essences[-1]["code"]), sock)
        self.send_msg(str(self.listener is None), sock)
        self.send_msg(str([self.essences, False]), sock)

    def setting(self, sock):
        self.listener = int(self.recv_msg(sock).decode('utf-8'))

    def start(self):
        sock_producer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_producer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_producer.bind((self.ip, 5000))
        sock_producer.listen(self.players)
        producers = []

        clients = []
        sock_consumer_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_consumer_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                if self.end_session:
                    rlist[0].close()
                    rlist[1].close()
                    break
                self.listener = None
                self.essences.clear()
                self.end_connecting = False
            r, w, err = select.select(rlist, wlist, errlist, 1)
            for sock in r:
                if sock == sock_producer:
                    prod, addr = sock.accept()
                    producers.append(prod)
                    self.new_client(prod)
                    if self.listener is None:
                        rlist.append(prod)
                        self.setting(prod)
                        self.end_session = True
                    elif self.listener > len(rlist) - 2:
                        rlist.append(prod)
                elif sock == sock_consumer_listener:
                    cons, addr = sock.accept()
                    clients.append(cons)
                    wlist.append(cons)
                elif self.listener is not None and self.end_connecting is True:
                    change = False
                    k = True
                    try:
                        info = self.recv_msg(sock)
                        out_buffer = list(map(lambda x: eval(x.decode('utf-8')), eval(info)))
                    except:
                        out_buffer = []
                    if out_buffer != []:
                        if out_buffer[-1] in [True, False]:
                            del (rlist[rlist.index(sock)])
                            k = out_buffer[-1]
                            out_buffer = out_buffer[:-1]
                        self.essences = out_buffer
                        if self.whose_move == 0:
                            self.server_step()
                        for ind, s in enumerate(rlist[2::]):
                            if ind == self.whose_move:
                                change = True
                            mes = str([self.essences, bool(ind == self.whose_move)])
                            self.send_msg(mes, s)
                        self.whose_move = (self.whose_move + int(change) * int(k)) % max((len(rlist) - 2), 1)


server = Server(100, 8)
server.start()
