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
        Form_OrderAssistant.resize(420, 484)
        self.layoutWidget = QtWidgets.QWidget(Form_OrderAssistant)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 177, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_ProdCode = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_ProdCode.setObjectName("lineEdit_ProdCode")
        self.horizontalLayout_7.addWidget(self.lineEdit_ProdCode)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.lineEdit_price = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_price.setEnabled(True)
        self.lineEdit_price.setReadOnly(True)
        self.lineEdit_price.setObjectName("lineEdit_price")
        self.horizontalLayout_7.addWidget(self.lineEdit_price)
        self.groupBox = QtWidgets.QGroupBox(Form_OrderAssistant)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 391, 91))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_takeprofit_amount = QtWidgets.QSpinBox(self.groupBox)
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
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_takeprofit_price = QtWidgets.QLineEdit(self.groupBox)
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
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_stoploss_amount = QtWidgets.QSpinBox(self.groupBox)
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
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_stoploss_price = QtWidgets.QLineEdit(self.groupBox)
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
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_tp_by_amount = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_tp_by_amount.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_tp_by_amount.setObjectName("pushButton_tp_by_amount")
        self.verticalLayout_9.addWidget(self.pushButton_tp_by_amount)
        self.pushButton_sl_by_amount = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_sl_by_amount.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_sl_by_amount.setObjectName("pushButton_sl_by_amount")
        self.verticalLayout_9.addWidget(self.pushButton_sl_by_amount)
        self.horizontalLayout_31.addLayout(self.verticalLayout_9)
        self.pushButton_OCO_close_position = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_OCO_close_position.setObjectName("pushButton_OCO_close_position")
        self.horizontalLayout_31.addWidget(self.pushButton_OCO_close_position)
        self.verticalLayout.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        self.groupBox_2 = QtWidgets.QGroupBox(Form_OrderAssistant)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 391, 91))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_10.addWidget(self.label_6)
        self.spinBox_tp_price = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_tp_price.setMaximum(16777215)
        self.spinBox_tp_price.setObjectName("spinBox_tp_price")
        self.horizontalLayout_10.addWidget(self.spinBox_tp_price)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_10)
        self.pushButton_tp = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_tp.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_tp.setObjectName("pushButton_tp")
        self.horizontalLayout_12.addWidget(self.pushButton_tp)
        self.checkBox_auto_tp = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_auto_tp.setCheckable(False)
        self.checkBox_auto_tp.setObjectName("checkBox_auto_tp")
        self.horizontalLayout_12.addWidget(self.checkBox_auto_tp)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_11.addWidget(self.label_7)
        self.spinBox_sl_price = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_sl_price.setMaximum(16777215)
        self.spinBox_sl_price.setObjectName("spinBox_sl_price")
        self.horizontalLayout_11.addWidget(self.spinBox_sl_price)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_22.addWidget(self.label_14)
        self.spinBox_stoploss_toler = QtWidgets.QSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_stoploss_toler.sizePolicy().hasHeightForWidth())
        self.spinBox_stoploss_toler.setSizePolicy(sizePolicy)
        self.spinBox_stoploss_toler.setMaximumSize(QtCore.QSize(35, 16777215))
        self.spinBox_stoploss_toler.setMaximum(1000)
        self.spinBox_stoploss_toler.setObjectName("spinBox_stoploss_toler")
        self.horizontalLayout_22.addWidget(self.spinBox_stoploss_toler)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem1)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_11)
        self.pushButton_sl = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_sl.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_sl.setObjectName("pushButton_sl")
        self.horizontalLayout_13.addWidget(self.pushButton_sl)
        self.checkBox_auto_sl = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_auto_sl.setCheckable(False)
        self.checkBox_auto_sl.setObjectName("checkBox_auto_sl")
        self.horizontalLayout_13.addWidget(self.checkBox_auto_sl)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14.addLayout(self.verticalLayout_3)
        self.groupBox_3 = QtWidgets.QGroupBox(Form_OrderAssistant)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 230, 391, 116))
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_15.addWidget(self.label_8)
        self.spinBox_trailing_toler = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_trailing_toler.setMaximum(16777215)
        self.spinBox_trailing_toler.setObjectName("spinBox_trailing_toler")
        self.horizontalLayout_15.addWidget(self.spinBox_trailing_toler)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_15)
        self.checkBox_trailing_stop = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_trailing_stop.setObjectName("checkBox_trailing_stop")
        self.horizontalLayout_16.addWidget(self.checkBox_trailing_stop)
        self.horizontalLayout_17.addLayout(self.horizontalLayout_16)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_18.addWidget(self.label_9)
        self.lineEdit_best_price = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_best_price.setEnabled(True)
        self.lineEdit_best_price.setReadOnly(True)
        self.lineEdit_best_price.setObjectName("lineEdit_best_price")
        self.horizontalLayout_18.addWidget(self.lineEdit_best_price)
        self.verticalLayout_4.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_19.addWidget(self.label_10)
        self.lineEdit_sl_close_price = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_sl_close_price.setEnabled(True)
        self.lineEdit_sl_close_price.setReadOnly(True)
        self.lineEdit_sl_close_price.setObjectName("lineEdit_sl_close_price")
        self.horizontalLayout_19.addWidget(self.lineEdit_sl_close_price)
        self.verticalLayout_4.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_17.addLayout(self.verticalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_17)
        self.horizontalSlider_toler = QtWidgets.QSlider(self.groupBox_3)
        self.horizontalSlider_toler.setEnabled(False)
        self.horizontalSlider_toler.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_toler.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider_toler.setTickInterval(5)
        self.horizontalSlider_toler.setObjectName("horizontalSlider_toler")
        self.verticalLayout_7.addWidget(self.horizontalSlider_toler)
        self.horizontalLayout_20.addLayout(self.verticalLayout_7)
        self.layoutWidget1 = QtWidgets.QWidget(Form_OrderAssistant)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.layoutWidget2 = QtWidgets.QWidget(Form_OrderAssistant)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.layoutWidget3 = QtWidgets.QWidget(Form_OrderAssistant)
        self.layoutWidget3.setGeometry(QtCore.QRect(240, 20, 151, 22))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_21.addWidget(self.label_12)
        self.lineEdit_holding_qty = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_holding_qty.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_holding_qty.sizePolicy().hasHeightForWidth())
        self.lineEdit_holding_qty.setSizePolicy(sizePolicy)
        self.lineEdit_holding_qty.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_holding_qty.setReadOnly(True)
        self.lineEdit_holding_qty.setObjectName("lineEdit_holding_qty")
        self.horizontalLayout_21.addWidget(self.lineEdit_holding_qty)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_21.addWidget(self.label_11)
        self.lineEdit_holding_price = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_holding_price.setEnabled(True)
        self.lineEdit_holding_price.setReadOnly(True)
        self.lineEdit_holding_price.setObjectName("lineEdit_holding_price")
        self.horizontalLayout_21.addWidget(self.lineEdit_holding_price)
        self.groupBox_4 = QtWidgets.QGroupBox(Form_OrderAssistant)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 360, 391, 120))
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_23.addWidget(self.label_15)
        self.spinBox_tp_addition = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_tp_addition.setMaximum(16777215)
        self.spinBox_tp_addition.setObjectName("spinBox_tp_addition")
        self.horizontalLayout_23.addWidget(self.spinBox_tp_addition)
        self.horizontalLayout_26.addLayout(self.horizontalLayout_23)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem2)
        self.pushButton_tp_pos_by_pos = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_tp_pos_by_pos.setObjectName("pushButton_tp_pos_by_pos")
        self.horizontalLayout_26.addWidget(self.pushButton_tp_pos_by_pos)
        self.verticalLayout_8.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_24.addWidget(self.label_16)
        self.spinBox_sl_addition = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_sl_addition.setMaximum(16777215)
        self.spinBox_sl_addition.setObjectName("spinBox_sl_addition")
        self.horizontalLayout_24.addWidget(self.spinBox_sl_addition)
        self.horizontalLayout_27.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_30.addWidget(self.label_18)
        self.spinBox_sl_addition_toler = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_sl_addition_toler.setMaximum(1000)
        self.spinBox_sl_addition_toler.setObjectName("spinBox_sl_addition_toler")
        self.horizontalLayout_30.addWidget(self.spinBox_sl_addition_toler)
        self.horizontalLayout_27.addLayout(self.horizontalLayout_30)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem3)
        self.pushButton_sl_pos_by_pos = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_sl_pos_by_pos.setObjectName("pushButton_sl_pos_by_pos")
        self.horizontalLayout_27.addWidget(self.pushButton_sl_pos_by_pos)
        self.verticalLayout_8.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_25.addWidget(self.label_17)
        self.spinBox_lock_pos = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox_lock_pos.setObjectName("spinBox_lock_pos")
        self.horizontalLayout_25.addWidget(self.spinBox_lock_pos)
        self.horizontalLayout_28.addLayout(self.horizontalLayout_25)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_28.addItem(spacerItem4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_29.addLayout(self.verticalLayout_8)
        self.label_5.setBuddy(self.lineEdit_ProdCode)
        self.label.setBuddy(self.spinBox_takeprofit_amount)
        self.label_3.setBuddy(self.lineEdit_takeprofit_price)
        self.label_2.setBuddy(self.spinBox_stoploss_amount)
        self.label_4.setBuddy(self.lineEdit_stoploss_price)
        self.label_6.setBuddy(self.spinBox_tp_price)
        self.label_7.setBuddy(self.spinBox_sl_price)
        self.label_14.setBuddy(self.spinBox_stoploss_toler)
        self.label_8.setBuddy(self.spinBox_trailing_toler)
        self.label_15.setBuddy(self.spinBox_tp_addition)
        self.label_16.setBuddy(self.spinBox_sl_addition)
        self.label_18.setBuddy(self.spinBox_sl_addition_toler)
        self.label_17.setBuddy(self.spinBox_lock_pos)

        self.retranslateUi(Form_OrderAssistant)
        self.checkBox_auto_tp.toggled['bool'].connect(self.spinBox_tp_price.setDisabled)
        self.checkBox_auto_sl.toggled['bool'].connect(self.spinBox_sl_price.setDisabled)
        self.checkBox_trailing_stop.toggled['bool'].connect(self.spinBox_trailing_toler.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Form_OrderAssistant)

    def retranslateUi(self, Form_OrderAssistant):
        _translate = QtCore.QCoreApplication.translate
        Form_OrderAssistant.setWindowTitle(_translate("Form_OrderAssistant", "SP ORDER ASSISTANT"))
        self.label_5.setText(_translate("Form_OrderAssistant", "代码："))
        self.label_13.setText(_translate("Form_OrderAssistant", "@"))
        self.groupBox.setTitle(_translate("Form_OrderAssistant", "指定金额平仓"))
        self.label.setText(_translate("Form_OrderAssistant", "止盈金额"))
        self.label_3.setText(_translate("Form_OrderAssistant", "止盈价"))
        self.label_2.setText(_translate("Form_OrderAssistant", "止损金额"))
        self.label_4.setText(_translate("Form_OrderAssistant", "止损价"))
        self.pushButton_tp_by_amount.setText(_translate("Form_OrderAssistant", "止盈"))
        self.pushButton_sl_by_amount.setText(_translate("Form_OrderAssistant", "止损"))
        self.pushButton_OCO_close_position.setText(_translate("Form_OrderAssistant", "双限平仓"))
        self.groupBox_2.setTitle(_translate("Form_OrderAssistant", "指定价格平仓"))
        self.label_6.setText(_translate("Form_OrderAssistant", "止盈价"))
        self.pushButton_tp.setText(_translate("Form_OrderAssistant", "止盈"))
        self.checkBox_auto_tp.setText(_translate("Form_OrderAssistant", "自动止盈"))
        self.label_7.setText(_translate("Form_OrderAssistant", "止损价"))
        self.label_14.setText(_translate("Form_OrderAssistant", "追价"))
        self.pushButton_sl.setText(_translate("Form_OrderAssistant", "止损"))
        self.checkBox_auto_sl.setText(_translate("Form_OrderAssistant", "自动止损"))
        self.groupBox_3.setTitle(_translate("Form_OrderAssistant", "移动止损"))
        self.label_8.setText(_translate("Form_OrderAssistant", "追踪点数"))
        self.checkBox_trailing_stop.setText(_translate("Form_OrderAssistant", "移动止损"))
        self.label_9.setText(_translate("Form_OrderAssistant", "最优价位"))
        self.label_10.setText(_translate("Form_OrderAssistant", "平仓价位"))
        self.label_12.setText(_translate("Form_OrderAssistant", "持仓:"))
        self.label_11.setText(_translate("Form_OrderAssistant", "@"))
        self.groupBox_4.setTitle(_translate("Form_OrderAssistant", "逐仓平仓"))
        self.label_15.setText(_translate("Form_OrderAssistant", "止盈点差"))
        self.pushButton_tp_pos_by_pos.setText(_translate("Form_OrderAssistant", "设置止盈"))
        self.label_16.setText(_translate("Form_OrderAssistant", "止损点差"))
        self.label_18.setText(_translate("Form_OrderAssistant", "止损追价"))
        self.pushButton_sl_pos_by_pos.setText(_translate("Form_OrderAssistant", "设置止损"))
        self.label_17.setText(_translate("Form_OrderAssistant", "锁定仓位"))

