import socket
import sqlite3
import threading
import time
from random import randint

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
uid = []
rooms = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Room:
    def __init__(self, value, members: list):
        self.value = value
        self.members = members

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        self.current = -1
        return self

    def __next__(self):
        self.current += 1
        try:
            return self.members[self.current]
        except IndexError:
            raise StopIteration

    def __str__(self):
        return f'{self.value} {self.members}'

    def remove(self, member):
        self.members.remove(member)

    def add_member(self, member):
        self.members.append(member)

    def get_members(self):
        return self.members

    def set_value(self, value):
        self.value = value

    def is_ready(self):
        return self.value == len(self.members)


def sqlite_request(request, conditions) -> list:
    con = sqlite3.connect('main_db.db')
    cur = con.cursor()
    result = cur.execute(request, conditions).fetchall()
    con.close()

    return result


def sqlite_update(request, conditions) -> None:
    con = sqlite3.connect('main_db.db')
    cur = con.cursor()
    cur.execute(request, conditions)
    con.commit()
    con.close()


def reception_response(conn, addr, msg: str) -> None:
    print(f"[{addr}] {msg}")
    conn.send("Msg received".encode(FORMAT))


def send(msg, conn, addr, count=0):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)    # msg with length of next msg
    conn.send(message)
    if conn.recv(HEADER).decode(FORMAT) == "Msg received":  # receiving test
        pass
    else:
        count += 1
        if count == 11:
            print('Something wrong with connection')
            conn.close()
        send(msg, conn, addr, count)


def receive(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        try:
            msg_length = int(msg_length)
        except ValueError:
            msg_length = 20
        msg = conn.recv(msg_length).decode(FORMAT)
        reception_response(conn, addr, msg)
        if msg == "!DISCONNECT":
            conn.close()
            raise SystemExit
        return msg


def target_input(msg, conn, addr):
    send("!INPUT", conn, addr)
    if msg is not None:
        send(msg, conn, addr)
    else:
        send('', conn, addr)
    return receive(conn, addr)


def registration(conn, addr) -> None:
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        reception_response(conn, addr, msg)
        msg = msg.split(';')

        while True:
            new_uid = randint(0, 999999999)
            if new_uid not in uid:
                break

        sqlite_update("""INSERT INTO Accounts(id, name, password)
                        VALUES(?, ?, ?)""", (new_uid, msg[0], msg[1]))

        uid.append(new_uid)


def login(conn, addr) -> None:
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        reception_response(conn, addr, msg)
        msg = msg.split(';')

        result = sqlite_request("""SELECT id FROM Accounts
                                    WHERE name = ? AND password = ?""",
                                (msg[0], msg[1]))[0]
        result = list(map(str, result))
        send(';'.join(result), conn, addr)


def create_room(conn, addr, value):
    for i in range(len(rooms)):
        if len(rooms[i]) == 0:
            rooms[i].set_value(value)
            rooms[i].append((conn, addr))
            send('Room created. Wait for other players.', conn, addr)
            return i
    rooms.append(Room(value, [(conn, addr)]))
    send('Room created. Wait for other players.', conn, addr)
    return len(rooms) - 1


def connect_room(conn, addr):
    for i in range(len(rooms)):
        if not rooms[i].is_ready():
            send_room("New player joined", rooms[i])
            rooms[i].add_member((conn, addr))
            return i
    return None


def send_room(msg, room):
    for i in room:
        send(msg, i[0], i[1])
