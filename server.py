import socket
import threading

from server_lib import *
# custom lib with some functions and another libs

HEADER = 64
PORT = 5050
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            reception_response(conn, addr, msg)

            if msg == "!DISCONNECT":
                connected = False

            elif msg == "!REGISTRATION":
                registration(conn, addr)

            elif msg == "!LOGIN":
                login(conn, addr)

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
    start()
