# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'battle.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.verticalLayout_3.setSpacing(50)
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
        self.AbilityButton1.setText(_translate("Battle", "None"))
        self.AbilityButton3.setText(_translate("Battle", "None"))
        self.AbilityButton4.setText(_translate("Battle", "None"))
        self.AbilityButton2.setText(_translate("Battle", "None"))
        self.AttackButton.setText(_translate("Battle", "Attack"))
        self.AbilityButton5.setText(_translate("Battle", "None"))
