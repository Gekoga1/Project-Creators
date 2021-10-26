import sqlite3
from random import randint

HEADER = 64
PORT = 5050
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
uid = []


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
        conn.send(";".join(result).encode(FORMAT))
