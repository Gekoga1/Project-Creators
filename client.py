from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray
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
    def __init__(self, lvl, name, stats, abilities, weapon, armor, inventory, abilities_book, image):
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
            info.image = receive_image()
            show_main_widow(self)

    def login(self):
        send("!LOGIN")
        send(';'.join([self.Name.text(), self.Password.text()]))
        answer = receive()

        if answer == "!False":
            self.ErrorLable.setText("Where is no such account")
        else:
            global info
            info = pickle.loads(receive_bytes())
            info.image = receive_image()
            show_main_widow(self)


class Main_screen(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.pixmap = b''
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')

        self.ArmorBox.currentTextChanged.connect(self.update_armor)
        self.WeaponBox.currentTextChanged.connect(self.update_weapon)

        self.Create.clicked.connect(self.create_room)
        self.Connect.clicked.connect(self.connect_room)

        self.StrValue.valueChanged.connect(self.change_stat)
        self.AgilityValue.valueChanged.connect(self.change_stat)
        self.IntValue.valueChanged.connect(self.change_stat)
        self.InitValue.valueChanged.connect(self.change_stat)
        self.PyroValue.valueChanged.connect(self.change_stat)
        self.AquaValue.valueChanged.connect(self.change_stat)
        self.GeoValue.valueChanged.connect(self.change_stat)
        self.AeroValue.valueChanged.connect(self.change_stat)

        self.Save.clicked.connect(self.save_point)

        self.SkillTree.currentItemChanged.connect(self.current_ability)
        self.Set1.clicked.connect(self.set_ability)
        self.Set2.clicked.connect(self.set_ability)
        self.Set3.clicked.connect(self.set_ability)
        self.Set4.clicked.connect(self.set_ability)
        self.Set5.clicked.connect(self.set_ability)

        self.LoadImg.clicked.connect(self.load_avatar)

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
        self.pixmap = base64.decodebytes(info.image)
        self.Name.setText(info.name)
        self.Lvl.setText(f'lvl {info.lvl}')

        self.WeaponBox.addItems(sorted(map(str, info.inventory["weapon"])))
        self.ArmorBox.addItems(sorted(map(str, info.inventory["armor"])))

        self.WeaponBox.setCurrentText(info.weapon)
        self.ArmorBox.setCurrentText(info.armor)

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

        self.SkillTree.clear()
        if info.abilities_book is not None:
            self.SkillTree.setColumnCount(len(info.abilities_book.keys()))
            self.SkillTree.setHorizontalHeaderLabels(map(lambda x: x.capitalize(), info.abilities_book.keys()))

            self.SkillTree.setRowCount(info.lvl)

            for j, i in enumerate(info.abilities_book.keys()):
                for g in info.abilities_book[i].keys():
                    for h in info.abilities_book[i][g]:
                        self.SkillTree.setItem(g - 1, j, QTableWidgetItem(h))

        pix = QPixmap()
        pix.loadFromData(QByteArray(bytearray(self.pixmap)))
        self.Avatar.setPixmap(pix)

    def update_weapon(self):
        global info
        weapon = info.inventory["weapon"][list(map(
            str, info.inventory["weapon"])).index(self.WeaponBox.currentText())]

        self.WeaponView.clear()

        self.WeaponView.addItem(f"Rarity: {weapon.rarity}")
        self.WeaponView.addItem(f"Damage: {weapon.base_damage}")
        self.WeaponView.addItem(f"Type: {weapon.type_of}")
        self.WeaponView.addItem(f"Damage: {weapon.attack_effect}")

    def update_armor(self):
        global info
        armor = info.inventory["armor"][list(map(
            str, info.inventory["armor"])).index(self.ArmorBox.currentText())]

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

        info.weapon = self.WeaponBox.currentText()
        info.armor = self.ArmorBox.currentText()
        info.image = None

        send("!SAVE_POINT")
        send_bytes(pickle.dumps(info, 3))
        send_image(base64.encodebytes(self.pixmap))

    def current_ability(self):
        item = self.SkillTree.currentItem()
        if item is not None:
            return item.text()

    def set_ability(self):
        text = self.current_ability()
        if text not in info.abilities:
            index = int(self.sender().text()[-1])
            if len(info.abilities) < index:
                info.abilities.append(text)
                self.findChild(QLabel, f'Ability{len(info.abilities)}').setText(text)
            else:
                info.abilities[index - 1] = text
                self.findChild(QLabel, f'Ability{index}').setText(text)

    def load_avatar(self):
        self.pixmap = QFileDialog.getOpenFileName(self, 'Choose image',
                                                  '', 'Image (*.jpg);;Image (*.png)')[0]
        self.Avatar.setPixmap(QPixmap(self.pixmap))

        with open(self.pixmap, 'rb') as file:
            self.pixmap = file.read()


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


def show_main_widow(this):
    this.hide()
    main_window.update_info()
    main_window.show()


if __name__ == '__main__':
    info = Info(1, '', [0, 0, 0, 0, 0, 0, 0, 0], [],
                Info_Weapon('', '', 0, '', None),
                Info_Armor('', '', [0, 0, 0, 0, 0, 0, 0, 0], 0, 0), None, None, b'')
    try:
        app = QApplication(sys.argv)
        login_window = Login_screen()
        main_window = Main_screen()
        login_window.show()
        sys.exit(app.exec_())
    except SystemExit:
        send("!DISCONNECT")
