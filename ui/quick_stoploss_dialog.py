# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_stoploss_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_quick_stoploss(object):
    def setupUi(self, Dialog_quick_stoploss):
        Dialog_quick_stoploss.setObjectName("Dialog_quick_stoploss")
        Dialog_quick_stoploss.resize(614, 207)
        self.groupBox_quick_sl = QtWidgets.QGroupBox(Dialog_quick_stoploss)
        self.groupBox_quick_sl.setGeometry(QtCore.QRect(30, 40, 524, 114))
        self.groupBox_quick_sl.setObjectName("groupBox_quick_sl")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_quick_sl)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_hodling_pos = QtWidgets.QLineEdit(self.groupBox_quick_sl)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_hodling_pos.sizePolicy().hasHeightForWidth())
        self.lineEdit_hodling_pos.setSizePolicy(sizePolicy)
        self.lineEdit_hodling_pos.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_hodling_pos.setReadOnly(True)
        self.lineEdit_hodling_pos.setObjectName("lineEdit_hodling_pos")
        self.horizontalLayout.addWidget(self.lineEdit_hodling_pos)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_session_pos = QtWidgets.QLineEdit(self.groupBox_quick_sl)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_session_pos.sizePolicy().hasHeightForWidth())
        self.lineEdit_session_pos.setSizePolicy(sizePolicy)
        self.lineEdit_session_pos.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_session_pos.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_session_pos.setReadOnly(True)
        self.lineEdit_session_pos.setObjectName("lineEdit_session_pos")
        self.horizontalLayout_2.addWidget(self.lineEdit_session_pos)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_all_pos = QtWidgets.QLineEdit(self.groupBox_quick_sl)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_all_pos.sizePolicy().hasHeightForWidth())
        self.lineEdit_all_pos.setSizePolicy(sizePolicy)
        self.lineEdit_all_pos.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_all_pos.setReadOnly(True)
        self.lineEdit_all_pos.setObjectName("lineEdit_all_pos")
        self.horizontalLayout_3.addWidget(self.lineEdit_all_pos)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox_sl_toler = QtWidgets.QSpinBox(self.groupBox_quick_sl)
        self.spinBox_sl_toler.setObjectName("spinBox_sl_toler")
        self.horizontalLayout_4.addWidget(self.spinBox_sl_toler)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.spinBox_stoploss = QtWidgets.QSpinBox(self.groupBox_quick_sl)
        self.spinBox_stoploss.setMaximum(1000)
        self.spinBox_stoploss.setProperty("value", 50)
        self.spinBox_stoploss.setObjectName("spinBox_stoploss")
        self.horizontalLayout_5.addWidget(self.spinBox_stoploss)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox_quick_sl)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.spinBox_lock = QtWidgets.QSpinBox(self.groupBox_quick_sl)
        self.spinBox_lock.setObjectName("spinBox_lock")
        self.horizontalLayout_6.addWidget(self.spinBox_lock)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_stoploss = QtWidgets.QPushButton(self.groupBox_quick_sl)
        self.pushButton_stoploss.setObjectName("pushButton_stoploss")
        self.horizontalLayout_8.addWidget(self.pushButton_stoploss)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.widget = QtWidgets.QWidget(Dialog_quick_stoploss)
        self.widget.setGeometry(QtCore.QRect(30, 10, 104, 23))
        self.widget.setObjectName("widget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.lineEdit_prodcode = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_prodcode.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_prodcode.setReadOnly(True)
        self.lineEdit_prodcode.setObjectName("lineEdit_prodcode")
        self.horizontalLayout_10.addWidget(self.lineEdit_prodcode)
        self.widget1 = QtWidgets.QWidget(Dialog_quick_stoploss)
        self.widget1.setGeometry(QtCore.QRect(50, 160, 352, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_del_all_orders = QtWidgets.QPushButton(self.widget1)
        self.pushButton_del_all_orders.setObjectName("pushButton_del_all_orders")
        self.horizontalLayout_11.addWidget(self.pushButton_del_all_orders)
        self.pushButton_del_short_orders = QtWidgets.QPushButton(self.widget1)
        self.pushButton_del_short_orders.setObjectName("pushButton_del_short_orders")
        self.horizontalLayout_11.addWidget(self.pushButton_del_short_orders)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_11.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_11.addWidget(self.pushButton_4)

        self.retranslateUi(Dialog_quick_stoploss)
        QtCore.QMetaObject.connectSlotsByName(Dialog_quick_stoploss)

    def retranslateUi(self, Dialog_quick_stoploss):
        _translate = QtCore.QCoreApplication.translate
        Dialog_quick_stoploss.setWindowTitle(_translate("Dialog_quick_stoploss", "Dialog"))
        self.groupBox_quick_sl.setTitle(_translate("Dialog_quick_stoploss", "-@-"))
        self.label.setText(_translate("Dialog_quick_stoploss", "持仓成本"))
        self.label_2.setText(_translate("Dialog_quick_stoploss", "会话成本"))
        self.label_3.setText(_translate("Dialog_quick_stoploss", "  总成本"))
        self.label_4.setText(_translate("Dialog_quick_stoploss", "追价点位"))
        self.label_5.setText(_translate("Dialog_quick_stoploss", "止损点位"))
        self.label_6.setText(_translate("Dialog_quick_stoploss", "锁单数"))
        self.pushButton_stoploss.setText(_translate("Dialog_quick_stoploss", "止损"))
        self.label_7.setText(_translate("Dialog_quick_stoploss", "代码："))
        self.pushButton_del_all_orders.setText(_translate("Dialog_quick_stoploss", "删除未成交单"))
        self.pushButton_del_short_orders.setText(_translate("Dialog_quick_stoploss", "删除止损多单"))
        self.pushButton_3.setText(_translate("Dialog_quick_stoploss", "删除止损空单"))
        self.pushButton_4.setText(_translate("Dialog_quick_stoploss", "删除多余止损单"))

