# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(554, 200)
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono ExtraBold")
        Form.setFont(font)
        Form.setStyleSheet("QLineEdit:hover{\n"
                           "       background-color:transparent;\n"
                           "    border-radius:7px;\n"
                           "    border:none;\n"
                           "    border-bottom:2px solid rgb(203, 203, 203);\n"
                           "    color:rgb(0, 0, 0);\n"
                           "    padding-bottom:7px;\n"
                           "}\n"
                           "QLineEdit{\n"
                           "    border:none;\n"
                           "    background-color:transparent;\n"
                           "    border-radius:7px;\n"
                           "    color:rgb(0,0,0);\n"
                           "    border-bottom:2px solid rgb(203, 203, 203);\n"
                           "    padding-bottom:7px;\n"
                           "}")
        self.uesr_name = QtWidgets.QLineEdit(Form)
        self.uesr_name.setGeometry(QtCore.QRect(129, 72, 421, 25))
        self.uesr_name.setObjectName("uesr_name")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 161, 51))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono ExtraBold")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 50, 554, 3))
        self.line.setStyleSheet("background-color: rgb(176, 176, 176);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 554, 351))
        self.label_2.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(2, 72, 120, 26))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 81 12pt \"JetBrains Mono ExtraBold\";")
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(2, 115, 120, 26))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 81 12pt \"JetBrains Mono ExtraBold\";")
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setGeometry(QtCore.QRect(129, 115, 421, 25))
        self.password.setObjectName("password")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(410, 160, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(450, 10, 91, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.WindowsTitle = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.WindowsTitle.setContentsMargins(0, 0, 0, 0)
        self.WindowsTitle.setObjectName("WindowsTitle")
        self.small = QtWidgets.QPushButton(self.layoutWidget)
        self.small.setMinimumSize(QtCore.QSize(24, 24))
        self.small.setMaximumSize(QtCore.QSize(24, 24))
        self.small.setStyleSheet("border-radius:12;\n"
                                 "background-color: yellow;")
        self.small.setText("")
        self.small.setObjectName("small")
        self.WindowsTitle.addWidget(self.small)
        self.Max = QtWidgets.QPushButton(self.layoutWidget)
        self.Max.setMinimumSize(QtCore.QSize(24, 24))
        self.Max.setMaximumSize(QtCore.QSize(24, 24))
        self.Max.setStyleSheet("border-radius:12;\n"
                               "background-color: green;")
        self.Max.setText("")
        self.Max.setObjectName("Max")
        self.WindowsTitle.addWidget(self.Max)
        self.exit = QtWidgets.QPushButton(self.layoutWidget)
        self.exit.setMinimumSize(QtCore.QSize(24, 24))
        self.exit.setMaximumSize(QtCore.QSize(24, 24))
        self.exit.setStyleSheet("border-radius:12;\n"
                                "background-color: red;")
        self.exit.setText("")
        self.exit.setObjectName("exit")
        self.WindowsTitle.addWidget(self.exit)
        self.label_2.raise_()
        self.uesr_name.raise_()
        self.label.raise_()
        self.line.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.password.raise_()
        self.pushButton.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Login Us"))
        self.label_3.setText(_translate("Form", "Uesr name:"))
        self.label_4.setText(_translate("Form", "Password:"))
        self.pushButton.setText(_translate("Form", "Start"))
        self.exit.setShortcut(_translate("Form", "Esc"))
