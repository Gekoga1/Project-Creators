# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'battle.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1033, 815)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(24)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.geo_area = QtWidgets.QScrollArea(self.centralwidget)
        self.geo_area.setMinimumSize(QtCore.QSize(374, 750))
        self.geo_area.setLayoutDirection(QtCore.Qt.RightToLeft)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 366, 742))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.frame_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_1.setGeometry(QtCore.QRect(4, 10, 331, 318))
        self.frame_1.setMinimumSize(QtCore.QSize(331, 318))
        self.frame_1.setMaximumSize(QtCore.QSize(331, 318))
        self.frame_1.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_1.setObjectName("frame_1")
        self.lvl_1 = QtWidgets.QLabel(self.frame_1)
        self.lvl_1.setGeometry(QtCore.QRect(8, 5, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(False)
        self.lvl_1.setFont(font)
        self.lvl_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lvl_1.setObjectName("lvl_1")
        self.widget = QtWidgets.QWidget(self.frame_1)
        self.widget.setGeometry(QtCore.QRect(16, 68, 311, 243))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setMinimumSize(QtCore.QSize(155, 210))
        self.frame.setMaximumSize(QtCore.QSize(155, 210))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.target = QtWidgets.QPushButton(self.widget)
        self.target.setObjectName("target")
        self.verticalLayout.addWidget(self.target)
        self.progressBar = QtWidgets.QProgressBar(self.frame_1)
        self.progressBar.setGeometry(QtCore.QRect(16, 34, 301, 23))
        self.progressBar.setMaximum(200)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.frame_1)
        self.label.setGeometry(QtCore.QRect(20, 34, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.name_2 = QtWidgets.QLabel(self.frame_1)
        self.name_2.setGeometry(QtCore.QRect(40, 10, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.name_2.setFont(font)
        self.name_2.setTextFormat(QtCore.Qt.AutoText)
        self.name_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_2.setObjectName("name_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_1)
        self.frame_4.setGeometry(QtCore.QRect(0, 450, 331, 318))
        self.frame_4.setMinimumSize(QtCore.QSize(331, 318))
        self.frame_4.setMaximumSize(QtCore.QSize(331, 318))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.lvl_3 = QtWidgets.QLabel(self.frame_4)
        self.lvl_3.setGeometry(QtCore.QRect(8, 5, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(False)
        self.lvl_3.setFont(font)
        self.lvl_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lvl_3.setObjectName("lvl_3")
        self.layoutWidget_3 = QtWidgets.QWidget(self.frame_4)
        self.layoutWidget_3.setGeometry(QtCore.QRect(16, 68, 311, 243))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_5 = QtWidgets.QFrame(self.layoutWidget_3)
        self.frame_5.setMinimumSize(QtCore.QSize(155, 210))
        self.frame_5.setMaximumSize(QtCore.QSize(155, 210))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_8.addWidget(self.frame_5)
        self.listWidget_4 = QtWidgets.QListWidget(self.layoutWidget_3)
        self.listWidget_4.setObjectName("listWidget_4")
        self.horizontalLayout_8.addWidget(self.listWidget_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.target_3 = QtWidgets.QPushButton(self.layoutWidget_3)
        self.target_3.setObjectName("target_3")
        self.verticalLayout_4.addWidget(self.target_3)
        self.progressBar_3 = QtWidgets.QProgressBar(self.frame_4)
        self.progressBar_3.setGeometry(QtCore.QRect(16, 34, 301, 23))
        self.progressBar_3.setMaximum(200)
        self.progressBar_3.setProperty("value", 100)
        self.progressBar_3.setTextVisible(False)
        self.progressBar_3.setObjectName("progressBar_3")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setGeometry(QtCore.QRect(20, 34, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.name_4 = QtWidgets.QLabel(self.frame_4)
        self.name_4.setGeometry(QtCore.QRect(40, 10, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.name_4.setFont(font)
        self.name_4.setTextFormat(QtCore.Qt.AutoText)
        self.name_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_4.setObjectName("name_4")
        self.geo_area.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.geo_area)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.aero_area = QtWidgets.QScrollArea(self.centralwidget)
        self.aero_area.setMinimumSize(QtCore.QSize(374, 750))
        self.aero_area.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.aero_area.setAutoFillBackground(False)
        self.aero_area.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.aero_area.setFrameShape(QtWidgets.QFrame.Box)
        self.aero_area.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.aero_area.setLineWidth(1)
        self.aero_area.setMidLineWidth(2)
        self.aero_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.aero_area.setWidgetResizable(False)
        self.aero_area.setObjectName("aero_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 366, 742))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.frame_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 331, 318))
        self.frame_2.setMinimumSize(QtCore.QSize(331, 318))
        self.frame_2.setMaximumSize(QtCore.QSize(331, 318))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.lvl_2 = QtWidgets.QLabel(self.frame_2)
        self.lvl_2.setGeometry(QtCore.QRect(8, 5, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(False)
        self.lvl_2.setFont(font)
        self.lvl_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lvl_2.setObjectName("lvl_2")
        self.layoutWidget_2 = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget_2.setGeometry(QtCore.QRect(16, 68, 311, 243))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.layoutWidget_2)
        self.frame_3.setMinimumSize(QtCore.QSize(155, 210))
        self.frame_3.setMaximumSize(QtCore.QSize(155, 210))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4.addWidget(self.frame_3)
        self.listWidget_2 = QtWidgets.QListWidget(self.layoutWidget_2)
        self.listWidget_2.setObjectName("listWidget_2")
        self.horizontalLayout_4.addWidget(self.listWidget_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.target_2 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.target_2.setObjectName("target_2")
        self.verticalLayout_2.addWidget(self.target_2)
        self.progressBar_2 = QtWidgets.QProgressBar(self.frame_2)
        self.progressBar_2.setGeometry(QtCore.QRect(16, 34, 301, 23))
        self.progressBar_2.setMaximum(200)
        self.progressBar_2.setProperty("value", 100)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setObjectName("progressBar_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(20, 34, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.name_3 = QtWidgets.QLabel(self.frame_2)
        self.name_3.setGeometry(QtCore.QRect(40, 10, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.name_3.setFont(font)
        self.name_3.setTextFormat(QtCore.Qt.AutoText)
        self.name_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.name_3.setObjectName("name_3")
        self.aero_area.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.addWidget(self.aero_area)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 50)
        self.verticalLayout_3.setSpacing(50)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setMinimumSize(QtCore.QSize(200, 300))
        self.listWidget_3.setMaximumSize(QtCore.QSize(250, 16777215))
        self.listWidget_3.setObjectName("listWidget_3")
        self.verticalLayout_3.addWidget(self.listWidget_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1033, 21))
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
        self.lvl_1.setText(_translate("MainWindow", "lvl 100"))
        self.target.setText(_translate("MainWindow", "Target"))
        self.label.setText(_translate("MainWindow", "100/200"))
        self.name_2.setText(_translate("MainWindow", "Gekoga"))
        self.lvl_3.setText(_translate("MainWindow", "lvl 100"))
        self.target_3.setText(_translate("MainWindow", "Target"))
        self.label_3.setText(_translate("MainWindow", "100/200"))
        self.name_4.setText(_translate("MainWindow", "Gekoga"))
        self.lvl_2.setText(_translate("MainWindow", "lvl 100"))
        self.target_2.setText(_translate("MainWindow", "Target"))
        self.label_2.setText(_translate("MainWindow", "100/200"))
        self.name_3.setText(_translate("MainWindow", "Gekoga"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))