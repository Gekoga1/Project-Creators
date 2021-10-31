from game_lib import *


def handle_client(conn, addr, y_char=None):
    print(f"[NEW CONNECTION] {addr} connected.")
    print(f"threads {threading.active_count()}")

    connected = True
    if y_char is None:
        logined = False
    else:
        logined = True
        y_id = sqlite_request("""SELECT CharacterId FROM Character
                                WHERE Pickle = ?""", (y_char,))

    while connected:
        msg = receive(conn, addr)
        if msg == "!DISCONNECT":
            connected = False
            logined = False

        elif msg == "!REGISTRATION" and not logined:
            info = registration(conn, addr)
            if info:
                y_id, y_char = info[0], info[1]
                logined = True

        elif msg == "!LOGIN" and not logined:
            info = login(conn, addr)
            if info:
                y_id, y_char = info[0], info[1]
                logined = True

        elif msg == "!CREATE_ROOM" and logined:
            create_room(conn, addr, int(receive(conn, addr)), pickle.loads(a))
            break

        elif msg == "!CONNECT_ROOM" and logined:
            room_addr = connect_room(conn, addr, pickle.loads(b))
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
    for j, i in enumerate(rooms[number]):
        if j % 2 == 0:
            rooms[number].chars[j].owner = i
            geo_team.append(rooms[number].chars[j])
        else:
            rooms[number].chars[j].owner = i
            aero_team.append(rooms[number].chars[j])
    game = Game(geo_team, aero_team, rooms[number])
    game.start()

    send_room("!GAME_END", rooms[number])

    for i in rooms[number]:
        thread = threading.Thread(target=handle_client, args=(i[0], i[1], rooms[number].chars))
        thread.start()

    rooms.remove(rooms[number])


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Account""", ())))
    start()
