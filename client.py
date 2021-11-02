import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
from login_window import Ui_LoginWindow
from main_window import Ui_MainWindow

from client_lib import *


class Info_Weapon:
    def __init__(self, name, rarity, base_damage, type_of, attack_effect):
        self.name = name
        self.rarity = rarity
        self.base_damage = base_damage
        self.type_of = type_of
        self.attack_effect = attack_effect


class Info_Armor:
    def __init__(self, name, rarity, stats, defence, spell_defence):
        self.name = name
        self.rarity = rarity
        self.stats = stats
        self.defence = defence
        self.spell_defence = spell_defence


class Info:
    def __init__(self, lvl, name, stats, abilities, weapon, armor):
        self.lvl = lvl
        self.name = name
        self.stats = stats
        self.abilities = abilities
        self.weapon = weapon
        self.armor = armor

    def __str__(self):
        return f'{self.lvl, self.name, self.stats, self.abilities, self.weapon, self.armor}'


class Login_screen(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')

        self.Login.clicked.connect(self.login)
        self.Register.clicked.connect(self.register)

    def register(self):
        send("!REGISTRATION")
        send(';'.join([self.Name.text(), self.Password.text()]))
        answer = receive()

        if answer == "!False":
            self.ErrorLable.setText("Try another Name")
        else:
            global info
            info = pickle.loads(receive_bytes())
            main_screen()

    def login(self):
        send("!LOGIN")
        send(';'.join([self.Name.text(), self.Password.text()]))
        answer = receive()

        if answer == "!False":
            self.ErrorLable.setText("Where is no such account")
        else:
            global info
            info = pickle.loads(receive_bytes())
            main_screen()


class Main_screen(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')

        self.Create.clicked.connect(self.create_room)
        self.Connect.clicked.connect(self.connect_room)

        self.ArmorBox.currentTextChanged.connect(self.update_weapon)
        self.WeaponBox.currentTextChanged.connect(self.update_armor)

        self.StrValue.valueChanged.connect(self.change_stat)
        self.AgilityValue.valueChanged.connect(self.change_stat)
        self.IntValue.valueChanged.connect(self.change_stat)
        self.InitValue.valueChanged.connect(self.change_stat)
        self.PyroValue.valueChanged.connect(self.change_stat)
        self.AquaValue.valueChanged.connect(self.change_stat)
        self.GeoValue.valueChanged.connect(self.change_stat)
        self.AeroValue.valueChanged.connect(self.change_stat)

        self.SavePoints.clicked.connect(self.save_point)

    def create_room(self):
        send("!CREATE_ROOM")
        send(str((self.Value.value())))

    def connect_room(self):
        send("!CONNECT_ROOM")
        answer = receive()
        if answer == "!True":
            pass
        elif answer == "!False":
            self.ErrorLable.setText(receive())

    def update_info(self):
        global info
        self.Name.setText(info.name)
        self.Lvl.setText(f'lvl {info.lvl}')

        self.WeaponBox.addItem(info.weapon.name)
        self.ArmorBox.addItem(info.armor.name)

        self.Points.setText(str(info.lvl - sum(info.stats) + 7))

        self.StrValue.setValue(info.stats[0])
        self.AgilityValue.setValue(info.stats[1])
        self.IntValue.setValue(info.stats[2])
        self.InitValue.setValue(info.stats[3])
        self.PyroValue.setValue(info.stats[4])
        self.AquaValue.setValue(info.stats[5])
        self.GeoValue.setValue(info.stats[6])
        self.AeroValue.setValue(info.stats[7])

        for j, i in enumerate(info.abilities):
            self.findChild(QLabel, f"Ability{j + 1}").setText(str(i))

    def update_weapon(self):
        global info
        weapon = info.weapon

        self.WeaponView.clear()

        self.WeaponView.addItem(f"Rarity: {weapon.rarity}")
        self.WeaponView.addItem(f"Damage: {weapon.base_damage}")
        self.WeaponView.addItem(f"Type: {weapon.type_of}")
        self.WeaponView.addItem(f"Damage: {weapon.attack_effect}")

    def update_armor(self):
        global info
        armor = info.armor

        self.ArmorView.clear()

        self.ArmorView.addItem(f"Rarity: {armor.rarity}")
        self.ArmorView.addItem(f"Strength: {armor.stats[0]}")
        self.ArmorView.addItem(f"Agility: {armor.stats[1]}")
        self.ArmorView.addItem(f"Intelligence: {armor.stats[2]}")
        self.ArmorView.addItem(f"Initiative: {armor.stats[3]}")
        self.ArmorView.addItem(f"Pyro: {armor.stats[4]}")
        self.ArmorView.addItem(f"Aqua: {armor.stats[5]}")
        self.ArmorView.addItem(f"Geo: {armor.stats[6]}")
        self.ArmorView.addItem(f"Aero: {armor.stats[7]}")
        self.ArmorView.addItem(f"Defence: {armor.defence}")
        self.ArmorView.addItem(f"Spell Defence: {armor.spell_defence}")

    def change_stat(self):
        summery = sum([self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                       self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                       self.GeoValue.value(), self.AeroValue.value()])

        if info.lvl - summery + 7 < 0:
            self.sender().setValue(self.sender().value() + info.lvl - summery + 7)
            self.Points.setText("0")
        else:
            self.Points.setText(str(info.lvl - summery + 7))

    def save_point(self):
        info.name = self.Name.text()
        info.stats = [self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                      self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                      self.GeoValue.value(), self.AeroValue.value()]

        send("!SAVE_POINT")
        send_bytes(pickle.dumps(info, 3))


def handle_game():
    while True:
        receivation = receive()
        if receivation == "!GAME_END":
            print(receive())
            break
        elif receivation == "!INPUT":
            action = input(receive())
            send(action)
        else:
            print(receivation)


def main_screen():
    widget.setCurrentIndex(1)
    widget.setMinimumSize(800, 600)
    widget.widget(1).update_info()


if __name__ == '__main__':
    info = Info(1, '', [0, 0, 0, 0, 0, 0, 0, 0], [],
                Info_Weapon('', '', 0, '', None),
                Info_Armor('', '', [0, 0, 0, 0, 0, 0, 0, 0], 0, 0))
    try:
        app = QApplication(sys.argv)
        widget = QStackedWidget()
        widget.addWidget(Login_screen())
        widget.addWidget(Main_screen())
        widget.setWindowTitle("Project-Creators")
        widget.show()
        sys.exit(app.exec_())
    except SystemExit:
        send("!DISCONNECT")
