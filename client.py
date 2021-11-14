from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, QThread, pyqtSignal, QObject
import socket
import pickle
import sys
import base64
from collections import defaultdict
import struct


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(200, 200)
        LoginWindow.setMinimumSize(QtCore.QSize(200, 200))
        LoginWindow.setMaximumSize(QtCore.QSize(200, 200))
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 182, 146))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ErrorLable = QtWidgets.QLabel(self.widget)
        self.ErrorLable.setMinimumSize(QtCore.QSize(180, 24))
        self.ErrorLable.setMaximumSize(QtCore.QSize(180, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ErrorLable.setFont(font)
        self.ErrorLable.setText("")
        self.ErrorLable.setAlignment(QtCore.Qt.AlignCenter)
        self.ErrorLable.setObjectName("ErrorLable")
        self.verticalLayout.addWidget(self.ErrorLable)
        self.Name = QtWidgets.QLineEdit(self.widget)
        self.Name.setMinimumSize(QtCore.QSize(180, 24))
        self.Name.setMaximumSize(QtCore.QSize(180, 24))
        self.Name.setObjectName("Name")
        self.verticalLayout.addWidget(self.Name)
        self.Password = QtWidgets.QLineEdit(self.widget)
        self.Password.setMinimumSize(QtCore.QSize(180, 24))
        self.Password.setMaximumSize(QtCore.QSize(180, 24))
        self.Password.setObjectName("Password")
        self.verticalLayout.addWidget(self.Password)
        self.Login = QtWidgets.QPushButton(self.widget)
        self.Login.setMinimumSize(QtCore.QSize(180, 24))
        self.Login.setMaximumSize(QtCore.QSize(180, 24))
        self.Login.setObjectName("Login")
        self.verticalLayout.addWidget(self.Login)
        self.Register = QtWidgets.QPushButton(self.widget)
        self.Register.setMinimumSize(QtCore.QSize(180, 24))
        self.Register.setMaximumSize(QtCore.QSize(180, 24))
        self.Register.setObjectName("Register")
        self.verticalLayout.addWidget(self.Register)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 200, 21))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "MainWindow"))
        self.Name.setPlaceholderText(_translate("LoginWindow", "Name"))
        self.Password.setPlaceholderText(_translate("LoginWindow", "Password"))
        self.Login.setText(_translate("LoginWindow", "Login"))
        self.Register.setText(_translate("LoginWindow", "Register"))


class Ui_Battle(object):
    def setupUi(self, Battle):
        Battle.setObjectName("Battle")
        Battle.resize(1205, 835)
        Battle.setMinimumSize(QtCore.QSize(1205, 835))
        self.centralwidget = QtWidgets.QWidget(Battle)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(24)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.geo_area = QtWidgets.QScrollArea(self.centralwidget)
        self.geo_area.setMinimumSize(QtCore.QSize(374, 750))
        self.geo_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.geo_area.setAutoFillBackground(False)
        self.geo_area.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.geo_area.setFrameShape(QtWidgets.QFrame.Box)
        self.geo_area.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.geo_area.setLineWidth(1)
        self.geo_area.setMidLineWidth(2)
        self.geo_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.geo_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.geo_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.geo_area.setWidgetResizable(True)
        self.geo_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.geo_area.setObjectName("geo_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 366, 762))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.geo_area.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.geo_area)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.aero_area = QtWidgets.QScrollArea(self.centralwidget)
        self.aero_area.setMinimumSize(QtCore.QSize(374, 750))
        self.aero_area.setAutoFillBackground(False)
        self.aero_area.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.aero_area.setFrameShape(QtWidgets.QFrame.Box)
        self.aero_area.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.aero_area.setLineWidth(1)
        self.aero_area.setMidLineWidth(2)
        self.aero_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.aero_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.aero_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.aero_area.setWidgetResizable(True)
        self.aero_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.aero_area.setObjectName("aero_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 366, 764))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.aero_area.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_5.addWidget(self.aero_area)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 50)
        self.verticalLayout_3.setSpacing(25)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Log = QtWidgets.QListWidget(self.centralwidget)
        self.Log.setMinimumSize(QtCore.QSize(200, 300))
        self.Log.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Log.setFont(font)
        self.Log.setObjectName("Log")
        self.verticalLayout_3.addWidget(self.Log)
        self.TargetList = QtWidgets.QListWidget(self.centralwidget)
        self.TargetList.setEnabled(False)
        self.TargetList.setMaximumSize(QtCore.QSize(350, 120))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.TargetList.setFont(font)
        self.TargetList.setObjectName("TargetList")
        self.verticalLayout_3.addWidget(self.TargetList)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TargetConfirm = QtWidgets.QPushButton(self.centralwidget)
        self.TargetConfirm.setEnabled(False)
        self.TargetConfirm.setMaximumSize(QtCore.QSize(173, 35))
        self.TargetConfirm.setObjectName("TargetConfirm")
        self.gridLayout_2.addWidget(self.TargetConfirm, 2, 0, 1, 1)
        self.TargetDelete = QtWidgets.QPushButton(self.centralwidget)
        self.TargetDelete.setEnabled(False)
        self.TargetDelete.setMaximumSize(QtCore.QSize(173, 35))
        self.TargetDelete.setObjectName("TargetDelete")
        self.gridLayout_2.addWidget(self.TargetDelete, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(200, 30))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Error = QtWidgets.QLabel(self.centralwidget)
        self.Error.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Error.setFont(font)
        self.Error.setText("")
        self.Error.setAlignment(QtCore.Qt.AlignCenter)
        self.Error.setObjectName("Error")
        self.verticalLayout.addWidget(self.Error)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.AbilityButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.AbilityButton1.setEnabled(False)
        self.AbilityButton1.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AbilityButton1.setObjectName("AbilityButton1")
        self.gridLayout.addWidget(self.AbilityButton1, 0, 1, 1, 1)
        self.AbilityButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.AbilityButton3.setEnabled(False)
        self.AbilityButton3.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AbilityButton3.setObjectName("AbilityButton3")
        self.gridLayout.addWidget(self.AbilityButton3, 1, 1, 1, 1)
        self.AbilityButton4 = QtWidgets.QPushButton(self.centralwidget)
        self.AbilityButton4.setEnabled(False)
        self.AbilityButton4.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AbilityButton4.setObjectName("AbilityButton4")
        self.gridLayout.addWidget(self.AbilityButton4, 2, 0, 1, 1)
        self.AbilityButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.AbilityButton2.setEnabled(False)
        self.AbilityButton2.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AbilityButton2.setObjectName("AbilityButton2")
        self.gridLayout.addWidget(self.AbilityButton2, 1, 0, 1, 1)
        self.AttackButton = QtWidgets.QPushButton(self.centralwidget)
        self.AttackButton.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AttackButton.setObjectName("AttackButton")
        self.AttackButton.setEnabled(False)
        self.gridLayout.addWidget(self.AttackButton, 0, 0, 1, 1)
        self.AbilityButton5 = QtWidgets.QPushButton(self.centralwidget)
        self.AbilityButton5.setEnabled(False)
        self.AbilityButton5.setMaximumSize(QtCore.QSize(180, 16777215))
        self.AbilityButton5.setObjectName("AbilityButton5")
        self.gridLayout.addWidget(self.AbilityButton5, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        Battle.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Battle)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1205, 21))
        self.menubar.setObjectName("menubar")
        Battle.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Battle)
        self.statusbar.setObjectName("statusbar")
        Battle.setStatusBar(self.statusbar)

        self.retranslateUi(Battle)
        QtCore.QMetaObject.connectSlotsByName(Battle)

    def retranslateUi(self, Battle):
        _translate = QtCore.QCoreApplication.translate
        Battle.setWindowTitle(_translate("Battle", "MainWindow"))
        self.TargetConfirm.setText(_translate("Battle", "Confirm"))
        self.TargetDelete.setText(_translate("Battle", "Delete"))
        self.AbilityButton1.setText(_translate("Battle", "None"))
        self.AbilityButton3.setText(_translate("Battle", "None"))
        self.AbilityButton4.setText(_translate("Battle", "None"))
        self.AbilityButton2.setText(_translate("Battle", "None"))
        self.AttackButton.setText(_translate("Battle", "Attack"))
        self.AbilityButton5.setText(_translate("Battle", "None"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 629)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Lvl = QtWidgets.QLabel(self.centralwidget)
        self.Lvl.setGeometry(QtCore.QRect(16, 10, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(False)
        font.setKerning(True)
        self.Lvl.setFont(font)
        self.Lvl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.Lvl.setObjectName("Lvl")
        self.Name = QtWidgets.QLineEdit(self.centralwidget)
        self.Name.setGeometry(QtCore.QRect(50, 20, 155, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Name.setFont(font)
        self.Name.setObjectName("Name")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(660, 50, 131, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Create = QtWidgets.QPushButton(self.layoutWidget)
        self.Create.setObjectName("Create")
        self.horizontalLayout_6.addWidget(self.Create)
        self.Value = QtWidgets.QSpinBox(self.layoutWidget)
        self.Value.setMaximumSize(QtCore.QSize(48, 20))
        self.Value.setMinimum(2)
        self.Value.setMaximum(10)
        self.Value.setObjectName("Value")
        self.horizontalLayout_6.addWidget(self.Value)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.Connect = QtWidgets.QPushButton(self.layoutWidget)
        self.Connect.setObjectName("Connect")
        self.gridLayout_4.addWidget(self.Connect, 1, 0, 1, 1)
        self.ErrorLable = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.ErrorLable.setFont(font)
        self.ErrorLable.setText("")
        self.ErrorLable.setScaledContents(False)
        self.ErrorLable.setAlignment(QtCore.Qt.AlignCenter)
        self.ErrorLable.setObjectName("ErrorLable")
        self.gridLayout_4.addWidget(self.ErrorLable, 2, 0, 1, 1)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(220, 20, 141, 251))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.WeaponView = QtWidgets.QListWidget(self.layoutWidget_2)
        self.WeaponView.setGridSize(QtCore.QSize(0, 16))
        self.WeaponView.setModelColumn(0)
        self.WeaponView.setObjectName("WeaponView")
        self.gridLayout_5.addWidget(self.WeaponView, 1, 0, 1, 1)
        self.WeaponBox = QtWidgets.QComboBox(self.layoutWidget_2)
        self.WeaponBox.setDuplicatesEnabled(False)
        self.WeaponBox.setObjectName("WeaponBox")
        self.gridLayout_5.addWidget(self.WeaponBox, 0, 0, 1, 1)
        self.ArmorView = QtWidgets.QListWidget(self.layoutWidget_2)
        self.ArmorView.setGridSize(QtCore.QSize(0, 16))
        self.ArmorView.setObjectName("ArmorView")
        self.gridLayout_5.addWidget(self.ArmorView, 3, 0, 1, 1)
        self.ArmorBox = QtWidgets.QComboBox(self.layoutWidget_2)
        self.ArmorBox.setObjectName("ArmorBox")
        self.gridLayout_5.addWidget(self.ArmorBox, 2, 0, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 22, 281, 211))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.InitLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.InitLable.setFont(font)
        self.InitLable.setObjectName("InitLable")
        self.gridLayout.addWidget(self.InitLable, 3, 0, 1, 1)
        self.AgilLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AgilLable.setFont(font)
        self.AgilLable.setObjectName("AgilLable")
        self.gridLayout.addWidget(self.AgilLable, 1, 0, 1, 1)
        self.StrLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.StrLable.setFont(font)
        self.StrLable.setObjectName("StrLable")
        self.gridLayout.addWidget(self.StrLable, 0, 0, 1, 1)
        self.StrValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.StrValue.setMinimumSize(QtCore.QSize(34, 20))
        self.StrValue.setMaximumSize(QtCore.QSize(44, 20))
        self.StrValue.setMinimum(1)
        self.StrValue.setProperty("value", 1)
        self.StrValue.setObjectName("StrValue")
        self.gridLayout.addWidget(self.StrValue, 0, 1, 1, 1)
        self.IntLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.IntLable.setFont(font)
        self.IntLable.setObjectName("IntLable")
        self.gridLayout.addWidget(self.IntLable, 2, 0, 1, 1)
        self.InitValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.InitValue.setMinimumSize(QtCore.QSize(34, 20))
        self.InitValue.setMaximumSize(QtCore.QSize(44, 20))
        self.InitValue.setMinimum(1)
        self.InitValue.setProperty("value", 1)
        self.InitValue.setObjectName("InitValue")
        self.gridLayout.addWidget(self.InitValue, 3, 1, 1, 1)
        self.IntValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.IntValue.setMinimumSize(QtCore.QSize(34, 20))
        self.IntValue.setMaximumSize(QtCore.QSize(44, 20))
        self.IntValue.setMinimum(1)
        self.IntValue.setProperty("value", 1)
        self.IntValue.setObjectName("IntValue")
        self.gridLayout.addWidget(self.IntValue, 2, 1, 1, 1)
        self.AgilityValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.AgilityValue.setMinimumSize(QtCore.QSize(34, 20))
        self.AgilityValue.setMaximumSize(QtCore.QSize(44, 20))
        self.AgilityValue.setMinimum(1)
        self.AgilityValue.setProperty("value", 1)
        self.AgilityValue.setObjectName("AgilityValue")
        self.gridLayout.addWidget(self.AgilityValue, 1, 1, 1, 1)
        self.MpLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.MpLable.setFont(font)
        self.MpLable.setObjectName("MpLable")
        self.gridLayout.addWidget(self.MpLable, 4, 0, 1, 1)
        self.MpValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.MpValue.setMinimumSize(QtCore.QSize(34, 20))
        self.MpValue.setMaximumSize(QtCore.QSize(44, 20))
        self.MpValue.setMinimum(5)
        self.MpValue.setMaximum(1000)
        self.MpValue.setSingleStep(5)
        self.MpValue.setProperty("value", 10)
        self.MpValue.setObjectName("MpValue")
        self.gridLayout.addWidget(self.MpValue, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.GeoLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.GeoLable.setFont(font)
        self.GeoLable.setObjectName("GeoLable")
        self.gridLayout_2.addWidget(self.GeoLable, 2, 0, 1, 1)
        self.AeroLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AeroLable.setFont(font)
        self.AeroLable.setObjectName("AeroLable")
        self.gridLayout_2.addWidget(self.AeroLable, 3, 0, 1, 1)
        self.PyroLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.PyroLable.setFont(font)
        self.PyroLable.setObjectName("PyroLable")
        self.gridLayout_2.addWidget(self.PyroLable, 0, 0, 1, 1)
        self.AquaLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AquaLable.setFont(font)
        self.AquaLable.setObjectName("AquaLable")
        self.gridLayout_2.addWidget(self.AquaLable, 1, 0, 1, 1)
        self.AeroValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.AeroValue.setMinimumSize(QtCore.QSize(34, 20))
        self.AeroValue.setMaximumSize(QtCore.QSize(44, 20))
        self.AeroValue.setMinimum(1)
        self.AeroValue.setProperty("value", 1)
        self.AeroValue.setObjectName("AeroValue")
        self.gridLayout_2.addWidget(self.AeroValue, 3, 1, 1, 1)
        self.AquaValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.AquaValue.setMinimumSize(QtCore.QSize(34, 20))
        self.AquaValue.setMaximumSize(QtCore.QSize(44, 20))
        self.AquaValue.setMinimum(1)
        self.AquaValue.setProperty("value", 1)
        self.AquaValue.setObjectName("AquaValue")
        self.gridLayout_2.addWidget(self.AquaValue, 1, 1, 1, 1)
        self.PyroValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.PyroValue.setMinimumSize(QtCore.QSize(34, 20))
        self.PyroValue.setMaximumSize(QtCore.QSize(44, 20))
        self.PyroValue.setMinimum(1)
        self.PyroValue.setProperty("value", 1)
        self.PyroValue.setObjectName("PyroValue")
        self.gridLayout_2.addWidget(self.PyroValue, 0, 1, 1, 1)
        self.GeoValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.GeoValue.setMinimumSize(QtCore.QSize(34, 20))
        self.GeoValue.setMaximumSize(QtCore.QSize(44, 20))
        self.GeoValue.setMinimum(1)
        self.GeoValue.setProperty("value", 1)
        self.GeoValue.setObjectName("GeoValue")
        self.gridLayout_2.addWidget(self.GeoValue, 2, 1, 1, 1)
        self.HpLable = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.HpLable.setFont(font)
        self.HpLable.setObjectName("HpLable")
        self.gridLayout_2.addWidget(self.HpLable, 4, 0, 1, 1)
        self.HpValue = QtWidgets.QSpinBox(self.layoutWidget1)
        self.HpValue.setMinimumSize(QtCore.QSize(34, 20))
        self.HpValue.setMaximumSize(QtCore.QSize(44, 20))
        self.HpValue.setMinimum(5)
        self.HpValue.setMaximum(1000)
        self.HpValue.setSingleStep(10)
        self.HpValue.setProperty("value", 10)
        self.HpValue.setObjectName("HpValue")
        self.gridLayout_2.addWidget(self.HpValue, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.LoadImg = QtWidgets.QPushButton(self.centralwidget)
        self.LoadImg.setGeometry(QtCore.QRect(50, 270, 155, 25))
        self.LoadImg.setObjectName("LoadImg")
        self.Avatar = QtWidgets.QLabel(self.centralwidget)
        self.Avatar.setGeometry(QtCore.QRect(50, 53, 155, 210))
        self.Avatar.setText("")
        self.Avatar.setPixmap(QtGui.QPixmap("../../Downloads/rick_astley_youtube_1627540038486.jpg"))
        self.Avatar.setScaledContents(True)
        self.Avatar.setObjectName("Avatar")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 310, 761, 271))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SkillTree = QtWidgets.QTableWidget(self.layoutWidget2)
        self.SkillTree.setMaximumSize(QtCore.QSize(465, 16777215))
        self.SkillTree.setObjectName("SkillTree")
        self.SkillTree.setColumnCount(0)
        self.SkillTree.setRowCount(0)
        self.horizontalLayout_5.addWidget(self.SkillTree)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.AbilityLable4 = QtWidgets.QLabel(self.layoutWidget2)
        self.AbilityLable4.setMinimumSize(QtCore.QSize(70, 20))
        self.AbilityLable4.setMaximumSize(QtCore.QSize(70, 48))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AbilityLable4.setFont(font)
        self.AbilityLable4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AbilityLable4.setObjectName("AbilityLable4")
        self.gridLayout_3.addWidget(self.AbilityLable4, 3, 1, 1, 1)
        self.AbilityLable3 = QtWidgets.QLabel(self.layoutWidget2)
        self.AbilityLable3.setMinimumSize(QtCore.QSize(70, 0))
        self.AbilityLable3.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AbilityLable3.setFont(font)
        self.AbilityLable3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AbilityLable3.setObjectName("AbilityLable3")
        self.gridLayout_3.addWidget(self.AbilityLable3, 2, 1, 1, 1)
        self.Ability5 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Ability5.setFont(font)
        self.Ability5.setObjectName("Ability5")
        self.gridLayout_3.addWidget(self.Ability5, 4, 2, 1, 1)
        self.Ability1 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Ability1.setFont(font)
        self.Ability1.setObjectName("Ability1")
        self.gridLayout_3.addWidget(self.Ability1, 0, 2, 1, 1)
        self.AbilityLable2 = QtWidgets.QLabel(self.layoutWidget2)
        self.AbilityLable2.setMinimumSize(QtCore.QSize(70, 0))
        self.AbilityLable2.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AbilityLable2.setFont(font)
        self.AbilityLable2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AbilityLable2.setObjectName("AbilityLable2")
        self.gridLayout_3.addWidget(self.AbilityLable2, 1, 1, 1, 1)
        self.Ability3 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Ability3.setFont(font)
        self.Ability3.setObjectName("Ability3")
        self.gridLayout_3.addWidget(self.Ability3, 2, 2, 1, 1)
        self.Ability4 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Ability4.setFont(font)
        self.Ability4.setObjectName("Ability4")
        self.gridLayout_3.addWidget(self.Ability4, 3, 2, 1, 1)
        self.AbilityLable5 = QtWidgets.QLabel(self.layoutWidget2)
        self.AbilityLable5.setMinimumSize(QtCore.QSize(70, 20))
        self.AbilityLable5.setMaximumSize(QtCore.QSize(70, 48))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AbilityLable5.setFont(font)
        self.AbilityLable5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AbilityLable5.setObjectName("AbilityLable5")
        self.gridLayout_3.addWidget(self.AbilityLable5, 4, 1, 1, 1)
        self.AbilityLable1 = QtWidgets.QLabel(self.layoutWidget2)
        self.AbilityLable1.setMinimumSize(QtCore.QSize(70, 0))
        self.AbilityLable1.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.AbilityLable1.setFont(font)
        self.AbilityLable1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.AbilityLable1.setObjectName("AbilityLable1")
        self.gridLayout_3.addWidget(self.AbilityLable1, 0, 1, 1, 1)
        self.Ability2 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Ability2.setFont(font)
        self.Ability2.setObjectName("Ability2")
        self.gridLayout_3.addWidget(self.Ability2, 1, 2, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Set1 = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Set1.setFont(font)
        self.Set1.setObjectName("Set1")
        self.horizontalLayout_4.addWidget(self.Set1)
        self.Set2 = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Set2.setFont(font)
        self.Set2.setObjectName("Set2")
        self.horizontalLayout_4.addWidget(self.Set2)
        self.Set3 = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Set3.setFont(font)
        self.Set3.setObjectName("Set3")
        self.horizontalLayout_4.addWidget(self.Set3)
        self.Set4 = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Set4.setFont(font)
        self.Set4.setObjectName("Set4")
        self.horizontalLayout_4.addWidget(self.Set4)
        self.Set5 = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Set5.setFont(font)
        self.Set5.setObjectName("Set5")
        self.horizontalLayout_4.addWidget(self.Set5)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        self.Save = QtWidgets.QPushButton(self.layoutWidget2)
        self.Save.setMaximumSize(QtCore.QSize(286, 36))
        self.Save.setObjectName("Save")
        self.Save.setEnabled(False)
        self.horizontalLayout_7.addWidget(self.Save)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(402, 242, 201, 31))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.InitLable_2 = QtWidgets.QLabel(self.layoutWidget3)
        self.InitLable_2.setMinimumSize(QtCore.QSize(90, 20))
        self.InitLable_2.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.InitLable_2.setFont(font)
        self.InitLable_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.InitLable_2.setObjectName("InitLable_2")
        self.horizontalLayout_2.addWidget(self.InitLable_2)
        self.Points = QtWidgets.QLineEdit(self.layoutWidget3)
        self.Points.setMinimumSize(QtCore.QSize(30, 20))
        self.Points.setMaximumSize(QtCore.QSize(80, 16777215))
        self.Points.setReadOnly(True)
        self.Points.setObjectName("Points")
        self.horizontalLayout_2.addWidget(self.Points)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Lvl.setText(_translate("MainWindow", "lvl 100"))
        self.Create.setText(_translate("MainWindow", "Create Room"))
        self.Connect.setText(_translate("MainWindow", "Connect Room"))
        self.InitLable.setText(_translate("MainWindow", "Initiative:"))
        self.AgilLable.setText(_translate("MainWindow", "Agility:"))
        self.StrLable.setText(_translate("MainWindow", "Strength:"))
        self.IntLable.setText(_translate("MainWindow", "Intelligence:"))
        self.MpLable.setText(_translate("MainWindow", "Mana:"))
        self.GeoLable.setText(_translate("MainWindow", "Geo:"))
        self.AeroLable.setText(_translate("MainWindow", "Aero:"))
        self.PyroLable.setText(_translate("MainWindow", "Pyro:"))
        self.AquaLable.setText(_translate("MainWindow", "Aqua:"))
        self.HpLable.setText(_translate("MainWindow", "Healph:"))
        self.LoadImg.setText(_translate("MainWindow", "Load (210x155)"))
        self.AbilityLable4.setText(_translate("MainWindow", "Ability №4:"))
        self.AbilityLable3.setText(_translate("MainWindow", "Ability №3:"))
        self.Ability5.setText(_translate("MainWindow", "None"))
        self.Ability1.setText(_translate("MainWindow", "None"))
        self.AbilityLable2.setText(_translate("MainWindow", "Ability №2:"))
        self.Ability3.setText(_translate("MainWindow", "None"))
        self.Ability4.setText(_translate("MainWindow", "None"))
        self.AbilityLable5.setText(_translate("MainWindow", "Ability №5:"))
        self.AbilityLable1.setText(_translate("MainWindow", "Ability №1:"))
        self.Ability2.setText(_translate("MainWindow", "None"))
        self.Set1.setText(_translate("MainWindow", "SetAbility №1"))
        self.Set2.setText(_translate("MainWindow", "SetAbility №2"))
        self.Set3.setText(_translate("MainWindow", "SetAbility №3"))
        self.Set4.setText(_translate("MainWindow", "SetAbility №4"))
        self.Set5.setText(_translate("MainWindow", "SetAbility №5"))
        self.Save.setText(_translate("MainWindow", "Save"))
        self.InitLable_2.setText(_translate("MainWindow", "Unused points:"))


class Ui_Waiting(object):
    def setupUi(self, Waiting):
        Waiting.setObjectName("Waiting")
        Waiting.resize(575, 314)
        self.centralwidget = QtWidgets.QWidget(Waiting)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 70)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Players = QtWidgets.QLabel(self.centralwidget)
        self.Players.setMaximumSize(QtCore.QSize(16777215, 20))
        self.Players.setAlignment(QtCore.Qt.AlignCenter)
        self.Players.setObjectName("Players")
        self.verticalLayout.addWidget(self.Players)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMinimum(1)
        self.progressBar.setMaximum(2)
        self.progressBar.setProperty("value", 2)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        Waiting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Waiting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 21))
        self.menubar.setObjectName("menubar")
        Waiting.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Waiting)
        self.statusbar.setObjectName("statusbar")
        Waiting.setStatusBar(self.statusbar)

        self.retranslateUi(Waiting)
        QtCore.QMetaObject.connectSlotsByName(Waiting)

    def retranslateUi(self, Waiting):
        _translate = QtCore.QCoreApplication.translate
        Waiting.setWindowTitle(_translate("Waiting", "MainWindow"))
        self.label.setText(_translate("Waiting", "Waite for other players"))
        self.Players.setText(_translate("Waiting", "TextLabel"))


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Server IP.v4: ")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    client.sendall(msg)


def receive():
    # Read message length and unpack it into an integer
    raw_msglen = recvall(4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(msglen)


def recvall(n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = client.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


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
                  zip(["Str", "Agl", "Int", "Init", "Pyro", "Aqua", "Geo", "Aero"], self.stats)]]

    def __str__(self):
        return f'{self.lvl, self.name, self.max_hp, self.max_mp} ' \
               f'{self.stats, self.abilities, self.weapon, self.armor} '\
               f'{self.inventory, self.abilities_book}'


class Login_screen(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')

        self.Login.clicked.connect(self.login)
        self.Register.clicked.connect(self.register)

    def register(self):
        send(b"!REGISTRATION")
        send(';'.join([self.Name.text(), self.Password.text()]).encode(FORMAT))
        answer = receive()

        if answer == b"!False":
            self.ErrorLable.setText("Try another Name")
        else:
            global info
            info = pickle.loads(receive())
            info.image = receive()
            show_main_widow(self)

    def login(self):
        send(b"!LOGIN")
        send(';'.join([self.Name.text(), self.Password.text()]).encode(FORMAT))
        answer = receive()

        if answer == b"!False":
            self.ErrorLable.setText("Where is no such account")
        else:
            global info
            info = pickle.loads(receive())
            info.image = receive()
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
        self.GeoValue.valueChanged.connect(self.change_stat)
        self.AeroValue.valueChanged.connect(self.change_stat)
        self.HpValue.valueChanged.connect(self.hp_mp_change)
        self.MpValue.valueChanged.connect(self.hp_mp_change)

        self.Save.clicked.connect(self.save_point)
        self.Save.setEnabled(False)

        self.SkillTree.currentItemChanged.connect(self.current_ability)
        self.Set1.clicked.connect(self.set_ability)
        self.Set2.clicked.connect(self.set_ability)
        self.Set3.clicked.connect(self.set_ability)
        self.Set4.clicked.connect(self.set_ability)
        self.Set5.clicked.connect(self.set_ability)

        self.LoadImg.clicked.connect(self.load_avatar)

    def create_room(self):
        send(b"!CREATE_ROOM")
        send(str((self.Value.value())).encode(FORMAT))
        show_waiting_widow(self)

    def connect_room(self):
        send(b"!CONNECT_ROOM")
        answer = receive()
        if answer == b"!True":
            show_waiting_widow(self)
        elif answer == b"!False":
            self.ErrorLable.setText(receive().decode(FORMAT))

    def update_info(self):
        global info
        self.pixmap = base64.decodebytes(info.image)
        self.Name.setText(info.name)
        self.Lvl.setText(f'lvl {info.lvl}')

        self.WeaponBox.addItems(sorted(map(str, info.inventory["weapon"])))
        self.ArmorBox.addItems(sorted(map(str, info.inventory["armor"])))

        self.WeaponBox.setCurrentText(info.weapon.name)
        self.ArmorBox.setCurrentText(info.armor.name)

        self.StrValue.setValue(info.stats[0])
        self.AgilityValue.setValue(info.stats[1])
        self.IntValue.setValue(info.stats[2])
        self.InitValue.setValue(info.stats[3])
        self.PyroValue.setValue(info.stats[4])
        self.AquaValue.setValue(info.stats[5])
        self.GeoValue.setValue(info.stats[6])
        self.AeroValue.setValue(info.stats[7])
        self.HpValue.setValue(info.max_hp)
        self.MpValue.setValue(info.max_mp)

        summery = sum([self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                       self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                       self.GeoValue.value(), self.AeroValue.value(),
                       self.MpValue.value() // 5, self.HpValue.value() // 10])

        self.Points.setText(str(info.lvl - summery + 13))

        for j, i in enumerate(info.abilities):
            self.findChild(QLabel, f"Ability{j + 1}").setText(str(i))

        self.SkillTree.clear()
        if info.abilities_book is not None:
            self.SkillTree.setColumnCount(len(info.abilities_book.keys()))
            self.SkillTree.setHorizontalHeaderLabels(map(lambda x: x.capitalize(), info.abilities_book.keys()))

            self.SkillTree.setRowCount(info.lvl)

            for i in range(self.SkillTree.columnCount()):
                for j in range(self.SkillTree.rowCount()):
                    item = QTableWidgetItem("")
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.SkillTree.setItem(j, i, item)

            for j, i in enumerate(info.abilities_book.keys()):
                for g in info.abilities_book[i].keys():
                    for h in info.abilities_book[i][g]:
                        item = QTableWidgetItem(h)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.SkillTree.setItem(g - 1, j, item)

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

        self.Save.setEnabled(True)

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

        self.Save.setEnabled(True)

    def change_stat(self):
        summery = sum([self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                       self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                       self.GeoValue.value(), self.AeroValue.value(),
                       self.MpValue.value() // 5, self.HpValue.value() // 10])

        if info.lvl - summery + 13 < 0:
            self.sender().setValue(self.sender().value() + info.lvl - summery + 13)
            self.Points.setText("0")
        else:
            self.Points.setText(str(info.lvl - summery + 13))

        self.Save.setEnabled(True)

    def hp_mp_change(self):
        if self.sender().objectName() == "MpValue":
            if self.sender().value() % 5 == 0:
                summery = sum([self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                               self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                               self.GeoValue.value(), self.AeroValue.value(),
                               self.MpValue.value() // 5, self.HpValue.value() // 10])

                if info.lvl - summery + 13 < 0:
                    self.sender().setValue(self.sender().value() + info.lvl - summery + 13)
                    self.Points.setText("0")
                else:
                    self.Points.setText(str(info.lvl - summery + 13))
            else:
                self.sender().setValue((self.sender().value() // 5) * 5)
        else:
            if self.sender().value() % 10 == 0:
                summery = sum([self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                               self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                               self.GeoValue.value(), self.AeroValue.value(),
                               self.MpValue.value() // 5, self.HpValue.value() // 10])

                if info.lvl - summery + 13 < 0:
                    self.sender().setValue(self.sender().value() + info.lvl - summery + 13)
                    self.Points.setText("0")
                else:
                    self.Points.setText(str(info.lvl - summery + 13))
            else:
                self.sender().setValue((self.sender().value() // 10) * 10)

        self.Save.setEnabled(True)

    def save_point(self):
        info.name = self.Name.text()
        info.max_hp = self.HpValue.value()
        info.max_mp = self.MpValue.value()
        info.stats = [self.StrValue.value(), self.AgilityValue.value(), self.IntValue.value(),
                      self.InitValue.value(), self.PyroValue.value(), self.AquaValue.value(),
                      self.GeoValue.value(), self.AeroValue.value()]

        info.weapon = self.WeaponBox.currentText()
        info.armor = self.ArmorBox.currentText()
        info.image = None

        send(b"!SAVE_POINT")
        send(pickle.dumps(info, 3))
        send(base64.encodebytes(self.pixmap))
        info.image = self.pixmap

        self.Save.setEnabled(False)

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

            self.Save.setEnabled(True)

    def load_avatar(self):
        self.pixmap = QFileDialog.getOpenFileName(self, 'Choose image',
                                                  '', 'Image (*.jpg);;Image (*.png)')[0]
        self.Avatar.setPixmap(QPixmap(self.pixmap))

        with open(self.pixmap, 'rb') as file:
            self.pixmap = file.read()

            self.Save.setEnabled(True)


class UpdateThread(QObject):
    new_data = pyqtSignal(int)
    game_start = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    # noinspection PyUnresolvedReferences
    def run(self):
        while True:
            rec = receive()
            if rec == b"!NEW_PLAYER":
                self.new_data.emit(int(receive().decode(FORMAT)))
            elif rec == b"!START":
                self.game_start.emit()
                break


class Waiting_screen(QMainWindow, Ui_Waiting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')
        self.thread = QThread()
        self.update = UpdateThread()

    # noinspection PyUnresolvedReferences
    def update_info(self, players, value):
        self.Players.setText(f"{players}/{value}")
        self.progressBar.setMaximum(value)
        self.progressBar.setValue(players)

        self.update.moveToThread(self.thread)
        self.update.game_start.connect(self.start)
        self.thread.started.connect(self.update.run)
        self.update.new_data.connect(self.update_value)
        self.thread.start()

    def update_value(self, data):
        value = int(self.Players.text().split('/')[1])
        self.Players.setText(f"{data}/{value}")
        self.progressBar.setValue(data)

    def start(self):
        self.thread.quit()

        book = defaultdict(list)
        for i in ["geo", "aero"]:
            rec = receive().decode(FORMAT)
            count = int(rec)
            if count >= 1:
                for j in range(count):
                    char = pickle.loads(receive())
                    char.image = base64.decodebytes(receive())
                    book[i].append(char)

        for i in ["geo", "aero"]:
            for j in book[i]:
                battle_window.room_info[i].append(j)

        battle_window.update_info()
        show_battle_widow(self)


def create_new_character_frame(self, num, char_info):
    widget_list = defaultdict()

    frame = QFrame(self)
    frame.setGeometry(QtCore.QRect(4, 10, 331, 318))
    frame.setObjectName(f"frame_{num}")
    frame.setMaximumSize(331, 318)
    frame.setMinimumSize(331, 318)
    frame.setFrameShape(QtWidgets.QFrame.Box)
    frame.setFrameShadow(QtWidgets.QFrame.Plain)

    widget_list["frame"] = frame

    lvl = QtWidgets.QLabel(frame)
    lvl.setGeometry(QtCore.QRect(8, 5, 31, 20))
    lvl.setObjectName(f"lvl_{num}")
    lvl.setText(f"lvl {char_info.lvl}")
    font = QtGui.QFont()
    font.setPointSize(7)
    font.setItalic(False)
    lvl.setFont(font)
    lvl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop | QtCore.Qt.AlignTrailing)

    widget_list["lvl"] = lvl

    layoutWidget = QtWidgets.QWidget(frame)
    layoutWidget.setGeometry(QtCore.QRect(16, 68, 311, 243))
    layoutWidget.setObjectName(f"layoutWidget_{num}")
    verticalLayout = QtWidgets.QVBoxLayout(layoutWidget)
    verticalLayout.setContentsMargins(0, 0, 0, 0)
    verticalLayout.setObjectName(f"verticalLayout_{num}")
    horizontalLayout = QtWidgets.QHBoxLayout()
    horizontalLayout.setSpacing(10)
    horizontalLayout.setObjectName(f"horizontalLayout_{num}")

    avatar = QtWidgets.QLabel(layoutWidget)
    avatar.setMinimumSize(QtCore.QSize(155, 210))
    avatar.setMaximumSize(QtCore.QSize(155, 210))
    avatar.setScaledContents(True)
    pix = QPixmap()
    pix.loadFromData(QByteArray(bytearray(char_info.image)))
    avatar.setPixmap(pix)
    avatar.setObjectName(f"avatar_{num}")
    horizontalLayout.addWidget(avatar)

    widget_list["avatar"] = avatar

    mpBar = QtWidgets.QProgressBar(frame)
    mpBar.setGeometry(QtCore.QRect(16, 48, 301, 16))
    mpBar.setAutoFillBackground(False)
    mpBar.setStyleSheet("background: rgb(71, 71, 212);border: 1px solid black;")
    mpBar.setMaximum(char_info.max_mp)
    mpBar.setProperty("value", char_info.max_mp - char_info.mp)
    mpBar.setTextVisible(False)
    mpBar.setInvertedAppearance(True)
    mpBar.setObjectName(f"mpBar_{num}")

    widget_list["mpBar"] = mpBar

    mp = QtWidgets.QLabel(frame)
    mp.setGeometry(QtCore.QRect(20, 48, 291, 16))
    font = QtGui.QFont()
    font.setPointSize(10)
    font.setKerning(True)
    mp.setFont(font)
    mp.setAutoFillBackground(False)
    mp.setAlignment(QtCore.Qt.AlignCenter)
    mp.setObjectName(f"mp_{num}")
    mp.setText(f"{char_info.mp}/{char_info.max_mp}")

    widget_list["mp"] = mp

    list = QtWidgets.QListWidget(layoutWidget)
    list.setObjectName(f"list_{num}")
    book = char_info.weapon.list_ref()
    book += char_info.armor.list_ref()
    book += char_info.list_ref()
    list.addItems(book)
    horizontalLayout.addWidget(list)

    widget_list["list"] = list

    verticalLayout.addLayout(horizontalLayout)

    target = QtWidgets.QPushButton(layoutWidget)
    target.setObjectName(f"target_{num}")
    target.setText("Target")
    target.setEnabled(False)
    verticalLayout.addWidget(target)

    widget_list["target"] = target

    hpBar = QtWidgets.QProgressBar(frame)
    hpBar.setGeometry(QtCore.QRect(16, 29, 301, 16))
    hpBar.setMaximum(char_info.max_hp)
    hpBar.setProperty("value", char_info.hp)
    hpBar.setTextVisible(False)
    hpBar.setObjectName(f"hpBar_{num}")

    widget_list["hpBar"] = hpBar

    hp = QtWidgets.QLabel(frame)
    hp.setGeometry(QtCore.QRect(20, 29, 291, 16))
    font = QtGui.QFont()
    font.setPointSize(10)
    hp.setFont(font)
    hp.setAlignment(QtCore.Qt.AlignCenter)
    hp.setObjectName(f"hp_{num}")
    hp.setText(f"{char_info.max_hp}/{char_info.hp}")

    widget_list["hp"] = hp

    name = QtWidgets.QLabel(frame)
    name.setGeometry(QtCore.QRect(40, 10, 241, 21))
    font = QtGui.QFont()
    font.setPointSize(9)
    font.setBold(True)
    font.setWeight(75)
    name.setFont(font)
    name.setTextFormat(QtCore.Qt.AutoText)
    name.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    name.setObjectName(f"name_{num}")
    name.setText(char_info.name)

    widget_list["name"] = name

    return [frame, widget_list]


class ControlThread(QObject):
    log = pyqtSignal(list)
    input = pyqtSignal(str)
    end = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.receiving = True

    # noinspection PyUnresolvedReferences
    def run(self):
        while True:
            if self.receiving:
                rec = receive()
                if rec == b"!LOG":
                    self.log.emit(pickle.loads(receive()))
                    self.receiving = False
                elif rec == b"!INPUT":
                    self.input.emit(receive().decode(FORMAT))
                    self.receiving = False
                elif rec == b"!GAME_END":
                    self.end.emit()
                    self.receiving = False


class Battle_screen(QMainWindow, Ui_Battle):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Project-Creators')
        self.room_info = defaultdict(list)
        self.room_info['geo'] = []
        self.room_info['aero'] = []
        self.chars = []
        self.targets = []
        self.count = 0
        self.widget_list = []

    def update_info(self):
        self.chars = []

        layout = QGridLayout()
        for j, i in enumerate(self.room_info['geo']):
            widget = create_new_character_frame(self, j, i)
            self.widget_list.append(widget[1])
            layout.addWidget(widget[0])
            self.chars.append(i)

        w = QWidget()
        w.setObjectName("geo_w")
        w.setLayout(layout)

        self.geo_area.setWidget(w)

        layout = QGridLayout()
        for j, i in enumerate(self.room_info['aero']):
            widget = create_new_character_frame(self, j + len(self.room_info['geo']), i)
            self.widget_list.append(widget[1])
            layout.addWidget(widget[0])
            self.chars.append(i)

        w = QWidget()
        w.setObjectName("aero_w")
        w.setLayout(layout)

        self.aero_area.setWidget(w)

        for j, i in enumerate(info.abilities):
            butt = self.findChild(QtWidgets.QPushButton, f"AbilityButton{j + 1}")
            butt.clicked.connect(self.action)
            butt.setText(i)
        self.AttackButton.clicked.connect(self.action)
        self.TargetDelete.clicked.connect(self.delete_target)
        self.TargetConfirm.clicked.connect(self.confirm_target)

        for i in range(len(self.room_info["geo"]) + len(self.room_info["aero"])):
            self.findChild(QtWidgets.QPushButton, f"target_{i}").clicked.connect(self.add_target)

        self.update = ControlThread()
        self.thread = QThread()
        self.update.moveToThread(self.thread)
        self.thread.started.connect(self.update.run)
        self.update.log.connect(self.log_unpack)
        self.update.input.connect(self.make_action)
        self.update.end.connect(self.back_to_main)
        self.thread.start()

    def log_unpack(self, items):
        self.label.setText('')
        self.Log.clear()
        self.Log.addItems(items)
        data = pickle.loads(receive())
        self.info_unpack(data)
        self.update.receiving = True

    def back_to_main(self):
        pass

    def info_unpack(self, data):
        for j, i in enumerate(data):
            self.widget_list[j]["hp"].setText(f"{i[0]}/{i[1]}")
            self.widget_list[j]["hpBar"].setMaximum(int(i[1] * 1000))
            self.widget_list[j]["hpBar"].setValue(int(i[0] * 1000))

            self.widget_list[j]["mp"].setText(f"{i[2]}/{i[3]}")
            self.widget_list[j]["mpBar"].setMaximum(int(i[3] * 1000))
            self.widget_list[j]["mpBar"].setValue(int((i[3] - i[2]) * 1000))

    def enable_buttons(self, act: bool):
        for j, i in enumerate(info.abilities):
            butt = self.findChild(QtWidgets.QPushButton, f"AbilityButton{j + 1}")
            butt.setEnabled(act)
        self.AttackButton.setEnabled(act)

    def enable_targets(self, act: bool):
        for i in range(len(self.room_info["geo"]) + len(self.room_info["aero"])):
            self.findChild(QtWidgets.QPushButton, f"target_{i}").setEnabled(act)

    def action(self):
        if self.sender().objectName() == "AttackButton":
            send(b"attack")
            answer = receive()
            if answer == b"!Action":
                self.enable_buttons(False)
                self.targets = []
                self.update.receiving = True
            elif answer == b"!ERROR":
                self.Error.setText("Error action!")
        else:
            send(b"ability")
            answer = receive()
            if answer == b"!Action":
                self.enable_buttons(False)
                send(self.sender().text().encode(FORMAT))
                self.targets = []
                self.update.receiving = True
            elif answer == b"!ERROR":
                self.Error.setText("Error action!")

    def add_target(self):
        self.targets.append(self.chars[int(self.sender().objectName().split('_')[-1])].name)
        self.TargetDelete.setEnabled(True)
        if len(self.targets) == self.count:
            self.enable_targets(False)
            self.TargetConfirm.setEnabled(True)
        self.TargetList.clear()
        self.TargetList.addItems(self.targets)

    def delete_target(self):
        if self.TargetList.currentItem():
            self.targets.remove(self.TargetList.currentItem().text())
            self.enable_targets(True)
            self.TargetConfirm.setEnabled(False)
            if len(self.targets) < 1:
                self.TargetDelete.setEnabled(False)
            self.TargetList.clear()
            self.TargetList.addItems(self.targets)

    def confirm_target(self):
        send(pickle.dumps(self.targets, 3))
        self.targets = []
        self.TargetList.clear()
        self.TargetList.setEnabled(False)
        self.TargetDelete.setEnabled(False)
        self.TargetDelete.setEnabled(False)
        self.TargetConfirm.setEnabled(False)
        self.label.setText("")
        self.Error.setText("")
        self.update.receiving = True

    def make_action(self, command):
        self.thread.quit()
        if command == "!MAKE_ACTION":
            self.label.setText("Your turn")
            self.enable_buttons(True)
        elif command == "!CHOOSE_TARGET":
            self.count = int(receive().decode(FORMAT))
            self.label.setText(f"Choose {self.count} target(-s)")
            self.TargetList.setEnabled(True)
            self.enable_targets(True)


def show_main_widow(this):
    this.hide()
    main_window.update_info()
    main_window.show()


def show_battle_widow(this):
    this.hide()
    battle_window.show()


def show_waiting_widow(this):
    this.hide()
    waiting_window.update_info(*pickle.loads(receive()))
    waiting_window.show()


if __name__ == '__main__':
    info = Info(1, '', 0, 0, 0, 0, [0, 0, 0, 0, 0, 0, 0, 0], [],
                Info_Weapon('', '', 0, '', None),
                Info_Armor('', '', [0, 0, 0, 0, 0, 0, 0, 0], 0, 0), None, None, b'')

    try:
        app = QApplication(sys.argv)
        login_window = Login_screen()
        main_window = Main_screen()
        battle_window = Battle_screen()
        waiting_window = Waiting_screen()
        login_window.show()
        sys.exit(app.exec_())
    except SystemExit:
        send(b"!DISCONNECT")
