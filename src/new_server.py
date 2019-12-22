import socket
import select
import copy
import random


class Server:
    def __init__(self, map_size, players):
        self.map_size = map_size
        self.players = players
        self.essences = []
        self.create_all_coord()
        self.whose_move = 0

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

    def start(self):
        sock_producer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_producer.bind(('127.0.0.1', 5000))
        sock_producer.listen(self.players)
        producers = []

        clients = []
        sock_consumer_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Note: different port to differentiate the clients who receive data from the one who sends messages
        sock_consumer_listener.bind(('127.0.0.1', 5001))

        last_sock = [sock_producer, sock_consumer_listener]

        rlist = [sock_producer, sock_consumer_listener]
        wlist = []
        errlist = []
        while True:
            if len(rlist) <= 2:
                self.essences.clear()
            r, w, err = select.select(rlist, wlist, errlist)
            for sock in r:
                if sock == sock_producer:
                    prod, addr = sock.accept()
                    producers.append(prod)
                    rlist.append(prod)
                elif sock == sock_consumer_listener:
                    cons, addr = sock.accept()
                    clients.append(cons)
                    wlist.append(cons)
                else:
                    print('Normal working')
                    change = False
                    try:
                        out_buffer = list(map(lambda x: eval(x.decode('utf-8')), eval(sock.recv(10240).decode('utf-8'))))
                    except:
                        del(rlist[rlist.index(sock)])
                        out_buffer = []
                    if out_buffer != []:
                        self.essences = out_buffer
                        for ind, s in enumerate(rlist[2::]):
                            if s is not sock:
                                if ind == self.whose_move:
                                    change = True
                                mes = str([self.essences, bool(ind == self.whose_move)])
                                s.send(bytes(mes, encoding='utf-8'))
                        self.whose_move = (self.whose_move + int(change)) % (len(rlist) - 2)

                intersection = list(set(rlist) - set(last_sock))
                last_sock = copy.copy(rlist)
                for i in intersection:
                    self.generate_new_hero('Hero1')
                    i.send(bytes(str(self.essences[-1]["code"]), encoding='utf-8'))
                    i.send(bytes(str([self.essences, False]), encoding='utf-8'))


server = Server(10, 8)
server.start()