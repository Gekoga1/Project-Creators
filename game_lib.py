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
        self.strength, self.agility, self.intellect = stats[0], stats[1], stats[2]
        self.pyro, self.aqua, self.geo, self.aero = stats[3], stats[4], stats[5], stats[6]
        self.initiation, self.speed, self.resistance = stats[7], stats[8], stats[9]
        self.weapon, self.gear = gear[0], gear[1:]
        self.abilities = abilities
        self.state = []
        self.alive = True

    def __str__(self):
        return self.name

    def hp_check(self) -> None:
        self.hp = clamp(self.hp, self.max_hp, 0)
        if self.hp == 0:
            self.alive = False
            print('Death')

    def get_damage(self, damage: float, sender) -> None:
        if self.alive:
            self.hp -= damage
            print(f'{self} получает {damage} от {str(sender)} и остается с {self.hp}')
            self.hp_check()

    def get_heal(self, heal: float) -> None:
        if self.alive:
            self.hp += heal
            self.hp_check()

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

    def attack(self, enemy):
        if self.alive:
            damage = self.strength
            enemy.get_damage(damage, self)
            self.weapon.apply_effect(enemy)


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
        return f'яд ({self.time}, {self.stacks}/{self.max_stacks}, {self.percent})'

    # Only one Poison -> Strongest poison based on potential damage (percent * stacks * time)
    def __add__(self, other: Effect):
        if isinstance(other, self.__class__):
            if (other.percent == self.percent) and (self.time <= other.time):
                self.time = other.time
                self.max_stacks = other.max_stacks
                if self.stacks < self.max_stacks:
                    self.stacks += other.stacks
                    return False    # without replacement
            elif other < self:
                return False
            elif other > self:
                return True    # with replacement
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


class Weapon(Gear):
    def __init__(self, name, rarity, base_damage, attack_effect=None):
        super().__init__(name, rarity)
        self.base_damage = base_damage
        self.attack_effect = attack_effect

    def apply_effect(self, target: Character):
        state_classes = list(map(lambda x: x.__class__, target.state))
        effect = self.attack_effect[0](*self.attack_effect[1:])
        if self.attack_effect[0] not in state_classes:
            target.state.append(effect)
        else:
            index = state_classes.index(self.attack_effect[0])
            if target.state[index] + effect:
                target.state[index] = effect


class Game:
    def __init__(self, geo_team, aero_team):
        self.geo_team = geo_team
        self.aero_team = aero_team
        self.geo_len = len(self.geo_team)
        self.aero_len = len(self.aero_team)

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
        while self.check_teams_alive():
            self.round_start()
            for character in self.geo_team:
                character.attack(self.aero_team[randint(0, self.aero_len) - 1])
            for character in self.aero_team:
                character.attack(self.geo_team[randint(0, self.geo_len) - 1])
            self.round_end()
            input()


a = Character('Anthem', 100, 100, 0, 0, [2, 2, 2, 3, 2, 2, 3, 2, 2, 2],
              [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 4, 1, 1)), 0, 0, 0], [])
a2 = Character('Mehtna', 100, 100, 0, 0, [2, 2, 2, 3, 2, 2, 3, 2, 2, 2],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 4, 1, 1)), 0, 0, 0], [])
a3 = Character('Grusha', 500, 500, 0, 0, [1, 2, 2, 3, 2, 2, 3, 2, 2, 2],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 1, 1, 1, 1)), 0, 0, 0], [])

b = Character('Assault1', 100, 100, 0, 0, [3, 2, 2, 3, 2, 2, 3, 2, 2, 2],
              [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 2, 1, 1, 9)), 0, 0, 0], [])
b2 = Character('Assault2', 100, 100, 0, 0, [3, 2, 2, 3, 2, 2, 3, 2, 2, 2],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 3, 1, 2)), 0, 0, 0], [])
b3 = Character('Assault3', 100, 100, 0, 0, [3, 2, 2, 3, 2, 2, 3, 2, 2, 2],
               [Weapon('Sword', 'common', 2, attack_effect=(Poisoned, 3, 6, 1, 1)), 0, 0, 0], [])

game = Game([a, a2, a3], [b, b2, b3])
game.start()
