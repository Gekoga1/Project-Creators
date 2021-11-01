from game_lib import *
from collections import defaultdict


class User:
    def __init__(self, conn, addr, y_id, name, password, y_char):
        self.conn = conn
        self.addr = addr
        self.y_id = y_id
        self.name = name
        self.password = password
        self.y_char = y_char

    def get_conn(self):
        return self.conn, self.addr

    def __str__(self):
        return f'{self.name}'


def handle_client(user):
    print(f"[NEW CONNECTION] {user.addr} connected.")
    print(f"threads {threading.active_count()}")

    connected = True
    if user.y_char is None or user.y_id is None:
        logined = False
    else:
        logined = True

    while connected:
        msg = receive(user)
        if msg == "!DISCONNECT":
            connected = False
            logined = False

        elif msg == "!REGISTRATION" and not logined:
            info = registration(user)
            if info:
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                logined = True

        elif msg == "!LOGIN" and not logined:
            info = login(user)
            if info:
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                logined = True

        elif msg == "!CREATE_ROOM" and logined:
            create_room(user, int(receive(user)))
            break

        elif msg == "!CONNECT_ROOM" and logined:
            room_addr = connect_room(user)
            if room_addr is not None:
                send("!True", user)
                send('Room found.', user)
                if rooms[room_addr].is_ready():
                    thread = threading.Thread(target=handle_room, args=(room_addr,))
                    thread.start()
                    break
                else:
                    send('Waiting other players.', user)
                    break
            else:
                send("!False", user)
                send('There are no open rooms.', user)

    if not connected:
        user.conn.close()


def handle_room(number):
    try:
        print(f"threads {threading.active_count()}")
        print(f"[ROOM {number}] ready.")

        send_room('Duel starts', rooms[number])

        geo_team = []
        aero_team = []

        for j, i in enumerate(rooms[number]):
            if j % 2 == 0:
                geo_team.append(i.y_char)
            else:
                aero_team.append(i.y_char)

        game = Game(geo_team, aero_team, rooms[number])
        game.start()

        send_room("!GAME_END", rooms[number])
        send_room("Game ended", rooms[number])

        for i in rooms[number]:
            thread = threading.Thread(target=handle_client, args=(i,))
            thread.start()

        rooms.remove(rooms[number])
    except SystemExit:
        send_room("!GAME_END", rooms[number])
        send_room("Somebody left", rooms[number])

        for i in rooms[number]:
            thread = threading.Thread(target=handle_client, args=(i,))
            thread.start()

        rooms.remove(rooms[number])


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(User(conn, addr, None, None, None, None),))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Account""", ())))
    active = defaultdict(list)
    start()
