# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'order_assistant_widget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_OrderAssistant(object):
    def setupUi(self, Form_OrderAssistant):
        Form_OrderAssistant.setObjectName("Form_OrderAssistant")
        Form_OrderAssistant.resize(422, 300)
        self.widget = QtWidgets.QWidget(Form_OrderAssistant)
        self.widget.setGeometry(QtCore.QRect(20, 20, 177, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_ProdCode = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_ProdCode.setObjectName("lineEdit_ProdCode")
        self.horizontalLayout_7.addWidget(self.lineEdit_ProdCode)
        self.widget1 = QtWidgets.QWidget(Form_OrderAssistant)
        self.widget1.setGeometry(QtCore.QRect(11, 51, 394, 58))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_takeprofit_amount = QtWidgets.QSpinBox(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_takeprofit_amount.sizePolicy().hasHeightForWidth())
        self.spinBox_takeprofit_amount.setSizePolicy(sizePolicy)
        self.spinBox_takeprofit_amount.setMinimum(-16777215)
        self.spinBox_takeprofit_amount.setMaximum(16777215)
        self.spinBox_takeprofit_amount.setObjectName("spinBox_takeprofit_amount")
        self.horizontalLayout.addWidget(self.spinBox_takeprofit_amount)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_takeprofit_price = QtWidgets.QLineEdit(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_takeprofit_price.sizePolicy().hasHeightForWidth())
        self.lineEdit_takeprofit_price.setSizePolicy(sizePolicy)
        self.lineEdit_takeprofit_price.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_takeprofit_price.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_takeprofit_price.setReadOnly(True)
        self.lineEdit_takeprofit_price.setObjectName("lineEdit_takeprofit_price")
        self.horizontalLayout_3.addWidget(self.lineEdit_takeprofit_price)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_stoploss_amount = QtWidgets.QSpinBox(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_stoploss_amount.sizePolicy().hasHeightForWidth())
        self.spinBox_stoploss_amount.setSizePolicy(sizePolicy)
        self.spinBox_stoploss_amount.setMinimum(-16777215)
        self.spinBox_stoploss_amount.setMaximum(16777215)
        self.spinBox_stoploss_amount.setObjectName("spinBox_stoploss_amount")
        self.horizontalLayout_2.addWidget(self.spinBox_stoploss_amount)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_stoploss_price = QtWidgets.QLineEdit(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_stoploss_price.sizePolicy().hasHeightForWidth())
        self.lineEdit_stoploss_price.setSizePolicy(sizePolicy)
        self.lineEdit_stoploss_price.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_stoploss_price.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_stoploss_price.setReadOnly(True)
        self.lineEdit_stoploss_price.setObjectName("lineEdit_stoploss_price")
        self.horizontalLayout_4.addWidget(self.lineEdit_stoploss_price)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_calc_tp_sl = QtWidgets.QPushButton(self.widget1)
        self.pushButton_calc_tp_sl.setObjectName("pushButton_calc_tp_sl")
        self.verticalLayout.addWidget(self.pushButton_calc_tp_sl)
        self.pushButton_OCO_close_position = QtWidgets.QPushButton(self.widget1)
        self.pushButton_OCO_close_position.setObjectName("pushButton_OCO_close_position")
        self.verticalLayout.addWidget(self.pushButton_OCO_close_position)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        self.label_5.setBuddy(self.lineEdit_ProdCode)
        self.label.setBuddy(self.spinBox_takeprofit_amount)
        self.label_3.setBuddy(self.lineEdit_takeprofit_price)
        self.label_2.setBuddy(self.spinBox_stoploss_amount)
        self.label_4.setBuddy(self.lineEdit_stoploss_price)

        self.retranslateUi(Form_OrderAssistant)
        QtCore.QMetaObject.connectSlotsByName(Form_OrderAssistant)

    def retranslateUi(self, Form_OrderAssistant):
        _translate = QtCore.QCoreApplication.translate
        Form_OrderAssistant.setWindowTitle(_translate("Form_OrderAssistant", "SP ORDER ASSISTANT"))
        self.label_5.setText(_translate("Form_OrderAssistant", "代码："))
        self.label.setText(_translate("Form_OrderAssistant", "止盈金额"))
        self.label_3.setText(_translate("Form_OrderAssistant", "止盈价"))
        self.label_2.setText(_translate("Form_OrderAssistant", "止损金额"))
        self.label_4.setText(_translate("Form_OrderAssistant", "止损价"))
        self.pushButton_calc_tp_sl.setText(_translate("Form_OrderAssistant", "计算止盈止损位"))
        self.pushButton_OCO_close_position.setText(_translate("Form_OrderAssistant", "双向限价平仓"))

