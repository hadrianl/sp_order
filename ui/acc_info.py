# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acc_info.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_acc_info(object):
    def setupUi(self, Form_acc_info):
        Form_acc_info.setObjectName("Form_acc_info")
        Form_acc_info.resize(1161, 322)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(Form_acc_info)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tableWidget_acc_info = QInfoWidget(Form_acc_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_acc_info.sizePolicy().hasHeightForWidth())
        self.tableWidget_acc_info.setSizePolicy(sizePolicy)
        self.tableWidget_acc_info.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tableWidget_acc_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_acc_info.setColumnCount(1)
        self.tableWidget_acc_info.setObjectName("tableWidget_acc_info")
        self.tableWidget_acc_info.setRowCount(14)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_acc_info.setVerticalHeaderItem(13, item)
        self.tableWidget_acc_info.horizontalHeader().setVisible(False)
        self.tableWidget_acc_info.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_acc_info.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_9.addWidget(self.tableWidget_acc_info)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_Order_Stoploss = QtWidgets.QPushButton(Form_acc_info)
        self.pushButton_Order_Stoploss.setCheckable(True)
        self.pushButton_Order_Stoploss.setObjectName("pushButton_Order_Stoploss")
        self.horizontalLayout_11.addWidget(self.pushButton_Order_Stoploss)
        self.pushButton_QuickOrder = QtWidgets.QPushButton(Form_acc_info)
        self.pushButton_QuickOrder.setCheckable(True)
        self.pushButton_QuickOrder.setObjectName("pushButton_QuickOrder")
        self.horizontalLayout_11.addWidget(self.pushButton_QuickOrder)
        self.horizontalLayout.addLayout(self.horizontalLayout_11)
        self.pushButton_tradesession = QtWidgets.QPushButton(Form_acc_info)
        self.pushButton_tradesession.setObjectName("pushButton_tradesession")
        self.horizontalLayout.addWidget(self.pushButton_tradesession)
        self.pushButton_mt4_order = QtWidgets.QPushButton(Form_acc_info)
        self.pushButton_mt4_order.setObjectName("pushButton_mt4_order")
        self.horizontalLayout.addWidget(self.pushButton_mt4_order)
        self.checkBox_follow_orders = QtWidgets.QCheckBox(Form_acc_info)
        self.checkBox_follow_orders.setObjectName("checkBox_follow_orders")
        self.horizontalLayout.addWidget(self.checkBox_follow_orders)
        self.checkBox_test = QtWidgets.QCheckBox(Form_acc_info)
        self.checkBox_test.setObjectName("checkBox_test")
        self.horizontalLayout.addWidget(self.checkBox_test)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox_wechat_info = QtWidgets.QCheckBox(Form_acc_info)
        self.checkBox_wechat_info.setObjectName("checkBox_wechat_info")
        self.horizontalLayout.addWidget(self.checkBox_wechat_info)
        self.toolButton_update_info = QtWidgets.QToolButton(Form_acc_info)
        self.toolButton_update_info.setMinimumSize(QtCore.QSize(10, 10))
        self.toolButton_update_info.setMaximumSize(QtCore.QSize(15, 15))
        self.toolButton_update_info.setStyleSheet("border-image: url(:/icon/update.png);")
        self.toolButton_update_info.setText("")
        self.toolButton_update_info.setObjectName("toolButton_update_info")
        self.horizontalLayout.addWidget(self.toolButton_update_info)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidget_acc_info = QtWidgets.QTabWidget(Form_acc_info)
        self.tabWidget_acc_info.setObjectName("tabWidget_acc_info")
        self.tab_orders = QtWidgets.QWidget()
        self.tab_orders.setObjectName("tab_orders")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tab_orders)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_del_order = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_del_order.setObjectName("pushButton_del_order")
        self.horizontalLayout_2.addWidget(self.pushButton_del_order)
        self.pushButton_activate_order = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_activate_order.setObjectName("pushButton_activate_order")
        self.horizontalLayout_2.addWidget(self.pushButton_activate_order)
        self.pushButton_inactivate_order = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_inactivate_order.setObjectName("pushButton_inactivate_order")
        self.horizontalLayout_2.addWidget(self.pushButton_inactivate_order)
        self.pushButton_del_all_orders = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_del_all_orders.setObjectName("pushButton_del_all_orders")
        self.horizontalLayout_2.addWidget(self.pushButton_del_all_orders)
        self.pushButton_activate_all_orders = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_activate_all_orders.setObjectName("pushButton_activate_all_orders")
        self.horizontalLayout_2.addWidget(self.pushButton_activate_all_orders)
        self.pushButton_inactivate_all_orders = QtWidgets.QPushButton(self.tab_orders)
        self.pushButton_inactivate_all_orders.setObjectName("pushButton_inactivate_all_orders")
        self.horizontalLayout_2.addWidget(self.pushButton_inactivate_all_orders)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget_orders = QInfoWidget(self.tab_orders)
        self.tableWidget_orders.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_orders.setObjectName("tableWidget_orders")
        self.tableWidget_orders.setColumnCount(14)
        self.tableWidget_orders.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orders.setHorizontalHeaderItem(13, item)
        self.tableWidget_orders.horizontalHeader().setDefaultSectionSize(65)
        self.tableWidget_orders.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_orders.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_orders.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget_orders)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.tabWidget_acc_info.addTab(self.tab_orders, "")
        self.tab_pos = QtWidgets.QWidget()
        self.tab_pos.setObjectName("tab_pos")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab_pos)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_close_order = QtWidgets.QPushButton(self.tab_pos)
        self.pushButton_close_order.setObjectName("pushButton_close_order")
        self.horizontalLayout_3.addWidget(self.pushButton_close_order)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tableWidget_pos = QInfoWidget(self.tab_pos)
        self.tableWidget_pos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_pos.setObjectName("tableWidget_pos")
        self.tableWidget_pos.setColumnCount(14)
        self.tableWidget_pos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_pos.setHorizontalHeaderItem(13, item)
        self.tableWidget_pos.horizontalHeader().setDefaultSectionSize(65)
        self.tableWidget_pos.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_pos.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_pos.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableWidget_pos)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.tabWidget_acc_info.addTab(self.tab_pos, "")
        self.tab_trades = QtWidgets.QWidget()
        self.tab_trades.setObjectName("tab_trades")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_trades)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget_trades = QInfoWidget(self.tab_trades)
        self.tableWidget_trades.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_trades.setObjectName("tableWidget_trades")
        self.tableWidget_trades.setColumnCount(14)
        self.tableWidget_trades.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_trades.setHorizontalHeaderItem(13, item)
        self.tableWidget_trades.horizontalHeader().setDefaultSectionSize(65)
        self.tableWidget_trades.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_trades.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_trades.verticalHeader().setVisible(False)
        self.horizontalLayout_4.addWidget(self.tableWidget_trades)
        self.tabWidget_acc_info.addTab(self.tab_trades, "")
        self.tab_bal = QtWidgets.QWidget()
        self.tab_bal.setObjectName("tab_bal")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_bal)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget_bal = QInfoWidget(self.tab_bal)
        self.tableWidget_bal.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_bal.setObjectName("tableWidget_bal")
        self.tableWidget_bal.setColumnCount(8)
        self.tableWidget_bal.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_bal.setHorizontalHeaderItem(7, item)
        self.tableWidget_bal.horizontalHeader().setDefaultSectionSize(65)
        self.tableWidget_bal.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_bal.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_bal.verticalHeader().setVisible(False)
        self.horizontalLayout_5.addWidget(self.tableWidget_bal)
        self.tabWidget_acc_info.addTab(self.tab_bal, "")
        self.tab_ccy = QtWidgets.QWidget()
        self.tab_ccy.setObjectName("tab_ccy")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_ccy)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tableWidget_ccy_rate = QInfoWidget(self.tab_ccy)
        self.tableWidget_ccy_rate.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_ccy_rate.setObjectName("tableWidget_ccy_rate")
        self.tableWidget_ccy_rate.setColumnCount(1)
        self.tableWidget_ccy_rate.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ccy_rate.setHorizontalHeaderItem(0, item)
        self.tableWidget_ccy_rate.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_ccy_rate.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget_ccy_rate.verticalHeader().setMinimumSectionSize(15)
        self.tableWidget_ccy_rate.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_6.addWidget(self.tableWidget_ccy_rate)
        self.tabWidget_acc_info.addTab(self.tab_ccy, "")
        self.verticalLayout_3.addWidget(self.tabWidget_acc_info)
        self.horizontalLayout_9.addLayout(self.verticalLayout_3)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_9)

        self.retranslateUi(Form_acc_info)
        self.tabWidget_acc_info.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form_acc_info)

    def retranslateUi(self, Form_acc_info):
        _translate = QtCore.QCoreApplication.translate
        Form_acc_info.setWindowTitle(_translate("Form_acc_info", "SP ACCOUNT"))
        item = self.tableWidget_acc_info.verticalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "购买力"))
        item = self.tableWidget_acc_info.verticalHeaderItem(1)
        item.setText(_translate("Form_acc_info", "资产净值"))
        item = self.tableWidget_acc_info.verticalHeaderItem(2)
        item.setText(_translate("Form_acc_info", "追收金额"))
        item = self.tableWidget_acc_info.verticalHeaderItem(3)
        item.setText(_translate("Form_acc_info", "商品盈亏"))
        item = self.tableWidget_acc_info.verticalHeaderItem(4)
        item.setText(_translate("Form_acc_info", "基本保证金"))
        item = self.tableWidget_acc_info.verticalHeaderItem(5)
        item.setText(_translate("Form_acc_info", "维持保证金"))
        item = self.tableWidget_acc_info.verticalHeaderItem(6)
        item.setText(_translate("Form_acc_info", "保证金水平"))
        item = self.tableWidget_acc_info.verticalHeaderItem(7)
        item.setText(_translate("Form_acc_info", "最高保证金"))
        item = self.tableWidget_acc_info.verticalHeaderItem(8)
        item.setText(_translate("Form_acc_info", "时段"))
        item = self.tableWidget_acc_info.verticalHeaderItem(9)
        item.setText(_translate("Form_acc_info", "现金结余"))
        item = self.tableWidget_acc_info.verticalHeaderItem(10)
        item.setText(_translate("Form_acc_info", "信贷限额"))
        item = self.tableWidget_acc_info.verticalHeaderItem(11)
        item.setText(_translate("Form_acc_info", "控制级数"))
        item = self.tableWidget_acc_info.verticalHeaderItem(12)
        item.setText(_translate("Form_acc_info", "保证金类别"))
        item = self.tableWidget_acc_info.verticalHeaderItem(13)
        item.setText(_translate("Form_acc_info", "经纪"))
        self.pushButton_Order_Stoploss.setText(_translate("Form_acc_info", "下单"))
        self.pushButton_QuickOrder.setText(_translate("Form_acc_info", "快速点击下单"))
        self.pushButton_tradesession.setText(_translate("Form_acc_info", "交易会话"))
        self.pushButton_mt4_order.setText(_translate("Form_acc_info", "MT4 ORDER"))
        self.checkBox_follow_orders.setText(_translate("Form_acc_info", "跟单"))
        self.checkBox_test.setText(_translate("Form_acc_info", "test"))
        self.checkBox_wechat_info.setText(_translate("Form_acc_info", "微信推送"))
        self.pushButton_del_order.setText(_translate("Form_acc_info", "删除"))
        self.pushButton_activate_order.setText(_translate("Form_acc_info", "生效"))
        self.pushButton_inactivate_order.setText(_translate("Form_acc_info", "无效"))
        self.pushButton_del_all_orders.setText(_translate("Form_acc_info", "全部删除"))
        self.pushButton_activate_all_orders.setText(_translate("Form_acc_info", "全部生效"))
        self.pushButton_inactivate_all_orders.setText(_translate("Form_acc_info", "全部无效"))
        item = self.tableWidget_orders.horizontalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "买卖指示"))
        item = self.tableWidget_orders.horizontalHeaderItem(1)
        item.setText(_translate("Form_acc_info", "代号"))
        item = self.tableWidget_orders.horizontalHeaderItem(2)
        item.setText(_translate("Form_acc_info", "名称"))
        item = self.tableWidget_orders.horizontalHeaderItem(3)
        item.setText(_translate("Form_acc_info", "买入余数"))
        item = self.tableWidget_orders.horizontalHeaderItem(4)
        item.setText(_translate("Form_acc_info", "沽出余数"))
        item = self.tableWidget_orders.horizontalHeaderItem(5)
        item.setText(_translate("Form_acc_info", "价格"))
        item = self.tableWidget_orders.horizontalHeaderItem(6)
        item.setText(_translate("Form_acc_info", "有效期"))
        item = self.tableWidget_orders.horizontalHeaderItem(7)
        item.setText(_translate("Form_acc_info", "条件"))
        item = self.tableWidget_orders.horizontalHeaderItem(8)
        item.setText(_translate("Form_acc_info", "状况"))
        item = self.tableWidget_orders.horizontalHeaderItem(9)
        item.setText(_translate("Form_acc_info", "已成交"))
        item = self.tableWidget_orders.horizontalHeaderItem(10)
        item.setText(_translate("Form_acc_info", "原发者"))
        item = self.tableWidget_orders.horizontalHeaderItem(11)
        item.setText(_translate("Form_acc_info", "参考"))
        item = self.tableWidget_orders.horizontalHeaderItem(12)
        item.setText(_translate("Form_acc_info", "时间标记"))
        item = self.tableWidget_orders.horizontalHeaderItem(13)
        item.setText(_translate("Form_acc_info", "外部指示#"))
        self.tabWidget_acc_info.setTabText(self.tabWidget_acc_info.indexOf(self.tab_orders), _translate("Form_acc_info", "订单"))
        self.pushButton_close_order.setText(_translate("Form_acc_info", "平仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "代号"))
        item = self.tableWidget_pos.horizontalHeaderItem(1)
        item.setText(_translate("Form_acc_info", "名称"))
        item = self.tableWidget_pos.horizontalHeaderItem(2)
        item.setText(_translate("Form_acc_info", "上日持仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(3)
        item.setText(_translate("Form_acc_info", "存取"))
        item = self.tableWidget_pos.horizontalHeaderItem(4)
        item.setText(_translate("Form_acc_info", "今日长仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(5)
        item.setText(_translate("Form_acc_info", "今日短仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(6)
        item.setText(_translate("Form_acc_info", "今日净仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(7)
        item.setText(_translate("Form_acc_info", "净仓"))
        item = self.tableWidget_pos.horizontalHeaderItem(8)
        item.setText(_translate("Form_acc_info", "市价"))
        item = self.tableWidget_pos.horizontalHeaderItem(9)
        item.setText(_translate("Form_acc_info", "盈亏"))
        item = self.tableWidget_pos.horizontalHeaderItem(10)
        item.setText(_translate("Form_acc_info", "前收盘价"))
        item = self.tableWidget_pos.horizontalHeaderItem(11)
        item.setText(_translate("Form_acc_info", "参考兑换率"))
        item = self.tableWidget_pos.horizontalHeaderItem(12)
        item.setText(_translate("Form_acc_info", "盈亏"))
        item = self.tableWidget_pos.horizontalHeaderItem(13)
        item.setText(_translate("Form_acc_info", "合约值"))
        self.tabWidget_acc_info.setTabText(self.tabWidget_acc_info.indexOf(self.tab_pos), _translate("Form_acc_info", "持仓"))
        item = self.tableWidget_trades.horizontalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "代号"))
        item = self.tableWidget_trades.horizontalHeaderItem(1)
        item.setText(_translate("Form_acc_info", "名称"))
        item = self.tableWidget_trades.horizontalHeaderItem(2)
        item.setText(_translate("Form_acc_info", "买入量"))
        item = self.tableWidget_trades.horizontalHeaderItem(3)
        item.setText(_translate("Form_acc_info", "沽出量"))
        item = self.tableWidget_trades.horizontalHeaderItem(4)
        item.setText(_translate("Form_acc_info", "成交价"))
        item = self.tableWidget_trades.horizontalHeaderItem(5)
        item.setText(_translate("Form_acc_info", "成交#"))
        item = self.tableWidget_trades.horizontalHeaderItem(6)
        item.setText(_translate("Form_acc_info", "状况"))
        item = self.tableWidget_trades.horizontalHeaderItem(7)
        item.setText(_translate("Form_acc_info", "原发者"))
        item = self.tableWidget_trades.horizontalHeaderItem(8)
        item.setText(_translate("Form_acc_info", "参考"))
        item = self.tableWidget_trades.horizontalHeaderItem(9)
        item.setText(_translate("Form_acc_info", "时间"))
        item = self.tableWidget_trades.horizontalHeaderItem(10)
        item.setText(_translate("Form_acc_info", "指示价"))
        item = self.tableWidget_trades.horizontalHeaderItem(11)
        item.setText(_translate("Form_acc_info", "指示#"))
        item = self.tableWidget_trades.horizontalHeaderItem(12)
        item.setText(_translate("Form_acc_info", "外部指示#"))
        item = self.tableWidget_trades.horizontalHeaderItem(13)
        item.setText(_translate("Form_acc_info", "成交记录#"))
        self.tabWidget_acc_info.setTabText(self.tabWidget_acc_info.indexOf(self.tab_trades), _translate("Form_acc_info", "成交结算"))
        item = self.tableWidget_bal.horizontalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "货币"))
        item = self.tableWidget_bal.horizontalHeaderItem(1)
        item.setText(_translate("Form_acc_info", "上日结余"))
        item = self.tableWidget_bal.horizontalHeaderItem(2)
        item.setText(_translate("Form_acc_info", "未交收"))
        item = self.tableWidget_bal.horizontalHeaderItem(3)
        item.setText(_translate("Form_acc_info", "今日存取"))
        item = self.tableWidget_bal.horizontalHeaderItem(4)
        item.setText(_translate("Form_acc_info", "现金结余"))
        item = self.tableWidget_bal.horizontalHeaderItem(5)
        item.setText(_translate("Form_acc_info", "未兑现"))
        item = self.tableWidget_bal.horizontalHeaderItem(6)
        item.setText(_translate("Form_acc_info", "参考兑换率"))
        item = self.tableWidget_bal.horizontalHeaderItem(7)
        item.setText(_translate("Form_acc_info", "现金"))
        self.tabWidget_acc_info.setTabText(self.tabWidget_acc_info.indexOf(self.tab_bal), _translate("Form_acc_info", "现金结余"))
        item = self.tableWidget_ccy_rate.horizontalHeaderItem(0)
        item.setText(_translate("Form_acc_info", "参考兑换率(HKD)"))
        self.tabWidget_acc_info.setTabText(self.tabWidget_acc_info.indexOf(self.tab_ccy), _translate("Form_acc_info", "参考汇率"))

from baseitems import QInfoWidget
import ui.order_rc
