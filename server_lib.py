import socket
import sqlite3
import threading
import time
from random import randint

HEADER = 64
PORT = 5050
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
uid = []
rooms = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


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
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        reception_response(conn, addr, msg)
        return msg


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


def create_room(conn, addr):
    for i in range(len(rooms)):
        if len(rooms[i]) == 0:
            rooms[i].append((conn, addr))
            send('Room created. Wait for second player.', conn, addr)
            return i
    rooms.append([(conn, addr)])
    send('Room created. Wait for second player.', conn, addr)
    return len(rooms) - 1


def connect_room(conn, addr):
    for i in range(len(rooms)):
        if len(rooms[i]) == 1:
            rooms[i].append((conn, addr))
            send('Room found. Starting duel.', conn, addr)
            return i
    send('There are no open rooms.', conn, addr)
    return None


def send_room(msg, room):
    for i in room:
        send(msg, i[0], i[1])
    print(msg)
