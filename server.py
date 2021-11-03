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
        self.image = b''

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
                    self.y_char.weapon.name, self.y_char.armor.name,
                    book, ability_book)

    def unpack_info(self, info):
        self.y_char.name = info.name
        self.y_char.stats = info.stats
        self.y_char.weapon = self.inventory["weapon"][list(map(
            str, self.inventory["weapon"])).index(info.weapon)]
        self.y_char.armor = self.inventory["armor"][list(map(
            str, self.inventory["armor"])).index(info.armor)]
        self.unpack_abilities(info)
        self.image = info.image

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

    def unpack_abilities(self, info):
        book = []
        for i in info.abilities:
            sql = sqlite_request("""SELECT Lvl, Pickle FROM Ability
                                    WHERE Name = ?""", (i,))[0]
            if sql[0] > self.lvl:
                self.conn.close()
                raise SystemExit
            else:
                book.append(pickle.loads(sql[1]))
        self.y_char.abilities = book

    def unpack_image(self, image):
        self.image = sqlite_request("""SELECT Pickle FROM Image
                                        WHERE ImageId = ?""", (image,))[0][0]

    def update_db(self):
        owner = self.y_char.owner
        self.y_char.owner = None
        sqlite_update("""UPDATE Character
                        SET Name = ?, Pickle = ?
                        WHERE CharacterId = ?""", (self.y_char.name, pickle.dumps(self.y_char, 3), self.y_id))
        try:
            sqlite_update("""INSERT INTO Image(Pickle)
                            VALUES(?)""", (self.image,))
        except sqlite3.IntegrityError:
            pass

        sqlite_update("""UPDATE Account
                        SET ImageId = (
                        SELECT ImageId FROM Image
                        WHERE Pickle = ?)
                        WHERE id = ?""", (self.image, self.y_id))
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
    def __init__(self, lvl, name, stats, abilities, weapon, armor, inventory, abilities_book, image=None):
        self.lvl = lvl
        self.name = name
        self.stats = stats
        self.abilities = abilities
        self.weapon = weapon
        self.armor = armor
        self.inventory = inventory

        if abilities_book is not None:
            self.abilities_book = abilities_book
            for i in self.abilities_book.keys():
                for j in self.abilities_book[i].keys():
                    self.abilities_book[i][j] = list(map(str, self.abilities_book[i][j]))

        self.image = image

    def __str__(self):
        return f'{self.lvl, self.name, self.stats, self.abilities, self.weapon, self.armor},' \
               f'{self.inventory, self.abilities_book}'


def handle_client(user):
    print(f"[NEW CONNECTION] {user.addr} connected.")
    print(f"threads {threading.active_count()}")
    for thread in threading.enumerate():
        print(thread.name)

    connected = True
    if user.y_char is None or user.y_id is None:
        logined = False
    else:
        logined = True

    timer = time.time()

    while connected:
        if time.time() - timer >= 5:
            connected = False

        msg = receive(user)
        if msg == "!DISCONNECT":
            connected = False
            logined = False

        elif msg == "!REGISTRATION" and not logined:
            timer = time.time()
            info = registration(user, uid)
            if info:
                uid.append(info[0])
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                user.unpack_inventory()
                user.unpack_image(1)
                send_bytes(pickle.dumps(user.get_info(), 3), user)
                send_image(user.image, user)
                logined = True

        elif msg == "!LOGIN" and not logined:
            timer = time.time()
            info = login(user)
            if info:
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                user.unpack_inventory()
                user.unpack_image(sqlite_request("""SELECT ImageId FROM Account
                                                    WHERE id = ?""", (user.y_id,))[0][0])
                send_bytes(pickle.dumps(user.get_info(), 3), user)
                send_image(user.image, user)
                logined = True

        elif msg == "!CREATE_ROOM" and logined:
            create_room(user, int(receive(user)))
            break

        elif msg == "!CONNECT_ROOM" and logined:
            timer = time.time()
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
            timer = time.time()
            user.unpack_info(pickle.loads(receive_bytes(user)))
            user.image = receive_image(user)
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
    thread = threading.Thread(target=cmd_control)
    thread.start()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(User(conn, addr, None, None, None, None, 1),))
        thread.start()


def cmd_control():
    while True:
        try:
            exec(input())
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Account""", ())))
    ability_book = update_abilities()
    start()
