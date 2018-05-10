# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_widget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_time(object):
    def setupUi(self, Form_time):
        Form_time.setObjectName("Form_time")
        Form_time.resize(400, 261)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form_time)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form_time)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_sys_time = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.label_sys_time.setFont(font)
        self.label_sys_time.setText("")
        self.label_sys_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sys_time.setObjectName("label_sys_time")
        self.verticalLayout.addWidget(self.label_sys_time)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form_time)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_data_time = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.label_data_time.setFont(font)
        self.label_data_time.setText("")
        self.label_data_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data_time.setObjectName("label_data_time")
        self.verticalLayout_2.addWidget(self.label_data_time)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form_time)
        QtCore.QMetaObject.connectSlotsByName(Form_time)

    def retranslateUi(self, Form_time):
        _translate = QtCore.QCoreApplication.translate
        Form_time.setWindowTitle(_translate("Form_time", "Form"))
        self.groupBox.setTitle(_translate("Form_time", "系统时间"))
        self.groupBox_2.setTitle(_translate("Form_time", "数据时间"))

