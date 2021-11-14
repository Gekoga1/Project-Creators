import socket
import sqlite3
import threading
import time
from random import randint
import pickle
from collections import defaultdict
from math import ceil
import struct


HEADER = 64
FORMAT = 'utf-8'
rooms = []


class Room:
    def __init__(self, value, members):
        self.value = value
        self.members = members

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        self.current = -1
        return self

    def __next__(self):
        self.current += 1
        try:
            return self.members[self.current]
        except IndexError:
            raise StopIteration

    def __str__(self):
        return f'{self.value} {self.members}'

    def remove(self, member):
        self.members.remove(member)

    def add_member(self, member):
        self.members.append(member)

    def get_members(self):
        return self.members

    def set_value(self, value):
        self.value = value

    def is_ready(self):
        return self.value == len(self.members)


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


def send(msg, sock):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.conn.sendall(msg)


def receive(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(4, sock)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data

    return recvall(msglen, sock)


def recvall(n, sock):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.conn.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    if data == b"!DISCONNECT":
        print("!DISCONNECT")
        raise SystemExit
    return data


def target_action(user):
    send(b"!INPUT", user)
    send(b"!MAKE_ACTION", user)
    return receive(user)


def target_choose(msg, user, match):
    send(b"!INPUT", user)
    send(b"!CHOOSE_TARGET", user)
    send(str(msg).encode(FORMAT), user)
    targets = pickle.loads(receive(user))
    names = list(map(str, match.characters))
    targets = list(map(lambda x: names.index(x), targets))
    return targets


def registration(user, uid):
    msg = receive(user).decode(FORMAT)
    msg = msg.split(';')

    result = sqlite_request("""SELECT id FROM Account
                                WHERE name = ?""", (msg[0],))

    if len(result) > 0:
        send(b"!False", user)
        return False
    else:

        while True:
            new_uid = randint(0, 999999999)
            if new_uid not in uid:
                break

        sqlite_update("""INSERT INTO Account(id, name, password, lvl, Weapons, Armors, ImageId)
                        VALUES(?, ?, ?, 15, ?, ?, 1)""", (new_uid, msg[0], msg[1],
                                                          pickle.dumps([1, 2, 3, 4], 3), pickle.dumps([1, 2, 3], 3)))

        user.y_id = new_uid
        user.name = msg[0]
        user.lvl = 15
        user.password = msg[1]
        user.inventory["weapon"] = [1, 2, 3, 4]
        user.inventory["armor"] = [1, 2, 3]

        send(str(new_uid).encode(FORMAT), user)

        return create_character(user)


def login(user, data=False):
    if not data:
        msg = receive(user).decode(FORMAT)
        msg = msg.split(';')
    else:
        msg = data

    try:
        result = sqlite_request("""SELECT id, Lvl FROM Account
                                    WHERE name = ? AND password = ?""", (msg[0], msg[1]))[0]
        send(b"!True", user)

        y_id = result[0]
        user.lvl = result[1]

        try:
            user.name = msg[0]
            user.password = msg[1]

            result = sqlite_request("""SELECT Pickle FROM Character
                                        WHERE CharacterId = ?""", (y_id,))[0][0]

            user.y_id = y_id
            user.y_char = result

            weapon = pickle.loads(sqlite_request("""SELECT Weapons FROM Account
                                                    WHERE id = ?""", (y_id,))[0][0])
            user.inventory["weapon"] = weapon

            armor = pickle.loads(sqlite_request("""SELECT Armors FROM Account
                                                    WHERE id = ?""", (y_id,))[0][0])
            user.inventory["armor"] = armor

            return [y_id, result]
        except IndexError:

            return create_character(user)

    except IndexError:
        send(b"!False", user)
        return False


def create_character(user):
    y_char = pickle.dumps(Character(str(user.y_id), 20, 20, 10, 10, [1, 1, 1, 1, 1, 1, 1, 1], None, None, []))

    sqlite_update("""INSERT INTO Character(CharacterId, Name, Pickle)
                    VALUES(?, ?, ?)""", (user.y_id, user.y_id, y_char))
    sqlite_update("""UPDATE Account
                    SET CharacterId = ?
                    WHERE id = ?""", (user.y_id, user.y_id))

    user.y_char = y_char

    return [user.y_id, y_char]


def create_room(user, value):
    for i in range(len(rooms)):
        if len(rooms[i]) < 1:
            rooms.remove(i)
    rooms.append(Room(value, [user]))
    send(pickle.dumps([1, value], 3), user)
    return len(rooms) - 1


def connect_room(user):
    for i in range(len(rooms)):
        if len(rooms[i]) < 1:
            rooms.remove(i)
        if not rooms[i].is_ready():
            send_room("!NEW_PLAYER", rooms[i])
            send_room(str(len(rooms[i]) + 1), rooms[i])
            rooms[i].add_member(user)
            send(b"!True", user)
            send(pickle.dumps([len(rooms[i]), rooms[i].value], 3), user)
            return i
    return None


def send_room(msg, room, with_encode=True):
    for_remove = []
    if with_encode:
        msg = msg.encode(FORMAT)

    for i in room:
        try:
            send(msg, i)
        except OSError or SystemExit:
            for_remove.append(i)

    for i in for_remove:
        room.remove(i)


def get_room_info(room):
    book = defaultdict(list)
    book["aero"] = []
    book["geo"] = []
    for j, i in enumerate(room.members):
        if (j + 1) % 2 == 0:
            info = i.get_info()
            info.image = i.image
            book["geo"].append(info)
        else:
            info = i.get_info()
            info.image = i.image
            book["aero"].append(info)
    return book


def send_room_info(room, user):
    book = get_room_info(room)
    for i in book.keys():
        send(str(len(book[i])).encode(FORMAT), user)
        for j in book[i]:
            img = j.image
            j.image = None
            send(pickle.dumps(j), user)
            send(img,  user)
    return True


def update_abilities():
    abilities = {"physical": defaultdict(list), "pyro": defaultdict(list), "aqua": defaultdict(list),
                 "geo": defaultdict(list), "aero": defaultdict(list)}
    for i in abilities.keys():
        for j in sqlite_request("""SELECT Lvl, Pickle FROM Ability
                                    WHERE Type = ?""", (i,)):
            abilities[i][j[0]].append(pickle.loads(j[1]))
    return abilities


def clamp(value: float, maximum: float, minimal: float) -> float:
    if value < minimal:
        value = minimal
    elif value > maximum:
        value = maximum
    return value


class Character:
    def __init__(self, name, max_hp: float, hp: float, max_mp: float, mp: float,
                 stats: list, weapon, armor, abilities: list, owner=None):
        self.owner = owner

        self.name = name

        self.max_hp, self.hp = max_hp, hp
        self.max_mp, self.mp = max_mp, mp

        self.stats = stats

        self.strength, self.agility, self.intellect = 0, 0, 0
        self.pyro, self.aqua, self.geo, self.aero = 0, 0, 0, 0
        self.initiation = 0

        self.defence, self.spell_defence = 0, 0

        if weapon is not None:
            self.weapon = weapon
        else:
            self.weapon = Weapon('', '', 0, )
        if armor is not None:
            self.armor = armor
        else:
            self.armor = Armor('', '', [0, 0, 0, 0, 0, 0, 0, 0], 0, 0)

        self.abilities = []
        for i in abilities:
            self.abilities.append(i[0](*i[1:]))

        self.state = []

        self.update_stats()
        self.alive = True
        self.tag = None
        self.match = None

    def __str__(self):
        return f'{self.name}'

    def set_up(self, match):
        self.match = match
        for j in range(len(self.abilities)):
            self.abilities[j].set_up(match, self.owner)
        self.weapon.set_up(match)
        self.armor.set_up(match)

    def update_stats(self):
        stats = [i + j for i, j in zip(self.stats, self.armor.stats)]
        self.strength, self.agility, self.intellect, self.initiation = stats[0], stats[1], stats[2], stats[3]
        self.pyro, self.aqua, self.geo, self.aero = stats[4], stats[5], stats[6], stats[7]
        self.defence = self.armor.defence
        self.spell_defence = self.armor.spell_defence

    def get_stats(self):
        return [self.strength, self.agility, self.intellect, self.initiation,
                self.pyro, self.aqua, self.geo, self.aero]

    def get_info(self):
        return f'hp: {self.hp}/{self.max_hp}\n' \
               f'mp: {self.mp}/{self.max_mp}\n' \
               f'defence: {self.defence} | spell defence: {self.spell_defence}\n' \
               f'stats: str={self.strength} | agl={self.agility} | int={self.intellect} | ' \
               f'initiation={self.initiation}\n' \
               f'states: {" ".join(map(str, self.state))}'

    def hp_check(self) -> None:
        self.hp = clamp(self.hp, self.max_hp, 0)
        if self.hp == 0:
            self.alive = False
            self.match.send_room(f'{self.name.capitalize()} is dead')

    def mp_check(self) -> None:
        self.mp = clamp(self.mp, self.max_mp, 0)

    def lose_mp(self, lost):
        lost = round(lost, 3)
        self.mp -= lost
        self.mp_check()

    def use_mp(self, lost) -> bool:
        lost = round(lost, 3)
        if self.mp < lost:
            return False
        else:
            self.lose_mp(lost)
            return True

    def get_mp(self, amount):
        amount = round(amount, 3)
        self.mp += amount
        self.mp_check()

    def get_damage(self, damage: float, sender, type_of='true') -> bool:
        if self.alive:
            damage = round(damage, 3)
            if type_of == 'true':
                self.hp -= damage
                self.match.send_room(f'{self} получает {damage}'
                                     f' чистого урона от {str(sender)} и остается с {self.hp}')
                self.hp_check()
                return True
            elif type_of == 'physical':
                if self.defence > damage:
                    self.match.send_room(f'{self} получает {damage}'
                                         f' физического урона от {str(sender)} и теряет {damage} брони')
                    self.defence -= damage
                    return False
                elif self.defence == damage:
                    self.defence = 0
                    self.match.send_room(f'{self} получает {damage}'
                                         f' физического урона от {str(sender)} и теряет ВСЮ БРОНЮ')
                    return False
                elif self.defence == 0:
                    self.hp -= damage
                    self.match.send_room(f'{self} получает {damage}'
                                         f' физического урона от {str(sender)} и остается с {self.hp}')
                    return True
                elif self.defence < damage:
                    self.match.send_room(f'{self} получает {damage} физического урона от '
                                         f'{str(sender)} и теряет ВСЮ БРОНЮ')
                    self.defence -= damage

                    damage = -self.defence
                    self.defence = 0
                    self.hp -= damage

                    self.match.send_room(f'{self} получает {damage}'
                                         f'физического урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True
            elif type_of == 'special':
                if self.spell_defence > damage:
                    self.match.send_room(f'{self} получает {damage} особого урона от {str(sender)} '
                                         f'и теряет {damage} магической защиты')
                    self.spell_defence -= damage
                    return False
                elif self.spell_defence == damage:
                    self.spell_defence = 0
                    self.match.send_room(f'{self} получает {damage} особого урона от {str(sender)} '
                                         f'и теряет ВСЮ магическую ЗАЩИТУ')
                    return False
                elif self.spell_defence == 0:
                    self.hp -= damage
                    self.match.send_room(f'{self} получает {damage}'
                                         f' особого урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True
                elif self.spell_defence < damage:
                    self.match.send_room(f'{self} получает {damage} особого урона от '
                                         f'{str(sender)} и теряет ВСЮ магическую ЗАЩИТУ')

                    self.spell_defence -= damage
                    damage = -self.spell_defence
                    self.spell_defence = 0

                    self.hp -= damage
                    self.match.send_room(f'{self} получает {damage}'
                                         f' особого урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True

    def get_heal(self, heal: float) -> None:
        heal = round(heal, 3)
        if self.alive:
            self.hp += heal
            self.hp_check()

    def apply_effect(self, attack_effect):
        if attack_effect is not None:
            state_classes = list(map(lambda z: z.__class__, self.state))
            effect = attack_effect
            if attack_effect not in state_classes:
                self.state.append(effect)
                self.match.send_room(f'{self} получает эффект {effect}')
            else:
                index = state_classes.index(attack_effect[0])
                if self.state[index] + effect:
                    self.match.send_room(f'{self} получает эффект {effect}')
                    self.state[index] = effect

    def proc_states(self, tik):
        if self.alive:
            if tik:
                for state in self.state:
                    state.tik(self)
            else:
                for state in self.state:
                    state.tak(self)
            for state in self.state:
                if state.duration <= 0:
                    self.state.remove(state)

    def cd_down(self, count):
        for i in self.abilities:
            i.now_cd -= count
            i.now_cd = clamp(i.now_cd, 100, 0)

    def attack(self, enemy):
        if self.alive:
            if self.weapon.type_of == 'melee':
                damage = self.strength + self.weapon.base_damage + self.agility * 0.4
                if enemy.get_damage(damage, self, type_of='physical'):
                    enemy.apply_effect(self.weapon.attack_effect)
            elif self.weapon.type_of == 'range':
                damage = self.agility + self.weapon.base_damage + self.strength * 0.4
                if enemy.get_damage(damage, self, type_of='physical'):
                    enemy.apply_effect(self.weapon.attack_effect)
            elif self.weapon.type_of == 'magick':
                damage = self.intellect + self.weapon.base_damage + (self.max_mp - self.mp) * 0.4
                if enemy.get_damage(damage, self, type_of='special'):
                    enemy.apply_effect(self.weapon.attack_effect)

    def make_action(self):
        if self.alive:
            action = target_action(self.owner).lower()
            if action == b'attack':
                send(b"!Action", self.owner)
                try:
                    choose = target_choose(1, self.owner, self.match)[0]
                    self.attack(self.match.characters[choose])
                    self.match.send_room(f"{str(self).capitalize()} оканчивает ход", with_update=True)
                except IndexError:
                    send(b"!ERROR", self.owner)
                    send(b'Error action', self.owner)
                    self.make_action()
                except ValueError:
                    send(b"!ERROR", self.owner)
                    send(b'Error action', self.owner)
                    self.make_action()

            elif action == b'ability':
                send(b"!Action", self.owner)
                if len(self.abilities) > 0:
                    try:
                        choose = receive(self.owner).decode(FORMAT)
                        choose = list(map(str, self.abilities)).index(choose)
                        if not self.abilities[choose].usage(self, self.match):
                            send(b"!ERROR", self.owner)
                            send(b"You can't do that", self.owner)
                            self.make_action()
                        else:
                            self.match.send_room(f"{str(self).capitalize()} оканчивает ход", with_update=True)
                    except IndexError:
                        send(b"!ERROR", self.owner)
                        send(b'Error action', self.owner)
                        self.make_action()
                    except ValueError:
                        send(b"!ERROR", self.owner)
                        send(b'Error action', self.owner)
                        self.make_action()
                else:
                    send(b"!ERROR", self.owner)
                    send(b'Error action', self.owner)
                    self.make_action()
            else:
                send(b"!ERROR", self.owner)
                self.make_action()


class Effect:
    def __init__(self, duration: int, max_stacks: int, stacks: int, match=None):
        self.duration = duration
        self.max_stacks = max_stacks
        self.stacks = stacks
        self.match = match

    def __add__(self, other):
        pass

    def tik(self, holder):
        pass

    def tak(self, holder):
        pass


class Poisoned(Effect):
    def __init__(self, duration: int, max_stacks: int, stacks: int, percent: float, match=None):
        super().__init__(duration, max_stacks, stacks, match)
        self.percent = percent / 100

    def __str__(self):
        return f'яд ({self.duration}, {self.stacks}/{self.max_stacks}, {self.percent * 100}%)'

    # Only one Poison -> Strongest poison based on potential damage (percent * stacks * duration)
    def __add__(self, other: Effect):
        if isinstance(other, self.__class__):
            if (other.percent == self.percent) and (self.duration <= other.duration):
                self.duration = other.duration
                self.max_stacks = other.max_stacks
                if self.stacks < self.max_stacks:
                    self.match.send_room(f'{self} усиливается на {other.stacks}')
                    self.stacks += other.stacks
                    return False  # without replacement
            elif other == self or other > self:
                return True  # with replacement
            elif other < self:
                return False
        return False

    def __eq__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.duration * self.stacks) == (other.percent * other.duration * other.stacks)

    def __gt__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.duration * self.stacks) > (other.percent * other.duration * other.stacks)

    def __lt__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.duration * self.stacks) < (other.percent * other.duration * other.stacks)

    def tak(self, holder):
        holder.get_damage(holder.max_hp * self.percent * self.stacks, self)
        self.duration -= 1


class Gear:
    def __init__(self, name, rarity, match=None):
        self.name = name
        self.rarity = rarity
        self.match = match

    def __str__(self):
        return self.name

    def set_up(self, match):
        self.match = match


class Armor(Gear):
    def __init__(self, name, rarity, stats, defence, spell_defence, match=None):
        super().__init__(name, rarity, match)
        self.stats = stats
        self.defence, self.spell_defence = defence, spell_defence

    def get_info(self):
        return self.name, self.rarity, self.stats, self.defence, self.spell_defence


class Weapon(Gear):
    def __init__(self, name, rarity, base_damage, type_of='melee', attack_effect=None, match=None):
        super().__init__(name, rarity, match)
        self.base_damage = base_damage
        self.type_of = type_of
        if attack_effect is not None:
            self.attack_effect = attack_effect[0](*attack_effect[1:])
        else:
            self.attack_effect = None

    def set_up(self, match):
        super().set_up(match)
        if self.attack_effect is not None:
            self.attack_effect.match = match

    def get_info(self):
        return self.name, self.rarity, self.base_damage, self.type_of, str(self.attack_effect)


class Ability:
    def __init__(self, type_of: str, mp_use: float, cd: int, number_of_choose: int, match=None, owner=None):
        self.match = match
        self.owner = owner

        self.type_of = type_of.lower()

        self.mp_use = mp_use

        self.cd = cd + 1
        self.now_cd = 0

        self.number_of_choose = number_of_choose

    def __str__(self):
        return 'способность'

    def set_up(self, match, owner):
        self.match = match
        self.owner = owner

    def choose(self, match):
        try:
            book = target_choose(self.number_of_choose, self.owner, self.match)
            return [list(map(lambda z: match.characters[z], book)), book]
        except IndexError:
            send(b"!ERROR", self.owner)
            send(b'Wrong Index', self.owner)
        except ValueError:
            send(b"!ERROR", self.owner)
            send(b'Input Only integer numbers', self.owner)

    def usage(self, user, match):
        pass


class PoisonTouch(Ability):
    def __init__(self, type_of: str, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(type_of, mp_use, cd, number_of_choose, match)

    def __str__(self):
        return 'Ядовитое касание'

    def full_str(self):
        return f'Ядовитое касание (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, кол-во целей: {self.number_of_choose})'

    def usage(self, user, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            targets = self.choose(match)

            for i in targets[0]:
                i.get_damage(user.intellect * user.geo * 0.05, self, type_of='special')
                if i.spell_defence == 0:
                    i.apply_effect((Poisoned, 2, 3, 1, 2, self.match))

            self.now_cd = self.cd

            return True
        else:
            return False


class Purify(Ability):
    def __init__(self, type_of: str, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(type_of, mp_use, cd, number_of_choose, match)

    def __str__(self):
        return 'Очищение'

    def full_str(self):
        return f'Очищение (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, на себя)'

    def usage(self, user, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            send_room(f'{user} очистился от {", ".join(map(str, user.state))}', self.match.room)
            user.state = []
            self.now_cd = self.cd - ceil(user.strength / 10)

            return True
        else:
            return False


class Splash(Ability):
    def __init__(self, type_of: str, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(type_of, mp_use, cd, number_of_choose, match)

    def __str__(self):
        return 'Рассекающий удар'

    def full_str(self):
        return f'Рассекающий удар (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, кол-во целей: {self.number_of_choose})'

    def usage(self, user, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            targets = self.choose(match)

            for i, j in zip(targets[0], targets[1]):
                user.attack(i)
                if i.tag == "geo":
                    try:
                        if j > 0:
                            user.attack(self.match.geo_team[j - 1])
                    except IndexError:
                        pass
                    try:
                        user.attack(self.match.geo_team[j + 1])
                    except IndexError:
                        pass
                elif i.tag == "aero":
                    j -= self.match.geo_len
                    try:
                        if j > 0:
                            user.attack(self.match.aero_team[j - 1])
                    except IndexError:
                        pass
                    try:
                        user.attack(self.match.aero_team[j + 1])
                    except IndexError:
                        pass

            self.now_cd = self.cd

            return True
        else:
            return False


class Game:
    def __init__(self, geo_team, aero_team, room):
        self.log = []
        self.room = room
        self.geo_team = geo_team
        self.aero_team = aero_team
        self.geo_len = len(self.geo_team)
        self.aero_len = len(self.aero_team)
        self.characters = self.geo_team + self.aero_team

    def send_room(self, msg, with_update=False):
        self.log.append(msg)
        if with_update:
            info = self.get_info()
            send_room("!LOG", self.room)
            for i in self.room.members:
                send(pickle.dumps(self.log, 3), i)
                time.sleep(0.1)
                if with_update:
                    send(pickle.dumps(info, 3), i)

    def get_info(self):
        book = []
        for i in self.characters:
            book.append([i.hp, i.max_hp, i.mp, i.max_mp, i.defence, i.spell_defence,
                         i.strength, i.agility, i.intellect, i.initiation,
                         i.pyro, i.aqua, i.geo, i.aero, list(map(str, i.state))])
        return book

    def check_teams_alive(self):
        geo = (not len(list(filter(lambda z: z.alive, self.geo_team))) > 0)
        aero = (not len(list(filter(lambda z: z.alive, self.aero_team))) > 0)
        if geo and aero:
            self.send_room('both teams are dead', with_update=True)
            return False
        elif geo:
            self.send_room('geo team are dead', with_update=True)
            return False
        elif aero:
            self.send_room('aero team are dead', with_update=True)
            return False
        else:
            return True

    def round_start(self):
        self.send_room(f"Новый раунд начинается!", with_update=True)
        for character in self.geo_team:
            character.proc_states(True)
        for character in self.aero_team:
            character.proc_states(True)

    def round_end(self):
        for character in self.geo_team:
            character.proc_states(False)
        for character in self.aero_team:
            character.proc_states(False)
        self.send_room(f"Раунд закончился!", with_update=True)
        time.sleep(1)

    def start(self):
        for character in self.geo_team:
            character.tag = 'geo'
            character.hp = character.max_hp
            character.mp = character.max_mp
        for character in self.aero_team:
            character.tag = 'aero'
            character.hp = character.max_hp
            character.mp = character.max_mp
        for character in self.characters:
            character.update_stats()
            character.set_up(self)

        while self.check_teams_alive():
            for character in self.characters:
                character.cd_down(1)
                character.get_mp(character.intellect)
            self.round_start()
            for character in sorted(self.characters, key=lambda z: z.initiation, reverse=True):
                self.send_room(f'{character} совершает действие', with_update=True)
                character.make_action()
            self.round_end()

        return [self.geo_team, self.aero_team]


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

        return Info(self.lvl, self.y_char.name, self.y_char.max_hp, self.y_char.max_mp,
                    self.y_char.max_hp, self.y_char.max_mp, self.y_char.stats,
                    list(map(str, self.y_char.abilities)),
                    Info_Weapon(*self.y_char.weapon.get_info()),
                    Info_Armor(*self.y_char.armor.get_info()),
                    book, ability_book)

    def unpack_info(self, info):
        self.y_char.name = info.name
        self.y_char.max_hp = info.max_hp
        self.y_char.max_mp = info.max_mp
        self.y_char.hp = info.max_hp
        self.y_char.mp = info.max_mp
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

    def update_base_db(self):
        sqlite_update("""UPDATE Account
                        SET Lvl = ?
                        WHERE id = ?""", (self.lvl, self.y_id))


class Info_Weapon:
    def __init__(self, name: str, rarity, base_damage, type_of, attack_effect):
        self.name = name
        self.rarity = rarity
        self.base_damage = base_damage
        self.type_of = type_of
        self.attack_effect = attack_effect

    def __str__(self):
        return f"{self.name}"

    def list_ref(self):
        return [f'Weapon: {self.rarity.capitalize()} {self.name.capitalize()} {self.type_of, self.base_damage}',
                f'                 {self.attack_effect}']


class Info_Armor:
    def __init__(self, name, rarity, stats, defence, spell_defence):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.defence = defence
        self.spell_defence = spell_defence

    def __str__(self):
        return f"{self.name}"

    def list_ref(self):
        return [f'Armor: {self.rarity.capitalize()} {self.name.capitalize()}',
                f'              def: {self.defence}, spell def:{self.spell_defence}',
                '              ' + ', '.join([f'{j}: {i}' for j, i in
                                              zip(["Str", "Agl", "Int", "Pyro", "Aqua", "Geo", "Aero", "Init"],
                                                  self.stats)])]


class Info:
    def __init__(self, lvl, name, max_hp, max_mp, hp, mp, stats,
                 abilities, weapon, armor, inventory, abilities_book, image=None):
        self.lvl = lvl
        self.name = name
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.hp = hp
        self.mp = mp
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

    def list_ref(self):
        return [*[f'{j}: {i}' for j, i in
                  zip(["Str", "Agl", "Int", "Pyro", "Aqua", "Geo", "Aero", "Init"], self.stats)]]

    def __str__(self):
        return f'{self.lvl, self.name, self.max_hp, self.max_mp} ' \
               f'{self.stats, self.abilities, self.weapon, self.armor} '\
               f'{self.inventory, self.abilities_book}'


def handle_client(user):
    print(f"[NEW CONNECTION] {user.addr} connected.")
    print(f"threads {threading.active_count()}")
    #   for thread in threading.enumerate():
    #       print(thread.name)

    connected = True

    timer = time.time()
    logined = False
    while connected:
        if time.time() - timer >= 5:
            connected = False

        msg = receive(user)
        if msg == b"!DISCONNECT":
            connected = False

        elif msg == b"!REGISTRATION" and not logined:
            timer = time.time()
            info = registration(user, uid)
            if info:
                uid.append(info[0])
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                user.unpack_inventory()
                user.unpack_image(1)
                send(pickle.dumps(user.get_info(), 3), user)
                send(user.image, user)
                logined = True

        elif msg == b"!LOGIN" and not logined:
            timer = time.time()
            info = login(user)
            if info:
                user.y_id, user.y_char = info[0], pickle.loads(info[1])
                user.y_char.owner = user
                user.unpack_inventory()
                user.unpack_image(sqlite_request("""SELECT ImageId FROM Account
                                                    WHERE id = ?""", (user.y_id,))[0][0])
                send(pickle.dumps(user.get_info(), 3), user)
                send(user.image, user)
                logined = True

        elif msg == b"!CREATE_ROOM" and logined:
            create_room(user, int(receive(user).decode(FORMAT)))
            break

        elif msg == b"!CONNECT_ROOM" and logined:
            timer = time.time()
            room_addr = connect_room(user)
            if room_addr is not None:
                if rooms[room_addr].is_ready():
                    thread = threading.Thread(target=handle_room, args=(room_addr,))
                    thread.start()
                    break
                else:
                    break
            else:
                send(b"!False", user)
                send(b"There are no open rooms", user)

        elif msg == b"!SAVE_POINT":
            timer = time.time()
            user.unpack_info(pickle.loads(receive(user)))
            user.image = receive(user)
            user.update_db()

    if not connected:
        user.conn.close()


def handle_room(number):
    try:
        print(f"threads {threading.active_count()}")
        print(f"[ROOM {number}] ready.")
        send_room("!START",  rooms[number])

        for i in rooms[number].members:
            send_room_info(rooms[number], i)

        geo_team = []
        aero_team = []

        for j, i in enumerate(rooms[number]):
            if (j + 1) % 2 == 0:
                aero_team.append(i.y_char)
            else:
                geo_team.append(i.y_char)

        game = Game(geo_team, aero_team, rooms[number])
        teams = game.start()

        geo = (not len(list(filter(lambda z: z.alive, teams[0]))) > 0)
        aero = (not len(list(filter(lambda z: z.alive, teams[1]))) > 0)
        if geo and aero:
            for i in teams[0]:
                i.owner.lvl += 1
            for i in teams[1]:
                i.owner.lvl += 1
        elif geo:
            for i in teams[1]:
                i.owner.lvl += 1
        elif aero:
            for i in teams[0]:
                i.owner.lvl += 1

        for i in rooms[number]:
            i.update_base_db()
            send(b"!GAME_END", i)

        rooms.remove(rooms[number])
    except SystemExit:
        send_room("!GAME_END", rooms[number])
        send_room("Somebody left", rooms[number])

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
    PORT = 5050

    try:
        SERVER = input("Input your Ip.v4 (or enter 1 for auto ip): ")

        if SERVER == "1":
            SERVER = socket.gethostbyname(socket.gethostname())

        ADDR = (SERVER, PORT)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
    except ValueError:
        SERVER = socket.gethostbyname(socket.gethostname())

        ADDR = (SERVER, PORT)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)

    print("[STARTING] server is starting...")
    uid = list(map(lambda qz: qz[0], sqlite_request("""SELECT id FROM Account""", ())))
    ability_book = update_abilities()
    start()
