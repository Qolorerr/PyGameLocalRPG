import socket
import select
import random
import struct


class Server:
    def __init__(self, map_size, players):
        self.map_size = map_size
        self.players = players
        self.essences = []
        self.create_all_coord()
        self.whose_move = 1
        self.listener = None
        self.end_connecting = False

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

    def generate_new_being(self):
        pass

    def generate_essence_code(self):
        A = list(map(lambda x: x["code"], self.essences))
        if self.essences == []:
            return 0
        A = min(list(set([i for i in range(max(A) + 2)]) - set(A)))
        return A

    def generate_new_hero(self, texture):
        info = {"name": "Lox",
                "health": 100,
                "damage": 10,
                "location": list(self.generate_location()),
                "texture": texture,
                "gold": 100,
                "code": self.generate_essence_code(),
                "live": 1,
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

    def new_client(self, sock):
        self.generate_new_hero('Hero1')
        self.send_msg(str(self.essences[-1]["code"]), sock)
        self.send_msg(str(self.listener is None), sock)
        self.send_msg(str([self.essences, False]), sock)

    def setting(self, sock):
        self.listener = int(self.recv_msg(sock).decode('utf-8'))

    def start(self):
        sock_producer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_producer.bind(('127.0.0.1', 5000))
        sock_producer.listen(self.players)
        producers = []

        clients = []
        sock_consumer_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Note: different port to differentiate the clients who receive data from the one who sends messages
        sock_consumer_listener.bind(('127.0.0.1', 5001))

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
            r, w, err = select.select(rlist, wlist, errlist, 1)
            for sock in r:
                if sock == sock_producer:
                    prod, addr = sock.accept()
                    producers.append(prod)
                    self.new_client(prod)
                    if self.listener is None:
                        rlist.append(prod)
                        self.setting(prod)
                        print('NICE')
                    elif self.listener > len(rlist) - 2:
                        print("GOOOD")
                        rlist.append(prod)
                elif sock == sock_consumer_listener:
                    cons, addr = sock.accept()
                    clients.append(cons)
                    wlist.append(cons)
                elif self.listener is not None and self.listener == len(rlist) - 2:
                    change = False
                    try:
                        info = self.recv_msg(sock)
                        print(info)
                        out_buffer = list(map(lambda x: eval(x.decode('utf-8')), eval(info)))
                    except:
                        print("gg")
                        del(rlist[rlist.index(sock)])
                        out_buffer = []
                    if out_buffer != []:
                        self.essences = out_buffer
                        for ind, s in enumerate(rlist[2::]):
                            if ind == self.whose_move:
                                change = True
                            mes = str([self.essences, bool(ind == self.whose_move)])
                            self.send_msg(mes, s)
                        self.whose_move = (self.whose_move + int(change)) % (len(rlist) - 2)
                        print(self.whose_move)
                print('------listeners ==', self.listener)


server = Server(10, 8)
server.start()
