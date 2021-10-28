from server_lib import *
# custom lib with some functions and another libs

from game_lib import *


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = receive(conn, addr)
        if msg == "!DISCONNECT":
            connected = False

        elif msg == "!REGISTRATION":
            registration(conn, addr)

        elif msg == "!LOGIN":
            login(conn, addr)

        elif msg == "!CREATE_ROOM":
            room_addr = create_room(conn, addr)
            break

        elif msg == "!CONNECT_ROOM":
            room_addr = connect_room(conn, addr)
            if room_addr is not None:
                thread = threading.Thread(target=handle_room, args=(room_addr,))
                thread.start()
                break

    if not connected:
        conn.close()


def handle_room(number):
    print(f"[ROOM {number}] ready.")

    send_room('Duel starts', rooms[number])

    game = Game([a], [b], rooms[number])
    game.start()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda x: x[0], sqlite_request("""SELECT id FROM Accounts""", ())))
    start()
