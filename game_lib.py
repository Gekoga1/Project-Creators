from typing import Union
from random import randint


def clamp(value: float, maximum: float, minimal: float) -> float:
    if value < minimal:
        value = minimal
    elif value > maximum:
        value = maximum
    return value


class Character:
    def __init__(self, name, max_hp: float, hp: float, max_mp: float, mp: float,
                 stats: list, gear: list, abilities: list):

        self.name = name

        self.max_hp, self.hp = max_hp, hp
        self.max_mp, self.mp = max_mp, mp

        self.stats = stats

        self.strength, self.agility, self.intellect = 0, 0, 0
        self.pyro, self.aqua, self.geo, self.aero = 0, 0, 0, 0
        self.initiation = 0

        self.defence, self.spell_defence = 0, 0
        self.weapon, self.armor = gear[0], gear[1]

        self.abilities = []
        for i in abilities:
            self.abilities.append(i[0](*i[1:]))

        self.state = []

        self.update_stats()
        self.alive = True
        self.tag = None

    def __str__(self):
        return self.name

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

    def hp_check(self) -> None:
        self.hp = clamp(self.hp, self.max_hp, 0)
        if self.hp == 0:
            self.alive = False
            print('Death')

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

    def get_damage(self, damage: float, sender, type_of='true') -> bool:
        if self.alive:
            if type_of == 'true':
                self.hp -= damage
                print(f'{self} получает {damage} чистого урона от {str(sender)} и остается с {self.hp}')
                self.hp_check()
                return True
            elif type_of == 'physical':
                if self.defence > damage:
                    print(f'{self} получает {damage} физического урона от {str(sender)} и теряет {damage} брони')
                    return False
                elif self.defence == damage:
                    self.defence -= damage
                    print(f'{self} получает {damage} физического урона от {str(sender)} и теряет ВСЮ БРОНЮ')
                    return False
                elif self.defence == 0:
                    self.hp -= damage
                    print(f'{self} получает {damage} физического урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True
                elif self.defence < damage:
                    print(f'{self} получает {damage} физического урона от '
                          f'{str(sender)} и теряет ВСЮ БРОНЮ')
                    self.defence -= damage

                    damage = -self.defence
                    self.defence = 0
                    self.hp -= damage

                    print(f'{self} получает {damage} физического урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True
            elif type_of == 'special':
                if self.spell_defence > damage:
                    print(f'{self} получает {damage} особого урона от {str(sender)} '
                          f'и теряет {damage} магической защиты')
                    return False
                elif self.spell_defence == damage:
                    self.spell_defence = 0
                    print(f'{self} получает {damage} особого урона от {str(sender)} '
                          f'и теряет ВСЮ магическую ЗАЩИТУ')
                    return False
                elif self.spell_defence == 0:
                    self.hp -= damage
                    print(f'{self} получает {damage} особого урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True
                elif self.spell_defence < damage:
                    print(f'{self} получает {damage} особого урона от '
                          f'{str(sender)} и теряет ВСЮ магическую ЗАЩИТУ')

                    self.spell_defence -= damage
                    damage = -self.spell_defence
                    self.spell_defence = 0

                    self.hp -= damage
                    print(f'{self} получает {damage} особого урона от {str(sender)} и остается с {self.hp}')
                    self.hp_check()
                    return True

    def get_heal(self, heal: float) -> None:
        if self.alive:
            self.hp += heal
            self.hp_check()

    def apply_effect(self, attack_effect):
        if attack_effect is not None:
            state_classes = list(map(lambda x: x.__class__, self.state))
            effect = attack_effect[0](*attack_effect[1:])
            if attack_effect[0] not in state_classes:
                self.state.append(effect)
                print(f'{self} получает эффект {effect}')
            else:
                index = state_classes.index(attack_effect[0])
                if self.state[index] + effect:
                    print(f'{self} получает эффект {effect}')
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
                if state.time <= 0:
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

    def make_action(self, match):
        if self.alive:
            action = input('Actions: attack/ability\n').lower()
            if action == 'attack':
                print(' '.join([f'{j + 1}: {i.name}' for j, i in enumerate(match.geo_team)]))
                print(' '.join([f'{j + 4}: {i.name}' for j, i in enumerate(match.aero_team)]))
                choose = int(input()) - 1

                try:
                    self.attack(match.characters[choose])
                except IndexError:
                    print('Error action')
                    self.make_action(match)

            elif action == 'ability':
                if len(self.abilities) > 0:
                    for j, i in enumerate(self.abilities):
                        print(f'{j + 1}: {i.full_str()}')
                    choose = int(input()) - 1
                    try:
                        self.abilities[choose].usage(self, match)
                    except IndexError:
                        print('Error action')
                        self.make_action(match)

            else:
                print('Error action')
                self.make_action(match)


class Effect:
    def __init__(self, time: int, max_stacks: int, stacks: int):
        self.time = time
        self.max_stacks = max_stacks
        self.stacks = stacks

    def __add__(self, other):
        pass

    def tik(self, holder):
        pass

    def tak(self, holder):
        pass


class Poisoned(Effect):
    def __init__(self, time: int, max_stacks: int, stacks: int, percent: float):
        super().__init__(time, max_stacks, stacks)
        self.percent = percent / 100

    def __str__(self):
        return f'яд ({self.time}, {self.stacks}/{self.max_stacks}, {self.percent * 100}%)'

    # Only one Poison -> Strongest poison based on potential damage (percent * stacks * time)
    def __add__(self, other: Effect):
        if isinstance(other, self.__class__):
            if (other.percent == self.percent) and (self.time <= other.time):
                self.time = other.time
                self.max_stacks = other.max_stacks
                if self.stacks < self.max_stacks:
                    print(f'{self} усиливается на {other.stacks}')
                    self.stacks += other.stacks
                    return False  # without replacement
            elif other == self or other > self:
                return True  # with replacement
            elif other < self:
                return False
        return False

    def __eq__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.time * self.stacks) == (other.percent * other.time * other.stacks)

    def __gt__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.time * self.stacks) > (other.percent * other.time * other.stacks)

    def __lt__(self, other: Effect):
        if isinstance(other, self.__class__):
            return (self.percent * self.time * self.stacks) < (other.percent * other.time * other.stacks)

    def tak(self, holder):
        holder.get_damage(holder.max_hp * self.percent * self.stacks, self)
        self.time -= 1


class Gear:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity


class Armor(Gear):
    def __init__(self, name, rarity, stats, defence, spell_defence):
        super().__init__(name, rarity)
        self.stats = stats
        self.defence, self.spell_defence = defence, spell_defence


class Weapon(Gear):
    def __init__(self, name, rarity, base_damage, type_of='melee', attack_effect=None):
        super().__init__(name, rarity)
        self.base_damage = base_damage
        self.type_of = type_of
        self.attack_effect = attack_effect


class Ability:
    def __init__(self: str, mp_use: float, cd: int, number_of_choose: int):
        self.mp_use = mp_use

        self.cd = cd + 1
        self.now_cd = 0

        self.number_of_choose = number_of_choose

    def __str__(self):
        return 'способность'

    def choose(self, match):
        book = []
        print(' '.join([f'{j + 1}: {i.name}'
                        for j, i in enumerate(match.geo_team)]))
        print(' '.join([f'{j + 4}: {i.name}'
                        for j, i in enumerate(match.aero_team)]))
        for _ in range(self.number_of_choose):
            book.append(int(input()) - 1)
        return map(lambda x: match.characters[x], book)

    def usage(self, user, match):
        pass


class PoisonTouch(Ability):
    def __init__(self, mp_use: float, cd: int, number_of_choose: int):
        super().__init__(mp_use, cd, number_of_choose)

    def __str__(self):
        return 'Ядовитое касание'

    def full_str(self):
        return f'Ядовитое касание (стоимость: {self.mp_use} mp, ' \
               f'cd: {self.now_cd}, кол-во целей: {self.number_of_choose})'

    def usage(self, user: Character, match):
        if self.now_cd == 0 and user.use_mp(self.mp_use):
            targets = self.choose(match)

            for i in targets:
                i.get_damage(user.intellect * 0.5, self, type_of='special')
                if i.spell_defence == 0:
                    i.apply_effect((Poisoned, 2, 3, 1, 2))

            self.now_cd = self.cd
        else:
            return False


class Game:
    def __init__(self, geo_team, aero_team):
        self.geo_team = geo_team
        self.aero_team = aero_team
        self.geo_len = len(self.geo_team)
        self.aero_len = len(self.aero_team)
        self.characters = self.geo_team + self.aero_team

    def check_teams_alive(self):
        geo = (not len(list(filter(lambda x: x.alive, self.geo_team))) > 0)
        aero = (not len(list(filter(lambda x: x.alive, self.aero_team))) > 0)
        if geo and aero:
            print('both teams are dead')
            return False
        elif geo:
            print('geo team are dead')
            return False
        elif aero:
            print('aero team are dead')
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
        while self.check_teams_alive():
            for character in self.characters:
                character.cd_down(1)
            self.round_start()
            for character in sorted(self.characters, key=lambda x: x.initiation, reverse=True):
                print(f'{character} совершает действие')
                character.make_action(self)
            self.round_end()


a = Character('Anthem', 100, 100, 0, 0, [2, 2, 2, 3, 2, 2, 3, 2],
              [Weapon('Sword', 'common', 2),
               Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)], [])
a2 = Character('Mehtna', 100, 100, 0, 0, [2, 2, 2, 3, 2, 2, 3, 2],
               [Weapon('Sword', 'common', 2),
                Armor('All in one', 'rare', [1, 1, 1, 1, 1, 1, 1, 1], 5, 5)], [])
a3 = Character('Grusha', 500, 500, 0, 0, [1, 2, 2, 3, 2, 2, 3, 2],
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
               [(PoisonTouch, 15, 1, 2), (PoisonTouch, 30, 2, 3)])

game = Game([a, a2, a3], [b, b2, b3])
game.start()
