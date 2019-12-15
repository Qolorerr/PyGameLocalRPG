import socket
import select
import copy


def give_essences(code, location):
    info = {"health": 111,
            "damage": 111,
            "location": location,
            "texture": 1,
            "exp": 11,
            "gold": 22,
            "code": code,
            "live": 1,
            "who_killed": None}
    info = bytes(str(info), encoding='utf-8')
    essences.append(info)


essences = []
sock_producer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_producer.bind(('127.0.0.1', 5000))
sock_producer.listen(8)
producers = []

clients = []
sock_consumer_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Note: different port to differentiate the clients who receive data from the one who sends messages
sock_consumer_listener.bind(('127.0.0.1', 5001))

last_sock = [sock_producer, sock_consumer_listener]

rlist = [sock_producer, sock_consumer_listener]
wlist = []
errlist = []
intersection = []
out_buffer = []
code = 1
location = [1, 1]
while True:
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
            out_buffer = eval(sock.recv(1024).decode('utf-8'))
            if out_buffer != []:
                essences = out_buffer
                for s in rlist[2::]:
                    if s is not sock:
                        s.send(bytes(str(essences), encoding='utf-8'))
        intersection = list(set(rlist) - set(last_sock))
        last_sock = copy.copy(rlist)
        for i in intersection:
            give_essences(code, location)
            code += 1
            location = [2, 2]
            i.send(bytes(str(essences), encoding='utf-8'))
            print(True)
        print(essences)

    out_buffer = []
    for sock in w:
        if sock in clients:
            sock.send(bytes(str(out_buffer), encoding='utf-8'))