# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_order_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog_quick_order(object):
    def setupUi(self, Dialog_quick_order):
        Dialog_quick_order.setObjectName("Dialog_quick_order")
        Dialog_quick_order.resize(430, 842)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_quick_order.sizePolicy().hasHeightForWidth())
        Dialog_quick_order.setSizePolicy(sizePolicy)
        Dialog_quick_order.setMinimumSize(QtCore.QSize(425, 0))
        Dialog_quick_order.setMaximumSize(QtCore.QSize(430, 16777215))
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(Dialog_quick_order)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog_quick_order)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_ProdCode = QtWidgets.QLineEdit(Dialog_quick_order)
        self.lineEdit_ProdCode.setObjectName("lineEdit_ProdCode")
        self.horizontalLayout.addWidget(self.lineEdit_ProdCode)
        self.checkBox_Lock = QtWidgets.QCheckBox(Dialog_quick_order)
        self.checkBox_Lock.setObjectName("checkBox_Lock")
        self.horizontalLayout.addWidget(self.checkBox_Lock)
        self.horizontalLayout_9.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_Qty = QtWidgets.QSpinBox(Dialog_quick_order)
        self.spinBox_Qty.setEnabled(False)
        self.spinBox_Qty.setProperty("value", 1)
        self.spinBox_Qty.setObjectName("spinBox_Qty")
        self.horizontalLayout_2.addWidget(self.spinBox_Qty)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_9)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.label_pos = QtWidgets.QLabel(Dialog_quick_order)
        self.label_pos.setText("")
        self.label_pos.setObjectName("label_pos")
        self.horizontalLayout_5.addWidget(self.label_pos)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.label_holding_porfit = QtWidgets.QLabel(Dialog_quick_order)
        self.label_holding_porfit.setText("")
        self.label_holding_porfit.setObjectName("label_holding_porfit")
        self.horizontalLayout_4.addWidget(self.label_holding_porfit)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_closed_profit = QtWidgets.QLabel(Dialog_quick_order)
        self.label_closed_profit.setText("")
        self.label_closed_profit.setObjectName("label_closed_profit")
        self.horizontalLayout_3.addWidget(self.label_closed_profit)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.pushButton_close_position = QtWidgets.QPushButton(Dialog_quick_order)
        self.pushButton_close_position.setEnabled(False)
        self.pushButton_close_position.setObjectName("pushButton_close_position")
        self.horizontalLayout_10.addWidget(self.pushButton_close_position)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_long = QtWidgets.QPushButton(Dialog_quick_order)
        self.pushButton_long.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_long.sizePolicy().hasHeightForWidth())
        self.pushButton_long.setSizePolicy(sizePolicy)
        self.pushButton_long.setObjectName("pushButton_long")
        self.verticalLayout_7.addWidget(self.pushButton_long)
        self.label_long_info = QtWidgets.QLabel(Dialog_quick_order)
        self.label_long_info.setText("")
        self.label_long_info.setObjectName("label_long_info")
        self.verticalLayout_7.addWidget(self.label_long_info)
        self.horizontalLayout_8.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_short = QtWidgets.QPushButton(Dialog_quick_order)
        self.pushButton_short.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_short.sizePolicy().hasHeightForWidth())
        self.pushButton_short.setSizePolicy(sizePolicy)
        self.pushButton_short.setObjectName("pushButton_short")
        self.verticalLayout_8.addWidget(self.pushButton_short)
        self.label_short_info = QtWidgets.QLabel(Dialog_quick_order)
        self.label_short_info.setText("")
        self.label_short_info.setObjectName("label_short_info")
        self.verticalLayout_8.addWidget(self.label_short_info)
        self.horizontalLayout_8.addLayout(self.verticalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.spinBox_toler = QtWidgets.QSpinBox(Dialog_quick_order)
        self.spinBox_toler.setEnabled(False)
        self.spinBox_toler.setMinimum(-99)
        self.spinBox_toler.setObjectName("spinBox_toler")
        self.verticalLayout_2.addWidget(self.spinBox_toler)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_10 = QtWidgets.QLabel(Dialog_quick_order)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.comboBox_VaildType = QtWidgets.QComboBox(Dialog_quick_order)
        self.comboBox_VaildType.setEnabled(False)
        self.comboBox_VaildType.setObjectName("comboBox_VaildType")
        self.comboBox_VaildType.addItem("")
        self.comboBox_VaildType.addItem("")
        self.comboBox_VaildType.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox_VaildType)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.checkBox_OrderOptions = QtWidgets.QCheckBox(Dialog_quick_order)
        self.checkBox_OrderOptions.setEnabled(False)
        self.checkBox_OrderOptions.setObjectName("checkBox_OrderOptions")
        self.horizontalLayout_7.addWidget(self.checkBox_OrderOptions)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.tableWidget_Price = QInfoWidget(Dialog_quick_order)
        self.tableWidget_Price.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_Price.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_Price.setObjectName("tableWidget_Price")
        self.tableWidget_Price.setColumnCount(9)
        self.tableWidget_Price.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Price.setHorizontalHeaderItem(8, item)
        self.tableWidget_Price.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget_Price.verticalHeader().setVisible(False)
        self.verticalLayout_5.addWidget(self.tableWidget_Price)
        self.pushButton_price_to_middle = QtWidgets.QPushButton(Dialog_quick_order)
        self.pushButton_price_to_middle.setEnabled(False)
        self.pushButton_price_to_middle.setObjectName("pushButton_price_to_middle")
        self.verticalLayout_5.addWidget(self.pushButton_price_to_middle)
        self.horizontalLayout_12.addLayout(self.verticalLayout_5)
        self.label.setBuddy(self.lineEdit_ProdCode)
        self.label_2.setBuddy(self.spinBox_Qty)

        self.retranslateUi(Dialog_quick_order)
        self.checkBox_Lock.toggled['bool'].connect(self.spinBox_Qty.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.pushButton_long.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.pushButton_short.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.pushButton_price_to_middle.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.spinBox_toler.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.comboBox_VaildType.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.checkBox_OrderOptions.setEnabled)
        self.checkBox_Lock.toggled['bool'].connect(self.lineEdit_ProdCode.setDisabled)
        self.checkBox_Lock.toggled['bool'].connect(self.pushButton_close_position.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog_quick_order)

    def retranslateUi(self, Dialog_quick_order):
        _translate = QtCore.QCoreApplication.translate
        Dialog_quick_order.setWindowTitle(_translate("Dialog_quick_order", "SP QUICK ORDER"))
        self.label.setText(_translate("Dialog_quick_order", "代号"))
        self.checkBox_Lock.setText(_translate("Dialog_quick_order", "锁定"))
        self.label_2.setText(_translate("Dialog_quick_order", "数量"))
        self.label_3.setText(_translate("Dialog_quick_order", "持仓："))
        self.label_4.setText(_translate("Dialog_quick_order", "持仓盈亏："))
        self.label_5.setText(_translate("Dialog_quick_order", "平仓盈亏："))
        self.pushButton_close_position.setText(_translate("Dialog_quick_order", "一键平仓"))
        self.pushButton_long.setText(_translate("Dialog_quick_order", "追价买入"))
        self.pushButton_short.setText(_translate("Dialog_quick_order", "追价沽出"))
        self.label_9.setText(_translate("Dialog_quick_order", "追价点数"))
        self.label_10.setText(_translate("Dialog_quick_order", "追价类型"))
        self.comboBox_VaildType.setItemText(0, _translate("Dialog_quick_order", "即日"))
        self.comboBox_VaildType.setItemText(1, _translate("Dialog_quick_order", "成交并取消"))
        self.comboBox_VaildType.setItemText(2, _translate("Dialog_quick_order", "成交或取消"))
        self.checkBox_OrderOptions.setText(_translate("Dialog_quick_order", "T+1"))
        item = self.tableWidget_Price.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_quick_order", "删"))
        item = self.tableWidget_Price.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_quick_order", "买入"))
        item = self.tableWidget_Price.horizontalHeaderItem(2)
        item.setText(_translate("Dialog_quick_order", "市场"))
        item = self.tableWidget_Price.horizontalHeaderItem(3)
        item.setText(_translate("Dialog_quick_order", "加"))
        item = self.tableWidget_Price.horizontalHeaderItem(4)
        item.setText(_translate("Dialog_quick_order", "价格"))
        item = self.tableWidget_Price.horizontalHeaderItem(5)
        item.setText(_translate("Dialog_quick_order", "加"))
        item = self.tableWidget_Price.horizontalHeaderItem(6)
        item.setText(_translate("Dialog_quick_order", "市场"))
        item = self.tableWidget_Price.horizontalHeaderItem(7)
        item.setText(_translate("Dialog_quick_order", "沽出"))
        item = self.tableWidget_Price.horizontalHeaderItem(8)
        item.setText(_translate("Dialog_quick_order", "删"))
        self.pushButton_price_to_middle.setText(_translate("Dialog_quick_order", "置中"))

from baseitems import QInfoWidget
