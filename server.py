import time

from game_lib import *


class User:
    def __init__(self, conn, addr, y_id, name, password, y_char: Character, lvl):
        self.conn = conn
        self.addr = addr
        self.y_id = y_id
        self.name = name
        self.password = password
        self.y_char = y_char
        self.lvl = lvl
        self.inventory = defaultdict(list)

    def __str__(self):
        return f'{self.name}'

    def get_conn(self):
        return self.conn, self.addr

    def get_info(self):
        book = defaultdict(list)
        for i in ["weapon", "armor"]:
            for j in self.inventory[i]:
                if i == "weapon":
                    book[i].append(Info_Weapon(*j.get_info()))
                else:
                    book[i].append(Info_Armor(*j.get_info()))

        return Info(self.lvl, self.y_char.name, self.y_char.stats,
                    list(map(str, self.y_char.abilities)),
                    self.y_char.weapon.name, self.y_char.armor.name, book)

    def unpack_info(self, info):
        self.y_char.name = info.name
        self.y_char.stats = info.stats
        self.y_char.weapon = self.inventory["weapon"][list(map(
            str, self.inventory["weapon"])).index(info.weapon)]
        self.y_char.armor = self.inventory["armor"][list(map(
            str, self.inventory["armor"])).index(info.armor)]

    def unpack_inventory(self):
        book = []
        for i in self.inventory["weapon"]:
            book.append(pickle.loads(sqlite_request("""SELECT Pickle FROM Weapon
                                                        WHERE WeaponId = ?""", (i,))[0][0]))
        self.inventory["weapon"] = book

        book = []
        for i in self.inventory["armor"]:
            book.append(pickle.loads(sqlite_request("""SELECT Pickle FROM Armor
                                                        WHERE ArmorId = ?""", (i,))[0][0]))
        self.inventory["armor"] = book

    def update_db(self):
        owner = self.y_char.owner
        self.y_char.owner = None
        sqlite_update("""UPDATE Character
                        SET Pickle = ?
                        WHERE CharacterId = ?""", (pickle.dumps(self.y_char, 3), self.y_id))
        self.y_char.owner = owner


class Info_Weapon:
    def __init__(self, name, rarity, base_damage, type_of, attack_effect):
        self.name = name
        self.rarity = rarity
        self.base_damage = base_damage
        self.type_of = type_of
        self.attack_effect = attack_effect

    def __str__(self):
        return f'{self.name}'


class Info_Armor:
    def __init__(self, name, rarity, stats, defence, spell_defence):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.defence = defence
        self.spell_defence = spell_defence

    def __str__(self):
        return f'{self.name}'


class Info:
    def __init__(self, lvl, name, stats, abilities, weapon, armor, inventory):
        self.lvl = lvl
        self.name = name
        self.stats = stats
        self.abilities = abilities
        self.weapon = weapon
        self.armor = armor
        self.inventory = inventory

    def __str__(self):
        return f'{self.lvl, self.name, self.stats, self.abilities, self.weapon, self.armor, self.inventory}'


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
                user.unpack_inventory()
                print(user.inventory)
                send_bytes(pickle.dumps(user.get_info(), 3), user)
                logined = True

        elif msg == "!LOGIN" and not logined:
            info = login(user)
            if info:
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                user.unpack_inventory()
                send_bytes(pickle.dumps(user.get_info(), 3), user)
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

        elif msg == "!SAVE_POINT":
            user.unpack_info(pickle.loads(receive_bytes(user)))
            user.update_db()

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
        thread = threading.Thread(target=handle_client, args=(User(conn, addr, None, None, None, None, 1),))
        thread.start()


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Account""", ())))
    active = defaultdict(list)
    start()
