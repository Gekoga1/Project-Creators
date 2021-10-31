from typing import Union
from random import randint

import socket
import sqlite3
import threading
import time
from random import randint
import pickle


HEADER = 64
PORT = 41480
SERVER = "25.73.197.223"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
uid = []
rooms = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Room:
    def __init__(self, value, members, chars: list):
        self.value = value
        self.members = members
        self.chars = chars

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

    def add_member(self, member, char):
        self.members.append(member)
        self.chars.append(char)

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


def reception_response(conn, addr, msg: str) -> None:
    print(f"[{addr}] {msg}")
    conn.send("Msg received".encode(FORMAT))


def send(msg, conn, addr, count=0):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)    # msg with length of next msg
    conn.send(message)
    if conn.recv(HEADER).decode(FORMAT) == "Msg received":  # receiving test
        pass
    else:
        count += 1
        if count == 11:
            print('Something wrong with connection')
            conn.close()
        send(msg, conn, addr, count)


def send_bytes(msg, conn, addr, count=0):
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)  # msg with length of next msg
    conn.send(msg)
    if conn.recv(HEADER).decode(FORMAT) == "Msg received":  # receiving test
        pass
    else:
        count += 1
        if count == 11:
            print('Something wrong with connection')
            conn.close()
        send_bytes(msg, conn, addr, count)


def receive(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        try:
            msg_length = int(msg_length)
        except ValueError:
            msg_length = 20
        msg = conn.recv(msg_length).decode(FORMAT)
        reception_response(conn, addr, msg)
        if msg == "!DISCONNECT":
            conn.close()
            raise SystemExit
        return msg


def receive_bytes(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        try:
            msg_length = int(msg_length)
        except ValueError:
            msg_length = 20
        msg = conn.recv(msg_length)
        reception_response(conn, addr, 'bytes')
        if msg == "!DISCONNECT":
            conn.close()
            raise SystemExit
        return msg


def target_input(msg, conn, addr):
    send("!INPUT", conn, addr)
    if msg is not None:
        send(msg, conn, addr)
    else:
        send('', conn, addr)
    return receive(conn, addr)


def registration(conn, addr):
    msg = receive(conn, addr)
    msg = msg.split(';')

    result = sqlite_request("""SELECT id FROM Account
                                WHERE name = ?""", (msg[0],))

    if len(result) > 0:
        send("!False", conn, addr)
        return False
    else:
        while True:
            new_uid = randint(0, 999999999)
            if new_uid not in uid:
                break

        sqlite_update("""INSERT INTO Account(id, name, password, lvl)
                        VALUES(?, ?, ?, 1)""", (new_uid, msg[0], msg[1]))

        uid.append(new_uid)
        send(str(new_uid), conn, addr)

        return create_character(receive_bytes(conn, addr), new_uid)


def login(conn, addr):
    msg = receive(conn, addr)
    msg = msg.split(';')

    try:
        result = sqlite_request("""SELECT id FROM Account
                                    WHERE name = ? AND password = ?""", (msg[0], msg[1]))[0][0]
        send(str(result), conn, addr)
        y_id = result

        try:
            result = sqlite_request("""SELECT Pickle FROM Character
                                        WHERE CharacterId = ?""", (y_id,))[0][0]
            send("!True", conn, addr)
            return [y_id, result]
        except IndexError:
            send("!NO_CHAR", conn, addr)
            return create_character(receive_bytes(conn, addr), y_id)

    except IndexError:
        send("!False", conn, addr)
        return False


def create_character(y_char, y_id):
    stat = pickle.loads(y_char)
    y_char = pickle.dumps(Character(*stat))

    sqlite_update("""INSERT INTO Character(CharacterId, Pickle)
                    VALUES(?, ?)""", (y_id, y_char))
    sqlite_update("""UPDATE Account
                    SET CharacterId = ?
                    WHERE id = ?""", (y_id, y_id))

    return [y_id, y_char]


def create_room(conn, addr, value, char):
    for i in range(len(rooms)):
        if len(rooms[i]) == 0:
            rooms[i].set_value(value)
            rooms[i].add_member((conn, addr), char)
            send('Room created. Wait for other players.', conn, addr)
            return i
    rooms.append(Room(value, [(conn, addr)], [char]))
    send('Room created. Wait for other players.', conn, addr)
    return len(rooms) - 1


def connect_room(conn, addr, char):
    for i in range(len(rooms)):
        if not rooms[i].is_ready():
            send_room("New player joined", rooms[i])
            rooms[i].add_member((conn, addr), char)
            return i
    return None


def send_room(msg, room):
    for i in room:
        send(msg, i[0], i[1])


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
        self.strength, self.agility, self.intellect = stats[0], stats[1], stats[2]
        self.pyro, self.aqua, self.geo, self.aero = stats[3], stats[4], stats[5], stats[6]
        self.initiation = stats[7]
        self.defence = self.armor.defence
        self.spell_defence = self.armor.spell_defence

    def get_stats(self):
        return [self.strength, self.agility, self.intellect,
                self.pyro, self.aqua, self.geo, self.aero,
                self.initiation]

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
            send_room('Death', self.match.room)

    def mp_check(self) -> None:
        self.mp = clamp(self.mp, self.max_mp, 0)

    def lose_mp(self, lost):
        self.mp -= lost
        self.mp_check()

    def use_mp(self, lost) -> bool:
        if self.mp < lost:
            return False
        else:
            self.lose_mp(lost)
            return True

    def get_mp(self, amount):
        amount = round(amount, 2)
        self.mp += amount
        self.mp_check()

    def get_damage(self, damage: float, sender, type_of='true') -> bool:
        if self.alive:
            if type_of == 'true':
                self.hp -= damage
                send_room(f'{self} получает {damage} чистого урона от {str(sender)} и остается с {self.hp}',
                          self.match.room)
                self.hp_check()
                return True
            elif type_of == 'physical':
                if self.defence > damage:
                    send_room(f'{self} получает {damage} физического урона от {str(sender)} и теряет {damage} брони',
                              self.match.room)
                    self.defence -= damage
                    return False
                elif self.defence == damage:
                    self.defence = 0
                    send_room(f'{self} получает {damage} физического урона от {str(sender)} и теряет ВСЮ БРОНЮ',
                              self.match.room)
                    return False
                elif self.defence == 0:
                    self.hp -= damage
                    send_room(f'{self} получает {damage} физического урона от {str(sender)} и остается с {self.hp}',
                              self.match.room)
                    self.hp_check()
                    return True
                elif self.defence < damage:
                    send_room(f'{self} получает {damage} физического урона от '
                              f'{str(sender)} и теряет ВСЮ БРОНЮ', self.match.room)
                    self.defence -= damage

                    damage = -self.defence
                    self.defence = 0
                    self.hp -= damage

                    send_room(f'{self} получает {damage} физического урона от {str(sender)} и остается с {self.hp}',
                              self.match.room)
                    self.hp_check()
                    return True
            elif type_of == 'special':
                if self.spell_defence > damage:
                    send_room(f'{self} получает {damage} особого урона от {str(sender)} '
                              f'и теряет {damage} магической защиты', self.match.room)
                    self.spell_defence -= damage
                    return False
                elif self.spell_defence == damage:
                    self.spell_defence = 0
                    send_room(f'{self} получает {damage} особого урона от {str(sender)} '
                              f'и теряет ВСЮ магическую ЗАЩИТУ', self.match.room)
                    return False
                elif self.spell_defence == 0:
                    self.hp -= damage
                    send_room(f'{self} получает {damage} особого урона от {str(sender)} и остается с {self.hp}',
                              self.match.room)
                    self.hp_check()
                    return True
                elif self.spell_defence < damage:
                    send_room(f'{self} получает {damage} особого урона от '
                              f'{str(sender)} и теряет ВСЮ магическую ЗАЩИТУ', self.match.room)

                    self.spell_defence -= damage
                    damage = -self.spell_defence
                    self.spell_defence = 0

                    self.hp -= damage
                    send_room(f'{self} получает {damage} особого урона от {str(sender)} и остается с {self.hp}',
                              self.match.room)
                    self.hp_check()
                    return True

    def get_heal(self, heal: float) -> None:
        if self.alive:
            self.hp += heal
            self.hp_check()

    def apply_effect(self, attack_effect):
        if attack_effect is not None:
            state_classes = list(map(lambda z: z.__class__, self.state))
            effect = attack_effect[0](*attack_effect[1:])
            if attack_effect[0] not in state_classes:
                self.state.append(effect)
                send_room(f'{self} получает эффект {effect}', self.match.room)
            else:
                index = state_classes.index(attack_effect[0])
                if self.state[index] + effect:
                    send_room(f'{self} получает эффект {effect}', self.match.room)
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
            action = target_input('Actions: attack/ability/info\n', *self.owner).lower()
            if action == 'attack':
                send(' '.join([f'{j + 1}: {i.name}'
                               for j, i in enumerate(self.match.geo_team)]), *self.owner)
                send(' '.join([f'{j + self.match.geo_len + 1}: {i.name}'
                               for j, i in enumerate(self.match.aero_team)]), *self.owner)
                #try:
                choose = int(target_input('choose target ', *self.owner)) - 1
                self.attack(self.match.characters[choose])
                #except IndexError:
                    #send('Error action', *self.owner)
                   #self.make_action()
                #except ValueError:
                  #  send('Error action', *self.owner)
                  #  self.make_action()

            elif action == 'ability':
                if len(self.abilities) > 0:
                    for j, i in enumerate(self.abilities):
                        send(f'{j + 1}: {i.full_str()}', *self.owner)
                    try:
                        choose = int(target_input(None, *self.owner)) - 1

                        if not self.abilities[choose].usage(self, self.match):
                            send("You can't do that", *self.owner)
                            self.make_action()
                    except IndexError:
                        send('Error action', *self.owner)
                        self.make_action()
                    except ValueError:
                        send('Error action', *self.owner)
                        self.make_action()
                else:
                    send('Error action', *self.owner)
                    self.make_action()
            elif action == 'info':
                send(' '.join([f'{j + 1}: {i.name}'
                               for j, i in enumerate(self.match.geo_team)]),
                     *self.owner)
                send(' '.join([f'{j + self.match.geo_len + 1}: {i.name}'
                               for j, i in enumerate(self.match.aero_team)]), *self.owner)
                try:
                    choose = int(target_input('choose target ', *self.owner)) - 1
                    send_room(self.match.characters[choose].get_info(), self.match.room)
                    self.make_action()
                except IndexError:
                    send('Error action', *self.owner)
                    self.make_action()
                except ValueError:
                    send('Error action', *self.owner)
                    self.make_action()
            else:
                send('Error action', *self.owner)
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
                    send_room(f'{self} усиливается на {other.stacks}', self.match.room)
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

    def set_up(self, match):
        self.match = match


class Armor(Gear):
    def __init__(self, name, rarity, stats, defence, spell_defence, match=None):
        super().__init__(name, rarity, match)
        self.stats = stats
        self.defence, self.spell_defence = defence, spell_defence


class Weapon(Gear):
    def __init__(self, name, rarity, base_damage, type_of='melee', attack_effect=None, match=None):
        super().__init__(name, rarity, match)
        self.base_damage = base_damage
        self.type_of = type_of
        self.attack_effect = attack_effect

    def set_up(self, match):
        super().set_up(match)
        if self.attack_effect is not None:
            self.attack_effect = (*self.attack_effect, match)


class Ability:
    def __init__(self, mp_use: float, cd: int, number_of_choose: int, match=None, owner=None):
        self.match = match
        self.owner = owner

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
            book = []
            send(' '.join([f'{j + 1}: {i.name}'
                           for j, i in enumerate(match.geo_team)]), *self.owner)
            send(' '.join([f'{j + match.geo_len + 1}: {i.name}'
                           for j, i in enumerate(match.aero_team)]), *self.owner)
            for i in range(self.number_of_choose):
                book.append(int(target_input(f'target №{i} - ', *self.owner)) - 1)
            return [list(map(lambda z: match.characters[z], book)), book]
        except IndexError:
            send('Wrong Index', *self.owner)
        except ValueError:
            send('Input Only integer numbers', *self.owner)

    def usage(self, user, match):
        pass


class PoisonTouch(Ability):
    def __init__(self, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(mp_use, cd, number_of_choose, match)

    def __str__(self):
        return 'Ядовитое касание'

    def full_str(self):
        return f'Ядовитое касание (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, кол-во целей: {self.number_of_choose})'

    def usage(self, user, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            targets = self.choose(match)

            for i in targets[0]:
                i.get_damage(user.intellect * 0.5, self, type_of='special')
                if i.spell_defence == 0:
                    i.apply_effect((Poisoned, 2, 3, 1, 2, self.match))

            self.now_cd = self.cd

            return True
        else:
            return False


class Purify(Ability):
    def __init__(self, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(mp_use, cd, number_of_choose, match)

    def __str__(self):
        return 'Очищение'

    def full_str(self):
        return f'Очищение (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, на себя)'

    def usage(self, user, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            send_room(f'{user} очистился от {", ".join(map(str, user.state))}', self.match.room)
            user.state = []
            self.now_cd = self.cd

            return True
        else:
            return False


class Splash(Ability):
    def __init__(self, mp_use: float, cd: int, number_of_choose: int, match=None):
        super().__init__(mp_use, cd, number_of_choose, match)

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
                    j -= self.match.aero_len
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
        self.room = room
        self.geo_team = geo_team
        self.aero_team = aero_team
        self.geo_len = len(self.geo_team)
        self.aero_len = len(self.aero_team)
        self.characters = self.geo_team + self.aero_team

    def check_teams_alive(self):
        geo = (not len(list(filter(lambda z: z.alive, self.geo_team))) > 0)
        aero = (not len(list(filter(lambda z: z.alive, self.aero_team))) > 0)
        if geo and aero:
            send_room('both teams are dead', self.room)
            return False
        elif geo:
            send_room('geo team are dead', self.room)
            return False
        elif aero:
            send_room('aero team are dead', self.room)
            return False
        else:
            return True

    def round_start(self):
        for character in self.geo_team:
            character.proc_states(True)
        for character in self.aero_team:
            character.proc_states(True)

    def round_end(self):
        for character in self.geo_team:
            character.proc_states(False)
        for character in self.aero_team:
            character.proc_states(False)

    def start(self):
        for character in self.geo_team:
            character.tag = 'geo'
        for character in self.aero_team:
            character.tag = 'aero'
        for character in self.characters:
            character.update_stats()
            character.set_up(self)

        while self.check_teams_alive():
            for character in self.characters:
                character.cd_down(1)
                character.get_mp(character.intellect)
            self.round_start()
            for character in sorted(self.characters, key=lambda z: z.initiation, reverse=True):
                send_room(f'{character} совершает действие', self.room)
                character.make_action()
            self.round_end()


a = (Character, 'Anthem', 120, 120, 15, 15, [7, 5, 2, 0, 0, 0, 0, 4],
     Weapon('Sword with troll', 'legendary', 10000000 ** 0, type_of='melee'),
     Armor('ANTI MAGICK VEIL', 'epic', [5, 2, 1, 0, 0, 0, 0, 1], 5, 20),
     [(Purify, 0, 4, 0)])

b = (Character, 'Mehtna', 75, 75, 20, 20, [3, 2, 5, 3, 2, 2, 3, 7],
     Weapon('Spiky Tooth', 'uncommon', 3, type_of='magick', attack_effect=(Poisoned, 1, 1, 1, 6)),
     Armor('Spider skin', 'rare', [1, 3, 3, 0, 0, 0, 0, 2], 12, 6),
     [(PoisonTouch, 15, 0, 2), (Splash, 5, 2, 1)])

a = a[0](*a[1:])
b = b[0](*b[1:])

a = pickle.dumps(a, 3)

b = pickle.dumps(b, 3)

"""a3 = Character('Grusha', 500, 500, 0, 0, [1, 2, 2, 3, 2, 2, 3, 2],
               [Weapon('Sword', 'common', 2),
                Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)], [])

b = Character('Assault1', 100, 100, 100, 100, [3, 2, 2, 3, 2, 2, 3, 4],
              [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 2, 1, 1, 9)),
               Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)],
              [(PoisonTouch, 15, 1, 2), (PoisonTouch, 30, 2, 3)])
b2 = Character('Assault2', 100, 100, 100, 100, [3, 2, 10, 3, 2, 2, 3, 5],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 3, 1, 2)),
                Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)],
               [(PoisonTouch, 15, 1, 2), (PoisonTouch, 30, 2, 3)])
b3 = Character('Assault3', 100, 100, 100, 100, [3, 2, 2, 3, 2, 2, 3, 4],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 6, 1, 1)),
                Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)],
               [(PoisonTouch, 15, 1, 2), (PoisonTouch, 30, 2, 3)])"""
