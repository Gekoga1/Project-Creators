from server_lib import *
# custom lib with some functions and another libs

from game_lib import *


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    print(f"threads {threading.active_count()}")

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
            create_room(conn, addr, int(receive(conn, addr)))
            break

        elif msg == "!CONNECT_ROOM":
            room_addr = connect_room(conn, addr)
            if room_addr is not None:
                send("!True", conn, addr)
                send('Room found.', conn, addr)
                if rooms[room_addr].is_ready():
                    thread = threading.Thread(target=handle_room, args=(room_addr,))
                    thread.start()
                    break
                else:
                    send('Waiting other players.', conn, addr)
                    break
            else:
                send("!False", conn, addr)
                send('There are no open rooms.', conn, addr)

    if not connected:
        conn.close()


def handle_room(number):
    print(f"threads {threading.active_count()}")
    print(f"[ROOM {number}] ready.")

    send_room('Duel starts', rooms[number])

    geo_team = []
    aero_team = []
    char = [a, b]
    for j, i in enumerate(rooms[number]):
        charr = char[randint(0, 1)]
        if j % 2 == 0:
            geo_team.append(charr[0](*charr[1:], owner=i))
        else:
            aero_team.append(charr[0](*charr[1:], owner=i))
    game = Game(geo_team, aero_team, rooms[number])
    game.start()

    for i in rooms[number]:
        thread = threading.Thread(target=handle_client, args=(i[0], i[1]))
        thread.start()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Accounts""", ())))
    start()
