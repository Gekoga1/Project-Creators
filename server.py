import socket
import threading

import sqlite3
from random import randint

HEADER = 64
PORT = 5050
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def reception_response(conn, addr, msg):
    print(f"[{addr}] {msg}")
    conn.send("Msg received".encode(FORMAT))


def sqlite_request(request, conditions):
    con = sqlite3.connect('main_db.db')
    cur = con.cursor()
    result = cur.execute(request, conditions).fetchall()
    con.close()

    return result


def sqlite_update(request, conditions):
    con = sqlite3.connect('main_db.db')
    cur = con.cursor()
    cur.execute(request, conditions)
    con.commit()
    con.close()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            reception_response(conn, addr, msg)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == "!REGISTRATION":

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

            elif msg == "!LOGIN":

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
                    conn.send(";".join(result).encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda x: x[0], sqlite_request("""SELECT id FROM Accounts""", ())))
    print(uid)
    start()
