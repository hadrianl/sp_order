#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/30 0030 11:40
# @Author  : Hadrianl 
# @File    : Spfunc.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.Qt import QDialog, QDesktopWidget, QTableWidget, QIcon, QColor, QFont, QMessageBox,pyqtSignal, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtSql

from ui.order_dialog import Ui_Dialog_order
from ui.acc_info import Ui_Form_acc_info
from ui.sp_login import Ui_Dialog_sp_login
from ui.quick_order_dialog import Ui_Dialog_quick_order
from ui.order_comfirm_dialog import Ui_Dialog_order_comfirm
from ui.close_position_dialog import Ui_Dialog_close_position
from ui.quick_stoploss_dialog import Ui_Dialog_quick_stoploss
from ui.order_stoploss_dialog import Ui_Dialog_order_stoploss
from baseitems import QPubOrder, QSubOrder, QWechatInfo
from ui.order_assistant_widget import Ui_Form_OrderAssistant
from ui.time_widget import Ui_Form_time
from spapi.spAPI import *
from spapi.conf.util import ORDER_VALIDTYPE
import os
import pickle
import datetime as dt
import time
from utils import get_order_cond
from baseitems import QData
from functools import reduce
from operator import add
from queue import Queue
from threading import Thread
import pymysql as pm
import pandas as pd
from extra.calc import HS

class QSqlTable(QtWidgets.QTableView):
    class QDataModel(QtSql.QSqlTableModel):
        def __init__(self, parent=None, db=None):
            QtSql.QSqlTableModel.__init__(self, parent, db)

        def data(self, index: QtCore.QModelIndex, role: int = ...):
            if (role == Qt.Qt.BackgroundColorRole):
                color = None
                if index.row() % 2 == 1:
                    color = QColor('#F2F2F2')
                if index.column() == 7:
                    profit = self.data(index, role=Qt.Qt.DisplayRole)
                    color = QColor('#FF0000') if profit >=0 else QColor('#00FF00')
                return color

            if role == Qt.Qt.ForegroundRole and index.column() == 9:
                order_type = self.data(index, role=Qt.Qt.DisplayRole)
                color = {0:QColor('#FF0000'), 2:QColor('#FF0000'), 4:QColor('#FF0000'), 1: QColor('#00FF00'), 3: QColor('#00FF00'), 5:QColor('#00FF00')}.get(order_type)
                return color

            return QtSql.QSqlTableModel.data(self, index, role)


    def __init__(self, table='order_detail'):
        QtWidgets.QTableView.__init__(self, None)
        # self.setWindowFlags(Qt.Qt.Window)
        self.setWindowTitle(table)
        self._db= QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self._db.setHostName('192.168.2.226')
        self._db.setPort(3306)
        self._db.setUserName('kairuitouzi')
        self._db.setPassword('kairuitouzi')
        self._db.setDatabaseName('carry_investment')
        if self._db.open():
            self._model = self.QDataModel(self, self._db)
            self._model.setTable(table)
            self._model.select()
            self._model.sort(3, Qt.Qt.DescendingOrder)
            self.setModel(self._model)
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.verticalHeader().hide()
            self.resize(800, 500)
            self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.show()
        else:
            raise Exception(self._db.lastError().text())


class AccInfoWidget(QtWidgets.QWidget, Ui_Form_acc_info):
    warning_sig = pyqtSignal(str, str)
    info_sig = pyqtSignal(str, str)
    acc_info_sig = pyqtSignal(float)  # 更新最新盈亏
    pos_info_sig = pyqtSignal(dict)  # 仓位更新信号，用于触发持仓的更新等
    order_info_sig = pyqtSignal(dict)  # 下单的订单信号，用于更新止损止盈状态等
    price_update_sig = pyqtSignal(dict)  # 价格更新信号
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_acc_info.__init__(self)
        self.setupUi(self)
        self.time = TimeWidget(self)
        self.message = QMessageBox(self)
        self.message.setModal(True)
        self.data = QData(self)
        self.PL = {}
        self.init_signal()
        self.info_update = [self.refresh_acc_info,
                            self.refresh_orders,
                            self.refresh_positions,
                            self.refresh_trades,
                            self.refresh_accbals,
                            self.refresh_ccy_rate]

    def init_signal(self):
        self.price_update_sig.connect(self.update_pos_info)
        self.warning_sig.connect(lambda title, text: self.message.warning(self.parent(), title, text))
        self.info_sig.connect(lambda title, text: self.message.information(self.parent(), title, text))
        self.acc_info_sig.connect(self.update_acc_info)
        # ---------------------订单的处理函数连接按钮----------------------------------
        self.pushButton_del_order.released.connect(self._del_current_selected_order)
        self.pushButton_activate_order.released.connect(self._activate_selected_order)
        self.pushButton_inactivate_order.released.connect(self._inactivate_selected_order)
        self.pushButton_del_all_orders.released.connect(self._del_all_orders)
        self.pushButton_activate_all_orders.released.connect(self._activate_all_orders)
        self.pushButton_inactivate_all_orders.released.connect(self._inactivate_all_orders)
        # -------------------------------------------------------------------------------
        self.toolButton_update_info.released.connect(lambda: [subscribe_price(p, 1) for p in self.data.sub_list])
        self.toolButton_update_info.released.connect(lambda: [func() for func in self.info_update])

        self.pushButton_close_order.mouseReleaseEvent = lambda e:self._close_position(e)

    def update_pos_info(self, price_dict):  # 根据price来更新持仓盈亏等
        for t in range(self.tableWidget_pos.rowCount()):
            prodcode = price_dict['ProdCode'].decode()
            if  prodcode == self.tableWidget_pos.item(t, 0).text():
                # AccInfo.tableWidget_pos.update_item_sig.emit(t, 8, str(price_dict['Last'][0]))
                pos = self.data.Pos[prodcode]
                net_qty = pos['Qty'] + pos['LongQty'] - pos['ShortQty'] if pos['LongShort'] ==b'B' else -pos['Qty'] + pos['LongQty'] - pos['ShortQty']
                totalamt = pos['TotalAmt'] if pos['LongShort'] ==b'B' else -pos['TotalAmt']
                net_price = (totalamt + pos['LongTotalAmt'] - pos['ShortTotalAmt']) / net_qty if net_qty != 0 else (totalamt + pos['LongTotalAmt'] - pos['ShortTotalAmt'])
                self.tableWidget_pos.item(t, 8).setText(str(price_dict['Last'][0]))
                leverage = int(self.tableWidget_pos.item(t, 13).text())
                PL = (net_qty * (price_dict['Last'][0] - net_price)) * leverage if net_qty != 0 else (0 - net_price) * leverage
                self.tableWidget_pos.item(t, 9).setText(f"{PL:.2f}HKD")
                self.tableWidget_pos.viewport().update()
                self.PL[prodcode] = PL
                self.acc_info_sig.emit(sum(self.PL.values()))

    def update_acc_info(self, PL):  # 实时更新持仓的盈亏
        ccy = self.data.Acc['BaseCcy'].decode()
        BuyingPower = self.data.Acc['CashBal'] + self.data.Acc['CreditLimit'] + PL - self.data.Acc['IMargin']
        NAV = self.data.Acc['CashBal'] + PL
        MarginCall = self.data.Acc['IMargin'] - (self.data.Acc['CashBal'] + self.data.Acc['CreditLimit'] + PL) if (self.data.Acc['CashBal'] + self.data.Acc['CreditLimit'] + PL) < self.data.Acc['IMargin'] else 0
        CommodityPL = PL

        try:
            MarginLevel = (self.data.Acc['CashBal'] + self.data.Acc['CreditLimit'] + PL) / \
                          self.data.Acc['IMargin']
            ML = f'{MarginLevel:.2%}'
        except ZeroDivisionError:
            ML = '-'

        self.tableWidget_acc_info.setItem(0, 0, QTableWidgetItem(f"{BuyingPower:,} {ccy}"))
        self.tableWidget_acc_info.setItem(1, 0, QTableWidgetItem(f"{NAV:,} {ccy}"))
        self.tableWidget_acc_info.setItem(2, 0, QTableWidgetItem(f"{MarginCall:,} {ccy}"))
        self.tableWidget_acc_info.setItem(3, 0, QTableWidgetItem(f"{CommodityPL:,.2f} {ccy}"))
        self.tableWidget_acc_info.setItem(6, 0, QTableWidgetItem(ML))
        # self.tableWidget_acc_info.setItem(0, 0, f"{BuyingPower:,} {ccy}")

    def __get_current_order_info(self):
        row = self.tableWidget_orders.currentRow()
        if row >= 0:
            order_no = int(self.tableWidget_orders.item(self.tableWidget_orders.currentRow(), 0).text())
            prodcode = self.tableWidget_orders.item(self.tableWidget_orders.currentRow(), 1).text()
            return order_no, prodcode
        else:
            raise Exception('未选择订单')

    def _del_current_selected_order(self):
        try:
            order_no, prodcode = self.__get_current_order_info()
            delete_order_by(order_no, prodcode)
        except Exception as e:
            QMessageBox.warning(self, 'WARING-删除', str(e))

    def _activate_selected_order(self):
        try:
            order_no, prodcode = self.__get_current_order_info()
            activate_order_by(order_no)
        except Exception as e:
            QMessageBox.warning(self, 'WARING-生效', str(e))

    def _inactivate_selected_order(self):
        try:
            order_no, prodcode = self.__get_current_order_info()
            inactivate_order_by(order_no)
        except Exception as e:
            QMessageBox.warning(self, 'WARING-失效', str(e))

    def _del_all_orders(self):
        try:
            delete_all_orders()
        except Exception as e:
            QMessageBox.warning(self, 'WARING-删除', str(e))

    def _activate_all_orders(self):
        try:
            activate_all_orders()
        except Exception as e:
            QMessageBox.warning(self, 'WARING-生效', str(e))

    def _inactivate_all_orders(self):
        try:
            inactivate_all_orders()
        except Exception as e:
            QMessageBox.warning(self, 'WARING-失效', str(e))

    def __get_current_pos_info(self):
        row = self.tableWidget_pos.currentRow()
        if row >= 0:
            prodcode = self.tableWidget_pos.item(self.tableWidget_pos.currentRow(), 0).text()
            pos = get_pos_by_product(prodcode)
            net_pos = (pos.Qty + pos.LongQty - pos.ShortQty) if pos.LongShort == b'B' else (
                        -pos.Qty + pos.LongQty - pos.ShortQty)
            return prodcode, net_pos
        else:
            raise Exception('请选择需要平仓仓位')

    def _close_position(self, e):
        try:
            prodcode, net_pos = self.__get_current_pos_info()
            if net_pos > 0:
                ClosePositionDialog('S', prodcode, net_pos, 10, self) if e.button() == Qt.Qt.LeftButton else ClosePositionDialog('S', prodcode, net_pos, 10, self).close_position('S')
            elif net_pos < 0:
                ClosePositionDialog('B', prodcode, -net_pos, 10, self) if e.button() == Qt.Qt.LeftButton else ClosePositionDialog('B', prodcode, -net_pos, 10, self).close_position('B')
            else:
                raise Exception('净仓为0')
        except Exception as e:
            QMessageBox.warning(self, 'WARING-平仓', str(e))

    # -------------------------------------------账户的更新函数--------------------------------------------------------
    def refresh_acc_info(self):
        try:
            acc_info = get_acc_info()
            self._refresh_acc_info(acc_info)
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新ACC', str(e))

    def _refresh_acc_info(self, a):
        self.data._update_acc(a)
        acc_info_dict = self.data.Acc
        base_ccy = acc_info_dict['BaseCcy'].decode()
        ctrllevel_dict = {0: '正常', 1: '停止交易', 2: '暂停', 3: '冻结户口'}
        try:
            MarginLevel = (acc_info_dict['CashBal'] + acc_info_dict['CreditLimit'] + acc_info_dict['CommodityPL']) / \
                          acc_info_dict['IMargin']
            ML = f'{MarginLevel:.2%}'
        except ZeroDivisionError:
            ML = '-'
        acc_info = [f"{acc_info_dict['BuyingPower']:,} {base_ccy}",
                    f"{acc_info_dict['NAV']:,} {base_ccy}",
                    f"{acc_info_dict['MarginCall']:,} {base_ccy}",
                    f"{acc_info_dict['CommodityPL']:,} {base_ccy}",
                    f"{acc_info_dict['IMargin']:,} {base_ccy}",
                    f"{acc_info_dict['MMargin']:,} {base_ccy}",
                    ML,
                    f"{acc_info_dict['MaxMargin']:,} {base_ccy}",
                    f"{ord(acc_info_dict['MarginPeriod'])}",
                    f"{acc_info_dict['CashBal']:,} {base_ccy}",
                    f"{acc_info_dict['CreditLimit']:,} {base_ccy}",
                    f"{ctrllevel_dict[ord(acc_info_dict['CtrlLevel'])]}",
                    acc_info_dict['MarginClass'].decode('GBK'),
                    acc_info_dict['AEId'].decode('GBK')
                    ]
        for i, s in zip(range(14), map(str, acc_info)):
            self.tableWidget_acc_info.setItem(i, 0, QTableWidgetItem(s))
        self.tableWidget_acc_info.viewport().update()

        return acc_info_dict

    def refresh_orders(self):
        try:
            orders_array = get_orders_by_array()
            orders = []
            for i in range(self.tableWidget_orders.rowCount()):
                self.tableWidget_orders.removeRow(0)

            for o in orders_array:
                orders.append(self._refresh_order(o))

        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新ORDER', str(e))

    def _refresh_order(self, o):
        self.data._update_order(o)
        order_dict = self.data.Order[o.IntOrderNo]
        self.order_info_sig.emit(order_dict)
        r = 0
        for i in range(self.tableWidget_orders.rowCount()):
            if order_dict['IntOrderNo'] == int(self.tableWidget_orders.item(i, 0).text()):
                r = i
                break
        else:
            self.tableWidget_orders.insertRow(0)

        cond = get_order_cond(o)
        prodcode = order_dict['ProdCode'].decode()
        order_info = [order_dict['IntOrderNo'],
                      prodcode,
                      self.data.Product.get(prodcode,''),
                      order_dict['Qty'] if order_dict['BuySell'].decode() == 'B' else '',
                      order_dict['Qty'] if order_dict['BuySell'].decode() == 'S' else '',
                      f"{order_dict['Price']:,}",
                      dt.datetime.fromtimestamp(order_dict['ValidTime']),
                      cond,
                      ORDER_STATUS[order_dict['Status']],
                      order_dict['TradedQty'],
                      order_dict['Initiator'].decode(),
                      order_dict['Ref'].decode(),
                      dt.datetime.fromtimestamp(order_dict['TimeStamp']),
                      order_dict['ExtOrderNo']]

        for i, s in zip(range(14), map(str, order_info)):
            self.tableWidget_orders.setItem(r, i, QTableWidgetItem(s))
        self.tableWidget_orders.viewport().update()

        if order_dict['Status'] in [10]:
            self.tableWidget_orders.removeRow(r)

        if order_dict['Status'] not in [0, 4, 5, 6, 7]:
            w_info = f"    {order_info[12]}\n" \
                     f"    跟随{order_info[11]}\n" \
                     f"代码:{order_info[1]}\n" \
                     f"买卖:{order_dict['BuySell'].decode()}\n" \
                     f"数量:{order_dict['Qty']}\n" \
                     f"价格:{order_info[5]}\n" \
                     f"状态:{order_info[8]}"
            self.parent().wechat_info.send_info_sig.emit(w_info)
        return order_dict

    def refresh_positions(self):
        try:
            pos_array = get_all_pos_by_array()
            pos = []
            for i in range(self.tableWidget_pos.rowCount()):
                self.tableWidget_pos.removeRow(0)
            for p in pos_array:
                pos.append(self._refresh_postion(p))
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新POS', str(e))

    def _refresh_postion(self, p):
        self.data._update_pos(p)
        prodcode = p.ProdCode.decode()
        pos_dict = self.data.Pos[prodcode]
        r = 0

        for i in range(self.tableWidget_pos.rowCount()):
            if pos_dict['ProdCode'] == self.tableWidget_pos.item(i, 0).text():
                r = i
                break
        else:
            self.tableWidget_pos.insertRow(0)

        qty = pos_dict['Qty'] if pos_dict['LongShort'] == b'B' else -pos_dict['Qty']
        amt = pos_dict['TotalAmt'] if pos_dict['LongShort'] == b'B' else -pos_dict['TotalAmt']
        today_net_pos = pos_dict['LongQty'] - pos_dict['ShortQty']
        today_net_pos_amt = pos_dict['LongTotalAmt'] - pos_dict['ShortTotalAmt']
        net_pos = qty + today_net_pos
        net_pos_amt = amt + today_net_pos_amt

        pos_info = [prodcode,
                    self.data.Product.get(prodcode, ''),
                    f"{qty}@{(pos_dict['TotalAmt']/pos_dict['Qty']) if pos_dict['Qty'] != 0 else 0:.2f}",
                    pos_dict['DepQty'],
                    f"{pos_dict['LongQty']}@{(pos_dict['LongTotalAmt']/pos_dict['LongQty']) if pos_dict['LongQty'] != 0 else 0:.2f}",
                    f"{-pos_dict['ShortQty']}@{(pos_dict['ShortTotalAmt']/pos_dict['ShortQty']) if pos_dict['ShortQty'] != 0 else 0:.2f}",
                    f"{today_net_pos}@{today_net_pos_amt/(1 if today_net_pos==0 else today_net_pos):.2f}",
                    f"{net_pos}@{net_pos_amt/(1 if net_pos==0 else net_pos):.2f}",
                    '',
                    f"{pos_dict['PL']:,}",
                    '',
                    f"{pos_dict['ExchangeRate']:,}",
                    f"{pos_dict['PLBaseCcy']:,}",
                    f"{pos_dict['leverage']}"]

        for i, s in zip(range(14), map(str, pos_info)):
            self.tableWidget_pos.setItem(r, i, QTableWidgetItem(s))

        self.tableWidget_pos.viewport().update()

        if prodcode not in self.data.sub_list:
            self.data.sub_list.append(prodcode)

        self.pos_info_sig.emit(self.data.Pos)
        return pos_dict

    def refresh_trades(self):
        try:
            trades_array = get_all_trades_by_array()
            trades = []
            for i in range(self.tableWidget_trades.rowCount()):
                self.tableWidget_trades.removeRow(0)

            for t in trades_array:
                trades.append(self._refresh_trade(t))

        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新TRADE', str(e))

    def _refresh_trade(self, t):
        self.data._update_trade(t)
        trade_dict = self.data.Trade[t.RecNO]
        if self.parent().QuickOrder.checkBox_Lock.isChecked():
            self.parent().QuickOrder.position_takeprofit_info_update(self.data.Trade)
        r = 0
        for i in range(self.tableWidget_trades.rowCount()):
            if trade_dict['RecNO'] == int(self.tableWidget_trades.item(i, 13).text()):
                r = i
                break
        else:
            self.tableWidget_trades.insertRow(0)
        prodcode = trade_dict['ProdCode'].decode()
        trade_info = [prodcode,
                      self.data.Product.get(prodcode,''),
                      trade_dict['Qty'] if trade_dict['BuySell'].decode() == 'B' else '',
                      trade_dict['Qty'] if trade_dict['BuySell'].decode() == 'S' else '',
                      f"{trade_dict['AvgPrice']:,}",
                      trade_dict['TradeNo'],
                      ORDER_STATUS[trade_dict['Status']],
                      trade_dict['Initiator'].decode(),
                      trade_dict['Ref'].decode(),
                      dt.datetime.fromtimestamp(trade_dict['TradeTime']),
                      f"{trade_dict['OrderPrice']:,}",
                      trade_dict['IntOrderNo'],
                      trade_dict['ExtOrderNo'],
                      trade_dict['RecNO']]

        for i, s in zip(range(14), map(str, trade_info)):
            self.tableWidget_trades.setItem(r, i, QTableWidgetItem(s))

        self.tableWidget_trades.viewport().update()
        return trade_dict

    def refresh_accbals(self):
        try:
            accbal_array = get_all_accbal_by_array()
            accbal = []
            for i in range(self.tableWidget_bal.rowCount()):
                self.tableWidget_bal.removeRow(0)
            for b in accbal_array:
                accbal.append(self._refresh_accbals(b))
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新BAL', str(e))

    def _refresh_accbals(self, b):
        self.data._update_bal(b)
        accbal_dict = self.data.Bal[b.Ccy.decode()]

        r = 0
        for i in range(self.tableWidget_bal.rowCount()):
            if accbal_dict['Ccy'].decode() == self.tableWidget_bal.item(i, 0).text():
                r = i
                break
        else:
            self.tableWidget_bal.insertRow(0)
        total_cash = accbal_dict['CashBF'] + accbal_dict['NotYetValue'] + accbal_dict['TodayCash']
        ccy = get_ccy_rate_by_ccy(accbal_dict['Ccy'].decode()).value
        bal_info = [accbal_dict['Ccy'].decode(),
                    f"{accbal_dict['CashBF']:,}",
                    f"{accbal_dict['NotYetValue']:,}",
                    f"{accbal_dict['TodayCash']:,}",
                    total_cash,
                    f"{accbal_dict['Unpresented']:,}",
                    ccy,
                    f"{total_cash * ccy:,}"]

        for i, s in zip(range(8), map(str, bal_info)):
            self.tableWidget_bal.setItem(r, i, QTableWidgetItem(s))
        self.tableWidget_bal.viewport().update()

        return accbal_dict

    def refresh_ccy_rate(self):
        try:
            ccy_list = ['CAD', 'CHF', 'EUR', 'GBP', 'HKD', 'JPY', 'KRW', 'MYR', 'SGD', 'USD']
            # ccy_dict = {ccy: get_ccy_rate_by_ccy(ccy).value for ccy in ccy_list}
            for ccy in ccy_list:
                self.data._update_ccy({ccy: get_ccy_rate_by_ccy(ccy).value})
            for i in range(self.tableWidget_ccy_rate.rowCount()):
                self.tableWidget_ccy_rate.removeRow(0)
            for i, (ccy, rate) in enumerate(self.data.Ccy.items()):
                self.tableWidget_ccy_rate.insertRow(i)
                self.tableWidget_ccy_rate.setVerticalHeaderItem(i, QTableWidgetItem(ccy))
                self.tableWidget_ccy_rate.setItem(i, 0, QTableWidgetItem(str(rate)))
            self.tableWidget_ccy_rate.viewport().update()
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-更新CCY', str(e))
    # -----------------------------------------------------------------------------------------------


class SpLoginDialog(QDialog, Ui_Dialog_sp_login):
    login_error_sig = pyqtSignal(str)
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog_sp_login.__init__(self)
        self.setupUi(self)
        self.login_error_sig.connect(self.login_waring)
        self.login_info = []
        self.init_info()

    def login_waring(self, text):
        QtWidgets.QMessageBox.critical(self,'CRITICAL-登录',text)

    def set_info(self, info):
        self.lineEdit_host.setText(info['host'])
        self.lineEdit_port.setText(str(info['port']))
        self.lineEdit_license.setText(info['License'])
        self.lineEdit_app_id.setText(info['app_id'])
        self.lineEdit_user_id.setText(info['user_id'])

    def init_info(self):
        if os.path.exists('info.plk'):
            try:
                with open('info.plk', 'rb') as f:
                    self.login_info = pickle.load(f)
                    info = self.login_info[0]
                    self.set_info(info)
                    self.comboBox_account.addItems([i['user_id'] for i in self.login_info])
                    self.comboBox_account.currentIndexChanged.connect(lambda n:self.set_info(self.login_info[n]))
            except Exception as e:
                print(e)

    def pickle_info(self):
        host = self.lineEdit_host.text()
        port = self.lineEdit_port.text()
        License = self.lineEdit_license.text()
        app_id = self.lineEdit_app_id.text()
        user_id = self.lineEdit_user_id.text()
        info = {'host': host, 'port': int(port), 'License': License, 'app_id': app_id, 'user_id': user_id}

        for i, l in enumerate(self.login_info):
            if info['user_id'] == l['user_id']:
                self.login_info.insert(0, self.login_info.pop(i))
                break
        else:
            self.login_info.insert(0, info)

        with open('info.plk', 'wb') as f:
            pickle.dump(self.login_info, f)

class ClosePositionDialog(QtWidgets.QDialog, Ui_Dialog_close_position):  # 平仓交互界面
    def __init__(self, BuySell, ProdCode, Qty, toler, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Dialog_close_position.__init__(self)
        self.setupUi(self)
        self.pushButton_Long.setVisible(BuySell == 'B')
        self.pushButton_Short.setVisible(BuySell == 'S')
        self.lineEdit_ProdCode.setText(ProdCode)
        self.spinBox_Qty.setValue(Qty)
        self.spinBox_toler.setValue(toler)
        self.init_signal()
        self.setModal(True)
        self.show()
        self.sub_prodcode(ProdCode)
        self.prodcode = ProdCode
        self.BuySell = BuySell

    def init_signal(self):
        self.pushButton_Long.released.connect(lambda :self.close_position('B'))
        self.pushButton_Short.released.connect(lambda :self.close_position('S'))
        self.checkBox_MarketOrder.toggled.connect(self.set_price)
        self.spinBox_Price.valueChanged.connect(self.update_price)

    def set_price(self, b):
        if b:
            self.spinBox_Price.setValue(0)
        else:
            self.price = get_price_by_code(self.prodcode)
            self.spinBox_Price.setValue(int(self.price.Ask[0]) if self.BuySell == 'B' else int(self.price.Bid[0]))

    def update_price(self, p):
        new_price = get_price_by_code(self.prodcode)
        if p == 0:
            return
        if self.BuySell == 'B':
            o_ask = p
            n_ask = int(new_price.Ask[0])
            if n_ask > o_ask:
                self.spinBox_Price.setValue(n_ask)
            else:
                self.price = new_price
        else:
            o_bid = p
            n_bid = int(new_price.Bid[0])
            if n_bid < o_bid:
                self.spinBox_Price.setValue(n_bid)
            else:
                self.price = new_price

    def sub_prodcode(self, prodcode):
        try:
            self.price = get_price_by_code(prodcode)
        except:
            if subscribe_price(prodcode, 1) != 0:
                mb = QMessageBox()
                mb.warning(self, f'WARING-订阅', f'订阅{prodcode}数据失败')
                mb.accepted.connect(self.close)
            else:
                QMessageBox.information(self, f'INFO-订阅成功', f'订阅{prodcode}数据成功')

    def close_position(self, BuySell):  # 平仓
        try:
            order_kwargs = {}
            order_kwargs['ProdCode'] = self.lineEdit_ProdCode.text()
            order_kwargs['Qty'] = self.spinBox_Qty.value()
            order_kwargs['BuySell'] = BuySell
            order_kwargs['OrderOptions'] = 1 if self.checkBox_OrderOptions.checkState() else 0
            order_kwargs['Ref'] = '一键平仓'
            order_kwargs['CondType'] = 0
            order_kwargs['ValidType'] = self.comboBox_ValidType.currentIndex()
            order_kwargs['OrderType'] = 0
            if self.checkBox_MarketOrder.isChecked():
                price = get_price_by_code(self.lineEdit_ProdCode.text())
                order_kwargs['Price'] = price.Bid[0] + self.spinBox_toler.value() if BuySell == 'B' else price.Ask[0] - self.spinBox_toler.value()
            else:
                order_kwargs['Price'] = self.spinBox_Price.value()
        except Exception as e:
            QMessageBox.warning(self, 'ERROR-平仓', str(e))
        else:
            comfirm_order = ComfirmDialog(self, **order_kwargs)
            comfirm_order.show()
            comfirm_order.accepted.connect(lambda : add_order(**order_kwargs))
            comfirm_order.accepted.connect(lambda :self.accept())


class QuickOrderDialog(QtWidgets.QDialog, Ui_Dialog_quick_order):  # 快速下单界面
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Dialog_quick_order.__init__(self)
        self.setupUi(self)
        self.tableWidget_Price.setColumnWidth(0, 30)
        self.tableWidget_Price.setColumnWidth(3, 30)
        self.tableWidget_Price.setColumnWidth(4, 70)
        self.tableWidget_Price.setColumnWidth(5, 30)
        self.tableWidget_Price.setColumnWidth(8, 30)
        # desktop = QDesktopWidget()
        self.move(0, 20)
        # self.move(self.parent().width() - self.width(), 0)
        self.tableWidget_Price.setSelectionMode(QTableWidget.SingleSelection)
        self.trade_long_queue = []
        self.trade_short_queue = []
        self.holding_pos = (0, 0)
        self.init_signal()
        self._price_active = False
        self.setWindowFlags(Qt.Qt.Window)

    def order(self, BuySell, Price):
        try:
            order_kwargs = {}
            order_kwargs['ProdCode'] = self.lineEdit_ProdCode.text()
            order_kwargs['BuySell'] = BuySell
            order_kwargs['Qty'] = self.spinBox_Qty.value()
            order_kwargs['OrderOptions'] = 1 if self.checkBox_OrderOptions.checkState() else 0
            order_kwargs['ValidType'] = self.comboBox_VaildType.currentIndex()
            order_kwargs['CondType'] = 0
            order_kwargs['Price'] = Price
            cond = get_order_cond(order_kwargs)
        except Exception as e:
            raise e
        else:
            comfirm_order = ComfirmDialog(self, Cond=cond, **order_kwargs)
            comfirm_order.show()
            comfirm_order.accepted.connect(lambda : add_order(**order_kwargs))

    def close_all_position(self, e):  # 一键平仓
        try:
            prodcode = self.lineEdit_ProdCode.text()
            pos = get_pos_by_product(prodcode)
            net_pos = (pos.Qty + pos.LongQty - pos.ShortQty) if pos.LongShort ==b'B' else (-pos.Qty + pos.LongQty - pos.ShortQty)
            toler = self.spinBox_toler.value()
            if net_pos > 0:
                ClosePositionDialog('S', prodcode, net_pos, toler, parent=self) if e.button() == Qt.Qt.LeftButton else ClosePositionDialog('S', prodcode, net_pos, toler, parent=self).close_position('S')
            elif net_pos < 0:
                ClosePositionDialog('B', prodcode, -net_pos, toler, parent=self) if e.button() == Qt.Qt.LeftButton else ClosePositionDialog('B', prodcode, -net_pos, toler, parent=self).close_position('B')
            else:
                QMessageBox.warning(self, 'WARNING-平仓', f'{prodcode}没有仓位')
        except Exception as e:
            QMessageBox.warning(self, 'ERROR-平仓', f'{e}或{prodcode}没有仓位')


    def init_signal(self):
        # self.checkBox_Lock.toggled.connect(lambda x: subscribe_price(self.lineEdit_ProdCode.text(), 1) if x else subscribe_price(self.lineEdit_ProdCode.text(), 0))
        self.pushButton_price_to_middle.released.connect(lambda :self.adjust_ui(25))
        self.tableWidget_Price.itemDoubleClicked.connect(lambda i: self.doubleclick_order(i.row(), i.column()))  # 双击下单的信号连接
        self.pushButton_long.released.connect(lambda :self.addition_toler_order('B'))
        self.pushButton_short.released.connect(lambda: self.addition_toler_order('S'))
        self.checkBox_Lock.toggled.connect(lambda b: [subscribe_price(self.lineEdit_ProdCode.text(), 1),time.sleep(0.5), self.adjust_ui(25)] if b else ...)
        # self.pushButton_close_position.released.connect(self.close_all_position)
        self.pushButton_close_position.mouseReleaseEvent = lambda e: self.close_all_position(e)

    def adjust_ui(self, n):  # 置中调整点击下单table
        try:
            last_price = get_price_by_code(self.lineEdit_ProdCode.text()).Last[0]
        except Exception as e:
            print(e)
        else:
            Price = range(int(last_price + n), int(last_price - n), -1)
            self.tableWidget_Price.clearContents()
            self.tableWidget_Price.setRowCount(len(Price))
            self.price_location = {}
            for i, p in enumerate(Price):
                self.price_location[p] = i
                self.tableWidget_Price.setItem(i, 0, QTableWidgetItem(QIcon(os.path.join('ui', 'deleteorder.png')), ''))
                self.tableWidget_Price.setItem(i, 1, QTableWidgetItem(''))
                self.tableWidget_Price.setItem(i, 2, QTableWidgetItem(''))
                self.tableWidget_Price.setItem(i, 3, QTableWidgetItem(QIcon(os.path.join('ui', 'addorder.png')), ''))
                self.tableWidget_Price.setItem(i, 4, QTableWidgetItem(str(p)))
                self.tableWidget_Price.setItem(i, 5, QTableWidgetItem(QIcon(os.path.join('ui', 'addorder.png')), ''))
                self.tableWidget_Price.setItem(i, 6, QTableWidgetItem(''))
                self.tableWidget_Price.setItem(i, 7, QTableWidgetItem(''))
                self.tableWidget_Price.setItem(i, 8, QTableWidgetItem(QIcon(os.path.join('ui', 'deleteorder.png')), ''))
            self._price_active = True
            self.working_order_update()
            self.tableWidget_Price.viewport().update()
            m = self.tableWidget_Price.verticalScrollBar().maximum() // 2
            self.tableWidget_Price.verticalScrollBar().setValue(m)
            # self.tableWidget_Price.selectRow(self.tableWidget_Price.currentRow()-3)
            # self.tableWidget_Price.verticalScrollBar().

    def working_order_update(self):  # 处理现有的订单在点击下单table中的显示
        orders = get_orders_by_array()
        bid_qty_loc = []
        ask_qty_loc =[]
        for order in [o for o in orders if (o.ProdCode.decode('GBK') == self.lineEdit_ProdCode.text())&(o.Status in [1, 3, 8])]:
            price_loc = self.price_location.get(order.Price)
            if (order.BuySell.decode() == 'B')&(price_loc is not None):
                origin_qty = self.tableWidget_Price.item(price_loc, 1).text()
                if origin_qty:
                    self.tableWidget_Price.setItem(price_loc, 1, QTableWidgetItem(str(order.Qty + int(origin_qty))))
                else:
                    self.tableWidget_Price.setItem(price_loc, 1, QTableWidgetItem(str(order.Qty)))
                bid_qty_loc.append(price_loc)
            elif (order.BuySell.decode() == 'S') & (price_loc is not None):
                origin_qty = self.tableWidget_Price.item(price_loc, 7).text()
                if origin_qty:
                    self.tableWidget_Price.setItem(price_loc, 7, QTableWidgetItem(str(order.Qty + int(origin_qty))))
                else:
                    self.tableWidget_Price.setItem(price_loc, 7, QTableWidgetItem(str(order.Qty)))
                ask_qty_loc.append(price_loc)

        for i in set(self.price_location.values()) - set(bid_qty_loc):
            self.tableWidget_Price.setItem(i, 1, QTableWidgetItem(''))
        for i in set(self.price_location.values()) - set(ask_qty_loc):
            self.tableWidget_Price.setItem(i, 7, QTableWidgetItem(''))

    def price_table_update(self, price_dict):  # 根据price来更新点击下单的table
        bids_loc = []
        asks_loc = []
        if self._price_active&(price_dict['ProdCode'].decode('GBK') == self.lineEdit_ProdCode.text()):
            for i in range(5):
                bid_loc = self.price_location.get(price_dict['Bid'][i])
                ask_loc = self.price_location.get(price_dict['Ask'][i])
                if bid_loc:
                    self.tableWidget_Price.item(bid_loc, 2).setText(str(price_dict['BidQty'][i]))
                    bids_loc.append(bid_loc)
                if ask_loc:
                    self.tableWidget_Price.item(ask_loc, 6).setText(str(price_dict['AskQty'][i]))
                    asks_loc.append(ask_loc)

            bid_empty_loc = set(self.price_location.values()) - set(bids_loc)
            ask_empty_loc = set(self.price_location.values()) - set(asks_loc)

            for n, m in zip(bid_empty_loc, ask_empty_loc):
                self.tableWidget_Price.item(n, 2).setText('')
                self.tableWidget_Price.item(m, 6).setText('')

            last1_loc = self.price_location.get(price_dict['Last'][0])
            bid1_loc = self.price_location.get(price_dict['Bid'][0])
            ask1_loc = self.price_location.get(price_dict['Ask'][0])
            color_map = {bid1_loc: '#FF0000', ask1_loc: '#00FF00'}

            for i in self.price_location.values():
                color = color_map.get(i, '#FFFFFF')
                self.tableWidget_Price.item(i, 4).setBackground(QColor(color))

                if i == last1_loc:
                    self.tableWidget_Price.item(i, 4).setFont(QFont('Microsoft YaHei', 9, QFont.Bold))
                else:
                    self.tableWidget_Price.item(i, 4).setFont(QFont('Microsoft YaHei', 9, QFont.Normal))

            self.tableWidget_Price.viewport().update()

    def price_info_update(self, price_dict):  # 根据推送的price来计算追价情况
        prodcode = price_dict['ProdCode'].decode()
        if prodcode == self.lineEdit_ProdCode.text():
            bid = price_dict['Bid'][0]
            ask = price_dict['Ask'][0]
            toler = self.spinBox_toler.value()
            self.pushButton_long.setText(f'追价买入\n@{ask}->{ask + toler}')
            self.pushButton_short.setText(f'追价沽出\n@{bid}->{bid - toler}')
            # self.label_long_info.setText(f'@{bid}->{bid + toler}')
            # self.label_short_info.setText(f'@{ask}->{ask - toler}')

    def position_takeprofit_info_update(self, trades_info):
        # trades = get_all_trades_by_array()
        prodcode = self.lineEdit_ProdCode.text()
        current_trades = [trade for Id, trade in trades_info.items() if trade['ProdCode'].decode('GBK') == prodcode]
        if 'HSI' in prodcode:
            leverage = 50
        elif 'MHI' in prodcode:
            leverage = 10
        else:
            leverage = 1
        try:
            pos = get_pos_by_product(self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)
        else:
            pre_pos = pos.Qty
            pre_pos_price = pos.TotalAmt  / pre_pos if pre_pos !=0 else 0
                # .sort(key=lambda x:x['IntOrderNo'])
            self.trade_long_queue.clear()
            self.trade_short_queue.clear()

            for t in current_trades:
                current_trade = [t['AvgPrice']] * t['Qty']
                if t['BuySell'].decode('GBK') == 'B':
                    self.trade_long_queue.extend(current_trade)
                else:
                    self.trade_short_queue.extend(current_trade)
            if pos.LongShort == b'B':
                self.trade_long_queue.extend([pre_pos_price] * pre_pos)
            elif pos.LongShort == b'S':
                self.trade_short_queue.extend([pre_pos_price] * pre_pos)

            close_pos_takeprofit = reduce(add, [s-l for l, s in zip(self.trade_long_queue, self.trade_short_queue) ]) if len(self.trade_long_queue) != 0 and len(self.trade_short_queue) != 0 else 0
            long_pos_num = len(self.trade_long_queue)
            short_pos_num = len(self.trade_short_queue)
            holding_pos_num = long_pos_num - short_pos_num

            if  long_pos_num == short_pos_num:
                self.holding_pos = (0, 0)
            elif long_pos_num > short_pos_num:
                self.holding_pos = (holding_pos_num, sum(self.trade_long_queue[-1:-(holding_pos_num + 1):-1]) / holding_pos_num)
            else:
                self.holding_pos = (holding_pos_num, sum(self.trade_short_queue[-1:-(-holding_pos_num + 1):-1]) / -holding_pos_num)

            self.label_closed_profit.setText(f'{close_pos_takeprofit * leverage:,.2f}')
            self.label_pos.setText(f'{self.holding_pos[0]}@{self.holding_pos[1]:,.2f}')

    def holding_profit(self, price_dict):  # 根据推送的price来计算持仓盈亏
        prodcode = self.lineEdit_ProdCode.text()
        if 'HSI' in prodcode:
            leverage = 50
        elif 'MHI' in prodcode:
            leverage = 10
        else:
            leverage = 1
        if price_dict['ProdCode'].decode('GBK') == prodcode:
            profit = (price_dict['Last'][0] - self.holding_pos[1]) * self.holding_pos[0]
            self.label_holding_porfit.setText(f'{profit * leverage:,.2f}')

    def doubleclick_order(self, row, column):  # 双击下单
        price = float(self.tableWidget_Price.item(row, 4).text())
        if column == 3:
            buysell = 'B'
            self.order(buysell, price)
        elif column == 5:
            buysell = 'S'
            self.order(buysell, price)

    def addition_toler_order(self, buysell):  # 追价下单
        try:
            price = get_price_by_code(self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)
        else:
            if buysell == 'B':
                bid = price.Bid[0]
                limit_price = bid + self.spinBox_toler.value()
            elif buysell =='S':
                ask = price.Ask[0]
                limit_price = ask - self.spinBox_toler.value()
            self.order(buysell, limit_price)

    # def closeEvent(self, a0: QtGui.QCloseEvent):
    #     self.parent().AccInfo.pushButton_QuickOrder.setChecked(False)
    #     a0.accept()


class OrderAssistantWidget(QtWidgets.QWidget, Ui_Form_OrderAssistant):
    oco_close_sig = pyqtSignal(str, int, float, float)
    close_position_trigger_sig = pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_OrderAssistant.__init__(self)
        self.setupUi(self)
        self.holding_qty = 0
        self.holding_pos_amt = 0
        self.trailing_best_price = None
        self.last_price = {}
        self.init_signal()
        self.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.Window)

    def init_signal(self):
        AccInfo = self.parent().AccInfo
        self.spinBox_takeprofit_amount.editingFinished.connect(lambda :self.calc_amount_base(AccInfo.data.Pos))
        self.spinBox_stoploss_amount.editingFinished.connect(lambda: self.calc_amount_base(AccInfo.data.Pos))
        self.pushButton_OCO_close_position.released.connect(self.oco_close_position)
        # self.lineEdit_ProdCode.editingFinished.connect(self.update_holding_pos)
        # self.parent().pos_info_sig.connect(lambda p:self.update_holding_pos())
        self.lineEdit_ProdCode.editingFinished.connect(self.update_holding_pos_LIFO)
        AccInfo.pos_info_sig.connect(lambda p:self.update_holding_pos_LIFO())

        self.checkBox_trailing_stop.toggled.connect(lambda b: AccInfo.price_update_sig.connect(self.update_trailing_stop) if b else AccInfo.price_update_sig.disconnect(self.update_trailing_stop))
        AccInfo.price_update_sig.connect(lambda p: self.lineEdit_price.setText(str(p['Last'][0])) if p['ProdCode'].decode() == self.lineEdit_ProdCode.text() else ...)
        AccInfo.price_update_sig.connect(lambda p: setattr(self, 'last_price', p) if p['ProdCode'].decode() == self.lineEdit_ProdCode.text() else ...)

        AccInfo.order_info_sig.connect(lambda o: self.checkBox_auto_tp.setChecked(True) if o['ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 1 and o['Ref'].decode() =='auto_tp' else ...)
        AccInfo.order_info_sig.connect(lambda o: self.checkBox_auto_tp.setChecked(False) if o[ 'ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 10 and o['Ref'].decode() == 'auto_tp' else ...)
        self.checkBox_auto_tp.clicked.connect(lambda b: self.init_auto_takeprofit() if b else self.deinit_auto_takeprofit())
        self.pushButton_tp.released.connect(lambda :self.init_auto_takeprofit())

        AccInfo.order_info_sig.connect(lambda o: self.checkBox_auto_sl.setChecked(True) if o['ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 1 and o['Ref'].decode() =='auto_sl' else ...)
        AccInfo.order_info_sig.connect(lambda o: self.checkBox_auto_sl.setChecked(False) if o[ 'ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 10 and o['Ref'].decode() == 'auto_sl' else ...)
        self.checkBox_auto_sl.clicked.connect(lambda b: self.init_auto_stoploss() if b else self.deinit_auto_stoploss())
        self.pushButton_sl.released.connect(lambda :self.init_auto_stoploss())

        self.lineEdit_ProdCode.editingFinished.connect(lambda :self.init_auto_tp_sl())

        self.pushButton_tp_pos_by_pos.released.connect(self.tp_pos_by_pos)
        self.pushButton_sl_pos_by_pos.released.connect(self.sl_pos_by_pos)

        self.pushButton_tp_by_amount.released.connect(self.tp_by_amount)
        self.pushButton_sl_by_amount.released.connect(self.sl_by_amount)

        self.close_position_trigger_sig.connect(lambda :QMessageBox.information(self, '<INFO>-追踪止损', '平仓信号触发'))

        self.spinBox_tp_price.valueChanged.connect(self.tp_price_update)
        self.spinBox_sl_price.valueChanged.connect(self.sl_price_update)

    def tp_price_update(self, p):
        prodcode = self.lineEdit_ProdCode.text()
        try:
            new_price = get_price_by_code(prodcode)
        except Exception as e:
            QMessageBox.warning(self, '<WARING>-止盈', str(e))
            return

        if not new_price.Last[0] * 0.9 < p < new_price.Last[0] * 1.1:
            self.spinBox_tp_price.setValue(int(new_price.Last[0]))
            return

        if self.holding_qty > 0:
            n_bid = new_price.Bid[0]
            if n_bid > p:
                self.spinBox_tp_price.setValue(n_bid)
        elif self.holding_qty < 0:
            n_ask = new_price.Ask[0]
            if n_ask < p:
                self.spinBox_tp_price.setValue(n_ask)

    def sl_price_update(self, p):
        prodcode = self.lineEdit_ProdCode.text()
        try:
            new_price = get_price_by_code(prodcode)
        except Exception as e:
            QMessageBox.warning(self, '<WARING>-止损', str(e))
            return

        if not new_price.Last[0] * 0.9 < p < new_price.Last[0] * 1.1:
            self.spinBox_sl_price.setValue(int(new_price.Last[0]))
            return

        if self.holding_qty > 0:
            n_bid = new_price.Bid[0]
            if n_bid < p:
                self.spinBox_sl_price.setValue(n_bid)
        elif self.holding_qty < 0:
            n_ask = new_price.Ask[0]
            if n_ask > p:
                self.spinBox_sl_price.setValue(n_ask)

    def init_auto_tp_sl(self):  # 产品代码输出后， 初始化原来的止损止盈情况
        try:
            orders = get_orders_by_array()
            self.checkBox_auto_tp.setChecked(False)
            self.checkBox_auto_sl.setChecked(False)
            for o in orders:
                if o.Status in [1, 3] and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    if o.Ref.decode() == 'auto_tp':
                        self.checkBox_auto_tp.setChecked(True)
                        break
                    elif o.Ref.decode() =='auto_sl':
                        self.checkBox_auto_sl.setChecked(True)
        except Exception as e:
            print(e)

    def init_auto_takeprofit(self):  # 初始化自动止盈
        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-自动止盈', '请检查合约代码')
            return
        tp = self.spinBox_tp_price.value()
        if self.holding_qty > 0:
            if tp <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止盈', '止盈价需高于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=int(self.holding_qty), ValidType=0, CondType=0, OrderType=0, Price=tp,
                          Ref='auto_tp')
        elif self.holding_qty < 0:
            if tp >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止盈', '止盈价需低于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=int(-self.holding_qty), ValidType=0, CondType=0, OrderType=0, Price=tp,
                          Ref='auto_tp')

    def deinit_auto_takeprofit(self):  # 取消自动止盈
        try:
            orders = get_orders_by_array()
            for o in orders:
                if o.Ref.decode() == 'auto_tp' and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    delete_order_by(o.IntOrderNo, self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)

    def init_auto_stoploss(self):  # 初始化自动止损
        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-自动止损', '请检查合约代码')
            return
        sl = self.spinBox_sl_price.value()
        if self.holding_qty > 0:
            if sl >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止损', '止损价需低于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=int(self.holding_qty), ValidType=0, CondType=1, OrderType=0, Price=sl - self.spinBox_stoploss_toler.value(),
                          StopType='L', StopLevel=sl,
                          Ref='auto_sl')
        elif self.holding_qty < 0:
            if sl <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止损', '止损价需高于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=int(-self.holding_qty), ValidType=0, CondType=1, OrderType=0, Price=sl + self.spinBox_stoploss_toler.value(),
                          StopType='L', StopLevel=sl,
                          Ref='auto_sl')

    def deinit_auto_stoploss(self):  # 取消自动止损
        try:
            orders = get_orders_by_array()
            for o in orders:
                if o.Ref.decode() == 'auto_sl' and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    delete_order_by(o.IntOrderNo, self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)

    def update_holding_pos(self):  #先进先出方法计算持仓
        pos = self.parent().AccInfo.pos_info.get(self.lineEdit_ProdCode.text())
        if pos is not None:
            qty = pos['Qty'] if pos['LongShort'] == b'B' else -pos['Qty']
            amt = pos['TotalAmt'] if pos['LongShort'] == b'B' else -pos['TotalAmt']
            today_net_pos = pos['LongQty'] - pos['ShortQty']
            today_net_pos_amt = pos['LongTotalAmt'] - pos['ShortTotalAmt']
            self.holding_pos_amt = amt + today_net_pos_amt
            self.holding_qty = qty + today_net_pos
            holding_price = self.holding_pos_amt / self.holding_qty if self.holding_qty != 0 else self.holding_pos_amt
            self.lineEdit_holding_qty.setText(str(self.holding_qty))
            self.lineEdit_holding_price.setText(f'{holding_price:.2f}')
        else:
            self.lineEdit_holding_qty.setText('-')
            self.lineEdit_holding_price.setText('-')

    def update_holding_pos_LIFO(self):  # 后进先出方法计算持仓
        try:
            self.holding_qty, holding_pos = self._get_holding_pos(self.parent().AccInfo.data.Trade)
        except Exception as e:
            self.lineEdit_holding_qty.setText('-')
            self.lineEdit_holding_price.setText('-')
        else:
            if self.holding_qty != 0:
                holding_price = sum(holding_pos) / len(holding_pos)
                self.lineEdit_holding_qty.setText(str(self.holding_qty))
                self.lineEdit_holding_price.setText(f'{holding_price:.2f}')
            else:
                self.lineEdit_holding_qty.setText('-')
                self.lineEdit_holding_price.setText('-')

    def update_trailing_stop(self, price):  # 基于price更新追踪止损

        toler = self.spinBox_trailing_toler.value()
        if price['ProdCode'].decode() != self.lineEdit_ProdCode.text():
            return
        if self.holding_qty > 0:
            self.trailing_best_price = max(self.trailing_best_price, price['Last'][0]) if self.trailing_best_price != None else price['Last'][0]
            self.trailing_close_price = self.trailing_best_price - toler
            if self.trailing_close_price >= price['Last'][0]:
                self.close_position_trigger_sig.emit()  # 触发平仓信号
                self.checkBox_trailing_stop.setChecked(False)
                self.trailing_best_price = None
                self.lineEdit_best_price.setText('-')
                self.lineEdit_sl_close_price.setText('-')
            else:
                self.lineEdit_best_price.setText(str(self.trailing_best_price))
                self.lineEdit_sl_close_price.setText(str(self.trailing_close_price))
                self.horizontalSlider_toler.setMaximum(int(self.trailing_best_price))
                self.horizontalSlider_toler.setMinimum(int(self.trailing_close_price))
                self.horizontalSlider_toler.setValue(int(price['Last'][0]))
        elif self.holding_qty < 0:
            self.trailing_best_price = min(self.trailing_best_price, price['Last'][0]) if self.trailing_best_price != None else price['Last'][0]
            self.trailing_close_price = self.trailing_best_price + toler
            self.horizontalSlider_toler.setValue(int(price['Last'][0]))
            if self.trailing_close_price <= price['Last'][0]:
                self.close_position_trigger_sig.emit()  # 触发平仓信号
                self.checkBox_trailing_stop.setChecked(False)
                self.trailing_best_price = None
                self.lineEdit_best_price.setText('-')
                self.lineEdit_sl_close_price.setText('-')
            else:
                self.lineEdit_best_price.setText(str(self.trailing_best_price))
                self.lineEdit_sl_close_price.setText(str(self.trailing_close_price))
                self.horizontalSlider_toler.setMinimum(int(self.trailing_best_price))
                self.horizontalSlider_toler.setMaximum(int(self.trailing_close_price))

    def _get_holding_pos(self, trades_info):  # 获取持仓
        prodcode = self.lineEdit_ProdCode.text()
        current_trades = [trade for Id, trade in trades_info.items() if trade['ProdCode'].decode('GBK') == prodcode]
        print(current_trades)
        if 'HSI' in prodcode:
            leverage = 50
        elif 'MHI' in prodcode:
            leverage = 10
        else:
            leverage = 1

        pos = get_pos_by_product(prodcode)
        pre_pos = pos.Qty
        pre_pos_price = pos.TotalAmt  / pre_pos if pre_pos !=0 else 0
            # .sort(key=lambda x:x['IntOrderNo'])
        self.trade_long_queue = []
        self.trade_short_queue = []

        if pos.LongShort == b'B':
            self.trade_long_queue.extend([pre_pos_price] * pre_pos)
        elif pos.LongShort == b'S':
            self.trade_short_queue.extend([pre_pos_price] * pre_pos)

        for t in current_trades:
            current_trade = [t['AvgPrice']] * t['Qty']
            if t['BuySell'].decode('GBK') == 'B':
                self.trade_long_queue.extend(current_trade)
            else:
                self.trade_short_queue.extend(current_trade)

        close_pos_takeprofit = reduce(add, [s-l for l, s in zip(self.trade_long_queue, self.trade_short_queue) ]) if len(self.trade_long_queue) != 0 and len(self.trade_short_queue) != 0 else 0
        long_qty = len(self.trade_long_queue)
        short_qty = len(self.trade_short_queue)
        holding_qty = long_qty - short_qty

        if holding_qty > 0:
            holding_pos = self.trade_long_queue[:holding_qty]
        elif holding_qty < 0:
            holding_pos = self.trade_short_queue[:-holding_qty]
        else:
            holding_pos = []

        return holding_qty, holding_pos

    def sl_pos_by_pos(self):  # 逐仓计算止损
        try:
            holding_qty, holding_pos = self._get_holding_pos(self.parent().AccInfo.data.Trade)
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-获取持仓失败', str(e))
            return

        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-逐仓止损错误', '请检查合约代码')
            return

        if self.spinBox_lock_pos.value() >= abs(holding_qty):
            QMessageBox.warning(self, 'WARING-锁仓错误', f'目前持仓只有{holding_qty}')
            return

        if holding_qty > 0:
            tp_close_qty = holding_qty - self.spinBox_lock_pos.value()
            holding_pos.reverse()
            tp_close_pos = holding_pos[:tp_close_qty]
            for p in tp_close_pos:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=1, ValidType=0, CondType=1, OrderType=0, Price=p - self.spinBox_sl_addition.value() - self.spinBox_sl_addition_toler.value(),
                          StopType='L', StopLevel=p - self.spinBox_sl_addition.value(),
                          Ref='sl_pos_by_pos')
        elif holding_qty < 0:
            tp_close_qty = -holding_qty - self.spinBox_lock_pos.value()
            holding_pos.reverse()
            tp_close_pos = holding_pos[:tp_close_qty]
            for p in tp_close_pos:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=1, ValidType=0, CondType=1, OrderType=0, Price=p + self.spinBox_sl_addition.value() + self.spinBox_sl_addition_toler.value(),
                          StopType='L', StopLevel=p + self.spinBox_sl_addition.value(),
                          Ref='sl_pos_by_pos')

        else:
            QMessageBox.warning(self, 'WARING-逐仓止损', '无持仓')

    def tp_pos_by_pos(self):  # 逐仓计算止盈
        try:
            holding_qty, holding_pos = self._get_holding_pos(self.parent().AccInfo.data.Trade)
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-获取持仓失败', str(e))
            return

        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-逐仓止盈错误', '请检查合约代码')
            return

        if self.spinBox_lock_pos.value() >= abs(holding_qty):
            QMessageBox.warning(self, 'WARING-锁仓错误', f'目前持仓只有{holding_qty}')
            return

        if holding_qty > 0:
            tp_close_qty = holding_qty - self.spinBox_lock_pos.value()
            holding_pos.reverse()
            tp_close_pos = holding_pos[:tp_close_qty]
            for p in tp_close_pos:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=1, ValidType=0, CondType=0, OrderType=0, Price=p + self.spinBox_tp_addition.value(),
                          Ref='tp_pos_by_pos')
        elif holding_qty < 0:
            tp_close_qty = -holding_qty - self.spinBox_lock_pos.value()
            holding_pos.reverse()
            tp_close_pos = holding_pos[:tp_close_qty]
            for p in tp_close_pos:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=1, ValidType=0, CondType=0, OrderType=0, Price=p - self.spinBox_tp_addition.value(),
                          Ref='tp_pos_by_pos')
        else:
            QMessageBox.warning(self, 'WARING-逐仓止盈', '无持仓')

    def calc_amount_base(self, pos_info):  # 计算持仓及相关止损止盈下的价格
        prodcode = self.lineEdit_ProdCode.text()
        p = pos_info.get(prodcode)
        if p:
            net_amt = p['TotalAmt'] + p['LongTotalAmt'] - p['ShortTotalAmt'] if p['LongShort'] == b'B' else -p['TotalAmt'] + p['LongTotalAmt'] - p['ShortTotalAmt']
            self.net_qty = p['Qty'] + p['LongQty'] - p['ShortQty'] if p['LongShort'] == b'B'else -p['Qty'] + p['LongQty'] - p['ShortQty']
            self.tp = (net_amt + self.spinBox_takeprofit_amount.value() / p['leverage']) / self.net_qty if self.net_qty != 0 else 0
            self.sl = (net_amt + self.spinBox_stoploss_amount.value() / p['leverage']) / self.net_qty if self.net_qty != 0 else 0
            self.lineEdit_takeprofit_price.setText(f'{self.net_qty}@{self.tp:.2f}')
            self.lineEdit_stoploss_price.setText(f'{self.net_qty}@{self.sl:.2f}')


    def oco_close_position(self):  # 双向限价平仓
        prodcode = self.lineEdit_ProdCode.text()
        net_qty = getattr(self, 'net_qty', 0)
        tp = getattr(self, 'tp', 0)
        sl = getattr(self, 'sl', 0)
        if net_qty != 0:
            self.oco_close_sig.emit(prodcode, net_qty, tp, sl)
        else:
            QMessageBox.warning(self, 'WARING-双向限价平仓', f'合约{prodcode}未有任何持仓，无法下平仓指令')

    def tp_by_amount(self):
        prodcode = self.lineEdit_ProdCode.text()
        net_qty = getattr(self, 'net_qty', 0)
        tp = round(getattr(self, 'tp', 0))
        if prodcode != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-止盈', '请检查合约代码')
            return

        if net_qty > 0:
            if tp <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-止盈', '止盈价需高于现价')
            else:
                add_order(ProdCode=prodcode, BuySell='S', OrderOptions=0,
                          Qty=int(net_qty), ValidType=0, CondType=0, OrderType=0, Price=tp,
                          Ref='tp_by_amount')
        elif net_qty < 0:
            if tp >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-止盈', '止盈价需低于现价')
            else:
                add_order(ProdCode=prodcode, BuySell='B', OrderOptions=0,
                          Qty=int(-net_qty), ValidType=0, CondType=0, OrderType=0, Price=tp,
                          Ref='tp_by_amount')


    def sl_by_amount(self):
        prodcode = self.lineEdit_ProdCode.text()
        net_qty = getattr(self, 'net_qty', 0)
        sl = round(getattr(self, 'sl', 0))

        if prodcode != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-止损', '请检查合约代码')
            return

        if net_qty > 0:
            if sl >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-止损', '止损价需低于现价')
            else:
                add_order(ProdCode=prodcode, BuySell='S', OrderOptions=0,
                          Qty=int(net_qty), ValidType=0, CondType=1, OrderType=0, Price=sl - self.spinBox_stoploss_toler.value(),
                          StopType='L', StopLevel=sl,
                          Ref='sl_by_amount')
        elif net_qty < 0:
            if sl <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-止损', '止损价需高于现价')
            else:
                add_order(ProdCode=prodcode, BuySell='B', OrderOptions=0,
                          Qty=int(-net_qty), ValidType=0, CondType=1, OrderType=0, Price=sl + self.spinBox_stoploss_toler.value(),
                          StopType='L', StopLevel=sl,
                          Ref='sl_by_amount')


class ComfirmDialog(QtWidgets.QDialog, Ui_Dialog_order_comfirm):  # 下单的二次确认
    def __init__(self, parent=None, **kwargs):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Dialog_order_comfirm.__init__(self)
        self.setupUi(self)
        self.update_comfirm_info(**kwargs)

    def update_comfirm_info(self, **kwargs):
        self.label_ProdCode.setText(kwargs.get('ProdCode', ''))
        self.label_BuySell.setText({'B': '买入', 'S': '沽出'}.get(kwargs.get('BuySell'), ''))
        self.label_Price.setText(str(kwargs.get('Price', '')))
        self.label_Qty.setText(str(kwargs.get('Qty', '')))
        self.label_Cond.setText(kwargs.get('Cond', ''))
        if kwargs.get('ValidType') != 4:
            validtime = ORDER_VALIDTYPE.get(kwargs['ValidType'])
        else:
            validtime = str(dt.datetime.fromtimestamp(kwargs.get('ValidTime')))

        self.label_VaildTime.setText(validtime)

class MainWindow(QtWidgets.QMainWindow):
    login_sig = pyqtSignal()
    info_sig = pyqtSignal(str, str, int)
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, parent, *args, **kwargs)
        self.resize(1161, 340)
        self.login_status = False
        self.handle_queue = Queue()  # 处理队列
        self.timer = QtCore.QTimer(self)
        self.wechat_info = QWechatInfo(self)  # 微信推送类
        self.order_pub = QPubOrder(self)  # 跟单订单接收类
        self.order_sub = QSubOrder(self.order_pub.order_queue, self)  # 跟单订单处理类
        self.Login = SpLoginDialog(self)  # 登录界面
        self.AccInfo = AccInfoWidget(self)  # 账户信息界面类
        self.OrderStoploss = QOrderStoplossDialog(self)  # 下单与快速止损综合界面
        self.QuickOrder = QuickOrderDialog(self)  # 快速下单界面
        self.OrderAssistant = OrderAssistantWidget(self)  # 辅助下单界面
        self.update_thread = Thread(target=self.info_handler)  # 回调信息的处理进程
        self.update_thread.start()
        self.trayicon = QTrayIcon(self)
        self.var_test = QTest(self)
        self.init_signal()
        self.init_callback()  # 初始化回调函数


    def init_signal(self):
        self.info_sig.connect(self.popup)  # inof_sig连接消息的popup
        self.login_sig.connect(self.show)
        self.login_sig.connect(self.AccInfo.show)
        self.login_sig.connect(lambda: self.Login.close())
        self.login_sig.connect(self.trayicon.show)
        self.AccInfo.checkBox_follow_orders.toggled.connect(
            lambda b: self.init_order_follower() if b else self.deinit_order_follower())  # 绑定跟单的checkbox可以初始化与反初始化跟单
        self.login_sig.connect(lambda: [self.AccInfo.refresh_accbals(), self.AccInfo.refresh_ccy_rate()])  # 登录时更新结余和汇率
        self.login_sig.connect(
            lambda: self.timer.singleShot(3000, lambda: [subscribe_price(p, 1) for p in self.AccInfo.data.sub_list]))  # 登录3秒后会自动订阅sublist的价格，sublist通过持仓的回调函数添加产品代码
        self.AccInfo.pushButton_mt4_order.released.connect(self.init_sql_table)  # 按钮test的测试
        self.AccInfo.pushButton_tradesession.released.connect(self.init_tradesession_table)  # 交易会话
        self.AccInfo.checkBox_wechat_info.clicked.connect(
            lambda b: self.init_wechat_info() if b else self.deinit_wechat_info())  # 微信消息推送的初始化与反初始化
        self.wechat_info.login_sig.connect(self.AccInfo.checkBox_wechat_info.setChecked)  # 微信登入信号为checkbox设置checked
        self.wechat_info.finished.connect(lambda: self.AccInfo.checkBox_wechat_info.setChecked(False))  # 微信消息推送的线程结束后，取消checkbox的checked
        self.Login.pushButton_login.released.connect(lambda: self.init_spapi())  # 登录按钮触发init_spapi
        self.login_sig.connect(self.AccInfo.time.show)

        self.AccInfo.price_update_sig.connect(self.QuickOrder.price_table_update)
        self.AccInfo.price_update_sig.connect(self.QuickOrder.price_info_update)
        self.AccInfo.price_update_sig.connect(self.QuickOrder.holding_profit)
        self.AccInfo.pushButton_Order_Stoploss.released.connect(self.OrderStoploss.show)
        self.AccInfo.pushButton_QuickOrder.released.connect(self.QuickOrder.show)
        self.OrderStoploss.lineEdit_ProdCode.textChanged.connect(lambda text: [self.QuickOrder.lineEdit_ProdCode.setText(text), self.OrderAssistant.lineEdit_ProdCode.setText(text), self.OrderStoploss.lineEdit_prodcode.setText(text)])  # 普通下单与快速下单的代码输入绑定
        self.QuickOrder.lineEdit_ProdCode.textChanged.connect(lambda text: [self.OrderStoploss.lineEdit_ProdCode.setText(text), self.OrderAssistant.lineEdit_ProdCode.setText(text), self.OrderStoploss.lineEdit_prodcode.setText(text)])  # 普通下单与快速下单的代码输入绑定

        self.OrderStoploss.checkBox_lock.toggled.connect(self.QuickOrder.checkBox_Lock.setChecked)  # 普通下单与快速下单的代码输入绑定
        self.QuickOrder.checkBox_Lock.toggled.connect(self.OrderStoploss.checkBox_lock.setChecked)  # 普通下单与快速下单的代码输入绑定
        self.AccInfo.pos_info_sig.connect(self.OrderAssistant.calc_amount_base)
        self.OrderAssistant.oco_close_sig.connect(self.OrderStoploss.oco_close)
        self.QuickOrder.checkBox_Lock.toggled.connect(
            lambda b: self.QuickOrder.position_takeprofit_info_update(self.AccInfo.data.Trade) if b else ...)

        self.trayicon.action_accinfo.toggled.connect(lambda b: [self.setWindowFlags(Qt.Qt.WindowStaysOnTopHint), self.show()] if b else [self.setWindowFlags(Qt.Qt.Window), self.hide()])
        self.trayicon.action_order_stoploss.toggled.connect(lambda b: self.OrderStoploss.setWindowFlags(Qt.Qt.Window | Qt.Qt.WindowStaysOnTopHint)if b else self.OrderStoploss.setWindowFlags(Qt.Qt.Window))
        self.trayicon.action_quickorder.toggled.connect(lambda b: self.QuickOrder.setWindowFlags(Qt.Qt.Window | Qt.Qt.WindowStaysOnTopHint) if b else self.QuickOrder.setWindowFlags(Qt.Qt.Window))
        # self.trayicon.action_order_stoploss.toggled.connect(self.AccInfo.pushButton_Order_Stoploss.setChecked)
        # self.trayicon.action_quickorder.toggled.connect(self.AccInfo.pushButton_QuickOrder.setChecked)

        self.OrderStoploss.checkBox_order_assistant.toggled.connect(self.OrderAssistant.setVisible)
        self.OrderStoploss.moveEvent = lambda a0: self.OrderAssistant.move(a0.pos().x() + self.OrderStoploss.width(), a0.pos().y())

        self.AccInfo.pos_info_sig.connect(self.OrderStoploss.pos_update_sig)
        self.AccInfo.price_update_sig.connect(self.OrderStoploss.update_price)

        self.AccInfo.pushButton_Order_Stoploss.released.connect(self.OrderStoploss.pos_update_sig)
        self.login_sig.connect(self.__load_last_prodcode)

        self.AccInfo.price_update_sig.connect(self.OrderStoploss.update_bid_ask_table)

        self.AccInfo.price_update_sig.connect(lambda p: self.statusBar().showMessage(f'系统时间:{str(dt.datetime.now().time())[0:8]}   数据时间:{str(dt.datetime.fromtimestamp(p["Timestamp"]).time())[0:8]}'))


    def bind_account(self, account_id):
        self.OrderStoploss.comboBox_account.addItem(account_id)

    def save_trade_info(self):
        try:
            conn = pm.connect(host='192.168.2.226', port=3306, user='kairuitouzi', passwd='kairuitouzi', db='carry_investment')
            cursor = conn.cursor()
            trades = get_all_trades_by_array()
            # trades_info = []
            for t in trades:
                trade_dict = {}
                for name, c_type in t._fields_:
                    v = getattr(t, name)
                    v = v if not isinstance(v, bytes) else v.decode()
                    trade_dict[name] = v
                    values = ','.join(['"' + str(v) + '"' for v in trade_dict.values()])
                sql = f'insert into sp_trade_records values({values})'
                print(sql)
                cursor.execute(sql)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

            # trades_info.append(trade_dict)

        # writer = pd.ExcelWriter('交易记录.xlsx')
        # df = pd.DataFrame(trades_info)
        # df.to_excel(writer,f'{dt.datetime.now().date()}', index=False)
        # writer.save()


    def init_spapi(self):  # 初始化SPAPI并登录
        Login = self.Login
        host = Login.lineEdit_host.text()
        port = Login.lineEdit_port.text()
        License = Login.lineEdit_license.text()
        app_id = Login.lineEdit_app_id.text()
        user_id = Login.lineEdit_user_id.text()
        password = Login.lineEdit_password.text()
        info = {'host': host, 'port': int(port), 'License': License, 'app_id': app_id, 'user_id': user_id}

        Login.pickle_info()  # 把登录信息序列化， 缓存了相关信息

        if initialize() == 0:
            self.info_handle('<API>', '初始化成功')
            set_login_info(**info, password=password)
            self.info_handle('<连接>',
                        f"设置登录信息-host:{info['host']} port:{info['port']} license:{info['License']} app_id:{info['app_id']} user_id:{info['user_id']}")
            login()
            self.bind_account(info['user_id'])

    def deinit_spapi(self):  # 登出并反初始化
        if logout() == 0:
            self.info_handle('<连接>', f'{c_char_p_user_id.value.decode()}登出请求发送成功')
            if unintialize() == 0:
                self.info_handle('<API>', '释放成功')
                self.login_status = False

    def popup(self,title, context, e_time=0):  # 主窗体的弹窗方法
        mb = QMessageBox(self)
        mb.move(self.width() - mb.width() - 100, 0)
        mb.setWindowTitle(title)
        mb.setText(context)
        mb.show()
        if e_time != 0:
            self.timer.singleShot(e_time, mb.close)

    def init_order_follower(self):  # 初始化跟单
        self.order_pub.finished.connect(lambda :self.popup('<INFO-跟单>', '交易发布已停止', 8000))
        self.order_sub.finished.connect(lambda : self.popup('<INFO-跟单>', '交易订阅已停止', 5000))
        self.order_pub.started.connect(lambda : self.popup('<INFO-跟单>', '开始发布交易', 8000))
        self.order_sub.started.connect(lambda : self.popup('<INFO-跟单>', '开始订阅交易', 5000))
        self.order_sub.started.connect(lambda : self.wechat_info.send_info_sig.emit('开始跟单'))
        self.order_sub.finished.connect(lambda :self.wechat_info.send_info_sig.emit('停止跟单'))
        self.order_pub.start()
        self.order_sub.start()

    def deinit_order_follower(self):
        self.order_pub.close()
        self.order_sub.close()

    def init_wechat_info(self):  # 初始化微信推送
        self.wechat_info.finished.connect(lambda: self.popup('INFO-微信推送', '关闭微信信息推送'))
        self.wechat_info.start()

    def deinit_wechat_info(self):
        self.wechat_info.close()

    def init_sql_table(self):
        try:
            self.sql_table = QSqlTable('order_detail')
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-SQLTable初始化', f'错误:{e}')

    def init_tradesession_table(self):
        try:
            self.trade_session = QTradeSession()
            self.trade_session.recalc(self.OrderStoploss.lineEdit_ProdCode.text())
            self.trade_session.show()
        except Exception as e:
            QMessageBox.critical(self, 'CRITICAL-TradeSession初始化', f'错误:{e}')
            raise e

    def info_handle(self, type, info, handle_type=0, handler=None, *args, **kwargs):  # 把回调的消息放进消息队列
        if handle_type == 0:
            print('*LOCAL*' + type + info)
            if handler is not None:
                self.handle_queue.put([handler, args, kwargs])
        elif handle_type == 1:
            print('*LOCAL*' + type + info)
            if handler is not None:
                self.handle_queue.put([handler, args, kwargs])
            # AccInfo.message_sig.emit('WARNING', handler.decode('GBK'))

    def info_handler(self):  # 回调的消息队列的处理函数
        while True:
            handler, arg, kwargs = self.handle_queue.get()
            try:
                handler(*arg, **kwargs)
            except Exception as e:
                print(e)

    def __load_last_prodcode(self):
        if os.path.exists('LP.plk'):
            try:
                with open('LP.plk', 'rb') as lp:
                    prodcode = pickle.load(lp)
                    self.OrderStoploss.lineEdit_ProdCode.setText(prodcode)
                self.timer.singleShot(5000, lambda :subscribe_price(prodcode, 1))
            except Exception as e:
                print(e)

    def __save_last_prodcode(self):
        try:
            with open('LP.plk', 'wb') as lp:
                prodcode = self.OrderStoploss.lineEdit_ProdCode.text()
                pickle.dump(prodcode, lp)
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '退出', "是否要退出SP下单？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.__save_last_prodcode()
            self.save_trade_info()
            a0.accept()
            logout()
            unintialize()
            pid = os.getpid()
            os.system(f'taskkill /F /PID {pid}')
        else:
            a0.ignore()

    def init_callback(self):  # 初始化SPAPI的回调函数
        info_handle = self.info_handle
        AccInfo = self.AccInfo
        Login = self.Login

        @on_login_reply  # 登录调用
        def login_reply(user_id, ret_code, ret_msg):
            if ret_code == 0:
                info_handle('<账户>', f'{user_id.decode()}登录成功', 0, self.login_sig.emit)
                self.login_status = True

            else:
                info_handle('<账户>', f'{user_id.decode()}登录失败--errcode:{ret_code}--errmsg:{ret_msg.decode()}', 0,
                            Login.login_error_sig.emit, f'登录失败-{ret_msg.decode()}')
                self.login_status = False

        @on_business_date_reply  # 登录成功后会返回一个交易日期
        def business_date_reply(business_date):
            print('<日期>', f'当前交易日--{dt.datetime.fromtimestamp(business_date)}')

        @on_account_info_push  # 普通客户登入后返回登入前的户口信息
        def account_info_push(acc_info):
            info_handle('<账户>',
                        f'{acc_info.ClientId.decode()}信息--NAV:{acc_info.NAV}-BaseCcy:{acc_info.BaseCcy.decode()}-BuyingPower:{acc_info.BuyingPower}-CashBal:{acc_info.CashBal}',
                        0, AccInfo._refresh_acc_info, acc_info)

        @on_load_trade_ready_push  # 登入后，登入前已存的成交信息推送
        def trade_ready_push(rec_no, trade):
            info_handle('<成交>',
                        f'历史成交记录--NO:{rec_no}--{trade.OpenClose.decode()}成交@{trade.ProdCode.decode()}--{trade.BuySell.decode()}--Price:{trade.AvgPrice}--Qty:{trade.Qty}',
                        0, AccInfo._refresh_trade, trade)

        @on_account_position_push  # 普通客户登入后返回登入前的已存在持仓信息
        def account_position_push(pos):
            info_handle('<持仓>',
                        f'历史持仓信息--ProdCode:{pos.ProdCode.decode()}-PLBaseCcy:{pos.PLBaseCcy}-PL:{pos.PL}-Qty:{pos.Qty}-DepQty:{pos.DepQty}',
                        0, AccInfo._refresh_postion, pos)

        # @on_ticker_update  # ticker数据推送
        # def ticker_update(ticker):
        #     ...
        #
        #

        @on_api_price_update  # price数据推送
        def price_update(price):
            price_dict = {}
            for name, c_type in price._fields_:
                price_dict[name] = getattr(price, name)
            AccInfo.price_update_sig.emit(price_dict)

        @on_connecting_reply  # 连接状态改变时调用
        def connecting_reply(host_id, con_status):
            info_handle('<连接>', f'{HOST_TYPE[host_id]}状态改变--{HOST_CON_STATUS[con_status]}')

        # -----------------------------------------------登入后的新信息回调------------------------------------------------------------------------------
        @on_order_request_failed  # 订单请求失败时候调用
        def order_request_failed(action, order, err_code, err_msg):
            info_handle('<订单>',
                        f'请求失败--ACTION:{action}-@{order.ProdCode.decode()}-Price:{order.Price}-Qty:{order.Qty}-BuySell:{order.BuySell.decode()}      errcode;{err_code}-errmsg:{err_msg.decode()}',
                        1, AccInfo.warning_sig.emit, 'WARNING-Order Failed', err_msg.decode('GBK'))

        @on_order_before_send_report  # 订单发送前调用
        def order_before_snd_report(order):
            cond = get_order_cond(order)
            info = f"""
            代码:{order.ProdCode.decode()}\n
            方向:{dict(B='买入', S='沽出').get(order.BuySell.decode(), '')}\n
            价格:{order.Price}\n
            数量:{order.Qty}\n
            条件:{cond}"""
            info_handle('<订单>',
                        f'即将发送请求--@{order.ProdCode.decode()}-Price:{order.Price}-Qty:{order.Qty}-BuySell:{order.BuySell.decode()}',
                        0, AccInfo.info_sig.emit, 'INFO-Order Before Send', info)

        @on_order_report  # 订单报告的回调推送
        def order_report(rec_no, order):
            info_handle('<订单>', f'编号:{rec_no}-@{order.ProdCode.decode()}-Status:{ORDER_STATUS[order.Status]}', 0,
                        AccInfo._refresh_order, order)

        @on_trade_report  # 成交记录更新后回调出推送新的成交记录
        def trade_report(rec_no, trade):
            info_handle('<成交>',
                        f'{rec_no}新成交{trade.OpenClose.decode()}--@{trade.ProdCode.decode()}--{trade.BuySell.decode()}--Price:{trade.AvgPrice}--Qty:{trade.Qty}',
                        0, AccInfo._refresh_trade, trade)

        @on_updated_account_position_push  # 新持仓信息
        def updated_account_position_push(pos):
            info_handle('<持仓>',
                        f'信息变动--@{pos.ProdCode.decode()}-PLBaseCcy:{pos.PLBaseCcy}-PL:{pos.PL}-Qty:{pos.Qty}-DepQty:{pos.DepQty}',
                        0, AccInfo._refresh_postion, pos)

        @on_updated_account_balance_push  # 户口账户发生变更时的回调，新的账户信息
        def updated_account_balance_push(acc_bal):
            info_handle('<结余>',
                        f'信息变动-{acc_bal.Ccy.decode()}-CashBF:{acc_bal.CashBF}-TodayCash:{acc_bal.TodayCash}-NotYetValue:{acc_bal.NotYetValue}-Unpresented:{acc_bal.Unpresented}-TodayOut:{acc_bal.TodayOut}',
                        0, AccInfo._refresh_accbals, acc_bal)

        # ------------------------------------------------------------------------------------------------------------------------------------------------------------

        # ------------------------------------------------------------请求回调函数------------------------------------------------------------------------------------

        @on_instrument_list_reply  # 产品系列信息的回调推送，用load_instrument_list()触发
        def inst_list_reply(req_id, is_ready, ret_msg):
            if is_ready:
                info_handle('<产品>', f'信息加载成功      req_id:{req_id}-msg:{ret_msg.decode()}')
            else:
                info_handle('<产品>', f'信息正在加载......req_id{req_id}-msg:{ret_msg.decode()}')

        @on_product_list_by_code_reply  # 根据产品系列名返回合约信息
        def product_list_by_code_reply(req_id, inst_code, is_ready, ret_msg):
            if is_ready:
                if inst_code == '':
                    info_handle('<合约>', f'该产品系列没有合约信息      req_id:{req_id}-msg:{ret_msg.decode()}')
                else:
                    info_handle('<合约>', f'产品:{inst_code.decode()}合约信息加载成功      req_id:{req_id}-msg:{ret_msg.decode()}')
            else:
                info_handle('<合约>', f'产品:{inst_code.decode()}合约信息正在加载......req_id:{req_id}-msg:{ret_msg.decode()}')

        @on_pswchange_reply  # 修改密码调用
        def pswchange_reply(ret_code, ret_msg):
            if ret_code == 0:
                info_handle('<密码>', '修改成功')
            else:
                info_handle('<密码>', f'修改失败  errcode:{ret_code}-errmsg:{ret_msg.decode()}')

        self.callback = [login_reply, business_date_reply, account_info_push, trade_ready_push, account_position_push, price_update, connecting_reply,
                         order_request_failed, order_before_snd_report, order_report, trade_report, updated_account_position_push, updated_account_balance_push,
                         inst_list_reply, product_list_by_code_reply, pswchange_reply]  # 把所有callback存在一个list，防止GC


class TimeWidget(QtWidgets.QWidget, Ui_Form_time):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_time.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.CoverWindow | Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnBottomHint)
        self.timer = QtCore.QTimer(self)
        self.init_signal()
        self.move(0, 0)

    def init_signal(self):
        self.timer.timeout.connect(self.update_sys_time)
        self.timer.start(1000)
        self.parent().price_update_sig.connect(lambda p:self.update_data_time(p['Timestamp']))

    def update_sys_time(self):
        t = dt.datetime.now().time()
        self.label_sys_time.setText(str(t)[:8])

    def update_data_time(self, timestamp):
        t = dt.datetime.fromtimestamp(timestamp).time()
        self.label_data_time.setText(str(t)[:8])

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        if self._isTracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


class QTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        self.init_Menu()
        self.init_icon()
        self.init_signal()
        self.setVisible(False)

    def init_Menu(self):
        self.menu = QtWidgets.QMenu()
        self.menu_suspen = QtWidgets.QMenu()
        self.menu_suspen.setTitle('悬浮置顶')
        self.action_accinfo = QtWidgets.QAction('账户', self, checkable=True)
        self.action_order_stoploss = QtWidgets.QAction('下单与止损', self, checkable=True)
        self.action_quickorder = QtWidgets.QAction('点击下单', self, checkable=True)
        self.action_quit = QtWidgets.QAction("退出", self)
        self.menu_suspen.addAction(self.action_accinfo)
        self.menu_suspen.addAction(self.action_order_stoploss)
        self.menu_suspen.addAction(self.action_quickorder)
        self.menu.addMenu(self.menu_suspen)
        self.menu.addAction(self.action_quit)
        self.setContextMenu(self.menu)

    def init_icon(self):
        self.setIcon(QIcon(os.path.join('ui', 'trayicon.png')))
        self.icon = self.MessageIcon()

    def init_signal(self):
        self.action_quit.triggered.connect(lambda :self.parent().close())


class QTest(QtCore.QThread):   # 测试用的
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        try:
            H_price = get_price_by_code('HSIK8')
            M_pirce = get_price_by_code('MHIK8')
            sql = f'insert into var_testing values("{str(dt.datetime.now())[:19]}", {H_price.Ask[0]}, {H_price.Bid[0]}, {H_price.Last[0]}, {M_pirce.Ask[0]}, {M_pirce.Bid[0]}, {M_pirce.Last[0]})'
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def open(self):
        self.conn = pm.connect(host='127.0.0.1', port=3306, user='hadrianl', passwd='kairuitouzi', db='carry_investment')
        self.cursor = self.conn.cursor()


class QTradeSession(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.setWindowTitle('TradeSession')
        self.verticalHeader().setHidden(True)
        self.HS = HS()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.resize(500, 800)

    def recalc(self, prodcode):
        raw_data = self.HS.get_data(prodcode)
        data = self.HS.ray(raw_data)
        self.clear()
        columns = data.columns
        index = data.index
        self.setColumnCount(len(columns))
        self.setRowCount(len(index))
        for c in range(len(columns)):
            self.setHorizontalHeaderItem(c, QTableWidgetItem(columns[c]))
            for i in range(len(index)):
                self.setItem(i, c, QTableWidgetItem(str(data.iat[i, c])))


class QOrderStoplossDialog(QDialog, Ui_Dialog_order_stoploss):
    pos_update_sig = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog_order_stoploss.__init__(self)
        self.setupUi(self)
        self.init_state()
        self.init_signal()

    def init_state(self):
        self.setWindowFlags(Qt.Qt.Window)
        self.dateEdit_ValidTime.setDate(dt.datetime.now().date())
        self.dateTimeEdit_sched_time.setDateTime(dt.datetime.now())
        self.spinBox_market_level.setDisabled(True)
        self.label_ValidTime.setHidden(True)
        self.dateEdit_ValidTime.setHidden(True)
        self.spinBox_Price.setSpecialValueText(' ')
        self.spinBox_StopLevel.setSpecialValueText(' ')
        self.spinBox_StopLevel2.setSpecialValueText(' ')
        self.spinBox_oco_StopLevel.setSpecialValueText(' ')
        self.price_items = []
        self.qty_items = []
        for i in range(10):
            pitem = QTableWidgetItem('')
            qitem = QTableWidgetItem('')
            self.tableWidget_bid_ask.setItem(i, 0, pitem)
            self.tableWidget_bid_ask.setItem(i, 1, qitem)
            self.price_items.append(pitem)
            self.qty_items.append(qitem)
        self._price_flag = True
        self._sl_flag = True
        self._sl2_flag = True
        self._oco_sl_flag = True
        self.holding_qty = 0
        self.holding_pos = []
        self.session_pos = []
        self.all_pos = []
        self.tableWidget_bid_ask.setVisible(False)
        self.resize(510, 350)
        # desktop = QDesktopWidget()
        # self.move(desktop.width() - self.width(),(desktop.height() - self.height())/2 - 70)

    def init_signal(self):
        self.comboBox_CondType.activated.connect(lambda n: (self.spinBox_Price.setDisabled(n in [1]),
                                                            self.checkBox_Auction.setHidden(n in [1, 2, 3, 4]),
                                                            self.checkBox_Auction.setCheckState(0),
                                                            self.checkBox_Market.setHidden(n in [1, 2, 4]),
                                                            self.checkBox_Market.setCheckState(0),
                                                            self.checkBox_stop_tri.setCheckState(0),
                                                            self.comboBox_ValidType.setCurrentIndex(0),
                                                            self.checkBox_invalid.setEnabled(n in [0, 3]),
                                                            self.checkBox_invalid.setCheckable(n in [0, 3]),
                                                            self.pushButton_buy.setHidden(n in [1, 2]),
                                                            self.pushButton_sell.setHidden(n in [1, 2]),
                                                            self.spinBox_Price.setValue(0) if n in [2] else ...,
                                                            setattr(self, '_price_flag', True),
                                                            setattr(self, '_sl_flag', True),
                                                            setattr(self, '_sl2_flag', True),
                                                            setattr(self, '_oco_sl_flag', True)
                                                            ))
        self.comboBox_ValidType.currentIndexChanged.connect(lambda n: (
                                                             self.checkBox_stop_tri.setCheckState(0) if n in [1, 2] else ...,
                                                             self.checkBox_Auction.setEnabled(n in [0]),
                                                             self.checkBox_Market.setEnabled(n in [0]),
                                                             self.checkBox_stop_tri.setEnabled(n in [0, 3, 4]),
                                                             self.dateEdit_ValidTime.setVisible(n in [4]),
                                                             self.dateEdit_ValidTime.setEnabled(n in [4]),
                                                             self.label_ValidTime.setVisible(n in [4]),
                                                             ))
        self.checkBox_stop_tri.toggled.connect(lambda x: (self.comboBox_StopType.setCurrentIndex(0) if not x else ...,
                                                          self.spinBox_StopLevel.setValue(0) if not x else ...))
        self.checkBox_Market.toggled.connect(lambda x: (self.spinBox_Price.setValue(0) if x else ...,
                                                        ))
        self.checkBox_Auction.toggled.connect(lambda x: (self.spinBox_Price.setValue(0x7fffffff) if x else self.spinBox_Price.setValue(0),
                                                         ))
        self.comboBox_StopType.activated.connect(lambda n: self.checkBox_Market.setChecked(n in [3]))
        self.spinBox_StopLevel2.valueChanged.connect(lambda x: self.spinBox_Price.setValue(x + self.spinBox_toler.value()if self.radioButton_buy1.isChecked() else x - self.spinBox_toler.value())if not self.checkBox_Market.checkState() else 0)
        self.spinBox_toler.valueChanged.connect(lambda x: self.spinBox_Price.setValue((x + self.spinBox_StopLevel2.value() if self.radioButton_buy1.isChecked() else self.spinBox_StopLevel2.value() - x) if not self.checkBox_Market.checkState() else 0))
        self.radioButton_buy1.toggled.connect(lambda x: self.spinBox_Price.setValue(self.spinBox_StopLevel2.value() + self.spinBox_toler.value()))
        self.radioButton_sell1.toggled.connect(lambda x: self.spinBox_Price.setValue(self.spinBox_StopLevel2.value() - self.spinBox_toler.value()))
        self.spinBox_oco_StopLevel.valueChanged.connect(lambda x: self.label_oco_pirce.setText(f'{x + self.spinBox_oco_toler.value() if self.radioButton_buy2.isChecked() else x - self.spinBox_oco_toler.value()}'))
        self.spinBox_oco_toler.valueChanged.connect(lambda x: self.label_oco_pirce.setText(f'{x + self.spinBox_oco_StopLevel.value() if self.radioButton_buy2.isChecked() else self.spinBox_oco_StopLevel.value() - x}'))
        self.radioButton_buy2.toggled.connect(lambda x: self.label_oco_pirce.setText(f'{self.spinBox_oco_StopLevel.value() + self.spinBox_oco_toler.value()}'))
        self.radioButton_sell1.toggled.connect(lambda x: self.label_oco_pirce.setText(f'{self.spinBox_oco_StopLevel.value() - self.spinBox_oco_toler.value()}'))
        self.spinBox_Price.valueChanged.connect(lambda x: (self.spinBox_Price.setValue(int(get_price_by_code(self.lineEdit_ProdCode.text()).Last[0])), setattr(self, '_price_flag', False)) if self._price_flag else ...)
        self.spinBox_StopLevel.valueChanged.connect(lambda x: (self.spinBox_StopLevel.setValue(int(get_price_by_code(self.lineEdit_ProdCode.text()).Last[0])), setattr(self, '_sl_flag', False)) if self._sl_flag else ...)
        self.spinBox_StopLevel2.valueChanged.connect(lambda x: (self.spinBox_StopLevel2.setValue(int(get_price_by_code(self.lineEdit_ProdCode.text()).Last[0])), setattr(self, '_sl2_flag', False)) if self._sl2_flag else ...)
        self.spinBox_oco_StopLevel.valueChanged.connect(lambda x: (self.spinBox_oco_StopLevel.setValue(int(get_price_by_code(self.lineEdit_ProdCode.text()).Last[0])), setattr(self, '_oco_sl_flag', False)) if self._oco_sl_flag else ...)
        self.pushButton_buy.released.connect(lambda :self.order('B'))
        self.pushButton_sell.released.connect(lambda :self.order('S'))
        # self.checkBox_lock.toggled.connect(lambda x: subscribe_price(self.lineEdit_ProdCode.text(), 1) if x else subscribe_price(self.lineEdit_ProdCode.text(), 0))
        self.rejected.connect(lambda : self.checkBox_order_assistant.setChecked(False))

        self.pos_update_sig.connect(
            lambda: [self.update_holding_pos_LIFO(), self.update_session_pos(), self.update_all_pos()])
        self.pushButton_stoploss.released.connect(self.quick_stoploss)
        self.pushButton_del_all_orders.released.connect(delete_all_orders)
        self.pushButton_del_long_sl.released.connect(self.del_long_sl)
        self.pushButton_del_short_sl.released.connect(self.del_short_sl)
        self.pushButton_del_remain_sl.released.connect(self.del_remain_sl)
        self.groupBox_price.toggled.connect(lambda b: self.resize(510, 700) if b else self.resize(510, 350))
        self.tableWidget_bid_ask.itemDoubleClicked.connect(lambda item: self.spinBox_Price.setValue(int(float(item.text()))) if item.column() ==  0 else ...)

    def update_bid_ask_table(self, price):
        if self.tableWidget_bid_ask.isEnabled() and price['ProdCode'].decode() == self.lineEdit_ProdCode.text():
            for i, (b, bq) in enumerate(zip(price['Bid'][0:5], price['BidQty'][0:5])):
                bid_item = self.price_items[5 + i]
                bid_qty_item = self.qty_items[5 + i]
                bid_item.setForeground(QColor('#FF0000'))
                bid_qty_item.setBackground(QColor('#FF0000') if bq >= 10 else QColor('#FFFFFF'))
                bid_item.setText(str(b))
                bid_qty_item.setText(str(bq))

            for i, (a, aq) in enumerate(zip(price['Ask'][0:5], price['AskQty'][0:5])):
                ask_item = self.price_items[4 - i]
                ask_qty_item = self.qty_items[4 -i]
                ask_item.setForeground(QColor('#00FF00'))
                ask_qty_item.setBackground(QColor('#00FF00') if aq >= 10 else QColor('#FFFFFF'))
                ask_item.setText(str(a))
                ask_qty_item.setText(str(aq))

            self.tableWidget_bid_ask.viewport().update()


    def order(self, BuySell):
        try:
            order_kwargs = {}
            order_kwargs['BuySell'] = BuySell
            order_kwargs['ProdCode'] = self.lineEdit_ProdCode.text()
            current_price = get_price_by_code(order_kwargs['ProdCode'])
            order_kwargs['Qty'] = self.spinBox_Qty.value()
            order_kwargs['Ref'] = self.lineEdit_Ref.text()
            order_kwargs['OrderOptions'] = 1 if self.checkBox_OrderOptions.checkState() else 0
            _condtype_index = self.comboBox_CondType.currentIndex()
            order_kwargs['CondType'] = {0: 0, 1: 1, 2: 4,3: 0, 4: 3}[_condtype_index]
            if _condtype_index == 0:
                _order_type = (self.checkBox_Auction.checkState() << 1) + self.checkBox_Market.checkState()
                order_kwargs['OrderType'] = {0: 0, 2: 6, 4: 2}[_order_type]
                order_kwargs['Price'] = {0: self.spinBox_Price.value(), 2: 0, 4: 0x7fffffff}[_order_type]
                order_kwargs['ValidType'] = self.comboBox_ValidType.currentIndex()

                if order_kwargs['ValidType'] == 4:
                    order_kwargs['ValidTime'] = int(dt.datetime.strptime(self.dateEdit_ValidTime.date().toPyDate().strftime('%Y/%m/%d'),
                                                         '%Y/%m/%d').timestamp())
                if self.checkBox_stop_tri.isChecked():
                    order_kwargs['StopType'] = {0: 'L', 1: 'U', 2: 'D', 3: 'L'}[self.comboBox_StopType.currentIndex()]
                    order_kwargs['StopLevel'] = self.spinBox_StopLevel.value()
                    order_kwargs['CondType'] = 1
                else:
                    order_kwargs['StopLevel'] = 0

            elif _condtype_index == 1:
                order_kwargs['StopType'] = 'L'
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = (self.spinBox_StopLevel2.value() + self.spinBox_toler.value()) if BuySell == 'B' \
                    else (self.spinBox_StopLevel2.value() - self.spinBox_toler.value())
                order_kwargs['StopLevel'] = self.spinBox_StopLevel2.value()
                if self.checkBox_Trailing_Stop.isChecked():
                    order_kwargs['CondType'] = 6

                    if BuySell == 'B':
                        order_kwargs['UpLevel'] = current_price.Ask[0]
                        order_kwargs['UpPrice'] = order_kwargs['StopLevel']
                        order_kwargs['DownLevel'] = self.spinBox_trailing_stop_step.value()
                    else:
                        order_kwargs['DownLevel'] = current_price.Bid[0]
                        order_kwargs['DownPrice'] = order_kwargs['StopLevel']
                        order_kwargs['UpLevel'] = self.spinBox_trailing_stop_step.value()

            elif _condtype_index == 2:
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = self.spinBox_Price.value()

                if BuySell == 'B':
                    order_kwargs['UpLevel'] = self.spinBox_oco_StopLevel.value()
                    order_kwargs['UpPrice'] = self.spinBox_oco_StopLevel.value() + self.spinBox_oco_toler.value()
                else:
                    order_kwargs['DownLevel'] = self.spinBox_oco_StopLevel.value()
                    order_kwargs['DownPrice'] = self.spinBox_oco_StopLevel.value() - self.spinBox_oco_toler.value()

            elif _condtype_index == 3:
                order_kwargs['ValidType'] = 0
                _profit = self.spinBox_bullbear_profit.value()
                _loss = self.spinBox_bullbear_loss.value()
                _loss_toler = self.spinBox_bullbear_loss_toler.value()
                order_kwargs['Price'] = Price = self.spinBox_Price.value()

                if BuySell == 'B':
                    order_kwargs['UpLevel'] = Price + _profit
                    order_kwargs['UpPrice'] = Price + _profit
                    order_kwargs['DownLevel'] = Price - _loss
                    order_kwargs['DownPrice'] = Price - _loss - _loss_toler
                else:
                    order_kwargs['DownLevel'] = Price - _profit
                    order_kwargs['DownPrice'] = Price - _profit
                    order_kwargs['UpLevel'] = Price + _loss
                    order_kwargs['UpPrice'] = Price + _loss + _loss_toler

            elif _condtype_index == 4:
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = self.spinBox_Price.value()
                _sched_time = self.dateTimeEdit_sched_time.dateTime().toPyDateTime()
                order_kwargs['SchedTime'] = int(_sched_time.timestamp())

            cond = get_order_cond(order_kwargs)
        except Exception as e:
            print(e)
            # raise e
        else:
            comfirm_order = ComfirmDialog(self, Cond=cond, **order_kwargs)

            if self.checkBox_invalid.isChecked():
                comfirm_order.label_subtitle.setText('新增无效指示')
                comfirm_order.show()
                comfirm_order.accepted.connect(lambda: add_inactive_order(**order_kwargs))
            else:
                comfirm_order.show()
                comfirm_order.accepted.connect(lambda : add_order(**order_kwargs))

    def oco_close(self, prodcode, net_qty, tp, sl):
        print( prodcode, net_qty, tp, sl)
        self.comboBox_CondType.setCurrentIndex(2)
        self._price_flag = False
        self._oco_sl_flag = False

        if net_qty > 0:
            self.lineEdit_ProdCode.setText(prodcode)
            self.lineEdit_ProdCode.update()
            self.radioButton_sell2.toggle()
            self.spinBox_Qty.setValue(net_qty)
            self.spinBox_Price.setValue(tp)
            self.spinBox_oco_StopLevel.setValue(sl)
            self.spinBox_oco_toler.setValue(5)
            self.show()
            self.checkBox_lock.setChecked(True)
        elif net_qty < 0:
            self.lineEdit_ProdCode.setText(prodcode)
            self.lineEdit_ProdCode.update()
            self.radioButton_buy2.toggle()
            self.spinBox_Qty.setValue(-net_qty)
            self.spinBox_Price.setValue(tp)
            self.spinBox_oco_StopLevel.setValue(sl)
            self.spinBox_oco_toler.setValue(5)
            self.show()
            self.checkBox_lock.setChecked(True)


    def _get_holding_pos(self, trades_info):  # 获取持仓
        prodcode = self.lineEdit_prodcode.text()
        current_trades = [{'TradeTime': trade['TradeTime'], 'Qty': trade['Qty'] if trade['BuySell'] == b'B' else -trade['Qty'], 'Price': trade['AvgPrice']} for Id, trade in trades_info.items() if trade['ProdCode'].decode('GBK') == prodcode]

        pos = get_pos_by_product(prodcode)
        if pos.Qty != 0:
            qty = pos.Qty if pos.LongShort == b'B' else -pos.Qty
            price = pos.TotalAmt  / abs(qty)
            remain_pos = {'TradeTime': 0, 'Qty': qty, 'Price': price}
            current_trades.append(remain_pos)
        print(current_trades)
        current_trades.sort(key=lambda x:x['TradeTime'])
        print(current_trades)

        holding_pos = [0 , 0]
        for t in current_trades:
            holding_qty = holding_pos[0] + t['Qty']
            hodling_price = (holding_pos[1] * holding_pos[0] + t['Price'] * t['Qty']) / holding_qty if holding_qty != 0 else 0
            holding_pos = [holding_qty, hodling_price]

        return holding_pos

    def update_holding_pos_LIFO(self):  # 后进先出方法计算持仓
        try:
            self.holding_qty, holding_price = self._get_holding_pos(self.parent().AccInfo.data.Trade)
            self.holding_pos = [self.holding_qty, holding_price]
        except Exception as e:
            self.lineEdit_hodling_pos.setText('-')
        else:
            if self.holding_qty != 0:
                self.lineEdit_hodling_pos.setText(f'{self.holding_qty}@{holding_price:.2f}')
            else:
                self.lineEdit_hodling_pos.setText('-@-')

    def update_session_pos(self):
        try:
            hs = HS()
            raw_data = hs.get_data(self.lineEdit_prodcode.text())
            data = hs.ray(raw_data)
            if not data.empty:
                d = data.iloc[-1]
                session_holding_pos = d['持仓']
                session_net_cost = d['净会话成本']
            else:
                raise Exception('无交易信息')
        except Exception as e:
            self.lineEdit_session_pos.setText('-')
            print(e)
        else:
            if session_holding_pos != 0:
                self.lineEdit_session_pos.setText(f'{session_holding_pos}@{session_net_cost}')
                self.session_pos = [session_holding_pos, session_net_cost]
            else:
                self.lineEdit_session_pos.setText('-@-')

    def update_all_pos(self):
        try:
            pos = self.parent().AccInfo.tableWidget_pos

            for r in range(pos.rowCount()):
                if pos.item(r, 0).text() == self.lineEdit_prodcode.text():
                    text = pos.item(r, 7).text()
                    self.lineEdit_all_pos.setText(text)
                    self.all_pos = [int(float(v)) for v in text.split('@')]
                    break
            else:
                raise Exception('无持仓信息')
        except Exception as e:
            self.lineEdit_all_pos.setText('-')
            print(e)

    def update_price(self, price_dict):
        prodcode = self.lineEdit_prodcode.text()
        if price_dict['ProdCode'].decode() == prodcode:
            self.groupBox_quick_sl.setTitle(f'{prodcode}@{price_dict["Last"][0]}')

    def quick_stoploss(self):
        try:
            if self.radioButton_holding.isChecked():
                qty, price = self.holding_pos
            elif self.radioButton_session.isChecked():
                qty, price = self.session_pos
            elif self.radioButton_all.isChecked():
                qty, price = self.all_pos
            else:
                raise Exception('请选择止损方式')
        except Exception as e:
            QMessageBox.warning(self, '<WARING>止损', f'无法获取持仓:{e}')
            return
        lock = self.spinBox_lock.value()

        if qty > 0 :
            if qty > lock:
                q = qty - lock
                stoplevel = price - self.spinBox_stoploss_addtion.value()
                stopprice = stoplevel - self.spinBox_sl_toler.value()
                order_kwargs = dict(ProdCode=self.lineEdit_prodcode.text(), BuySell='S', OrderOptions=0,
                          Qty=q, ValidType=0, CondType=1, OrderType=0, Price=round(stopprice),
                          StopType='L', StopLevel=round(stoplevel),
                          Ref='quick_sl-short')
                cond = get_order_cond(order_kwargs)
                comfirm_order = ComfirmDialog(self, Cond=cond, **order_kwargs)
                comfirm_order.show()
                comfirm_order.accepted.connect(lambda: add_order(**order_kwargs))
            else:
                QMessageBox.warning(self, '<WARING>止损', '全部仓位已锁定,请重新设置锁定仓位')
        elif qty < 0:
            if -qty > lock:
                q = -qty - lock
                stoplevel = price + self.spinBox_stoploss_addtion.value()
                stopprice = stoplevel + self.spinBox_sl_toler.value()

                order_kwargs = dict(ProdCode=self.lineEdit_prodcode.text(), BuySell='B', OrderOptions=0,
                          Qty=q, ValidType=0, CondType=1, OrderType=0, Price=round(stopprice),
                          StopType='L', StopLevel=round(stoplevel),
                          Ref='quick_sl-long')
                cond = get_order_cond(order_kwargs)
                comfirm_order = ComfirmDialog(self, Cond=cond, **order_kwargs)
                comfirm_order.show()
                comfirm_order.accepted.connect(lambda: add_order(**order_kwargs))
            else:
                QMessageBox.warning(self,  '<WARING>止损', '全部仓位已锁定, ,请重新设置锁定仓位')

    def del_long_sl(self):
        try:
            orders = get_orders_by_array()
            for o in orders:
                if 'quick_sl-long' in o.Ref.decode():
                    o_id = o.IntOrderNo
                    o_prodcode = o.ProdCode.decode()
                    delete_order_by(o_id, o_prodcode)
        except Exception as e:
            QMessageBox.warning(self, '<WARING>删除止损', f'错误:{e}')

    def del_short_sl(self):
        try:
            orders = get_orders_by_array()
            for o in orders:
                if 'quick_sl-short' in o.Ref.decode():
                    o_id = o.IntOrderNo
                    o_prodcode = o.ProdCode.decode()
                    delete_order_by(o_id, o_prodcode)
        except Exception as e:
            QMessageBox.warning(self, '<WARING>删除止损', f'错误:{e}')

    def del_remain_sl(self):
        try:
            orders = get_orders_by_array()
            for o in orders:
                if 'quick_sl' in o.Ref.decode():
                    o_id = o.IntOrderNo
                    o_prodcode = o.ProdCode.decode()
                    delete_order_by(o_id, o_prodcode)
        except Exception as e:
            QMessageBox.warning(self, '<WARING>删除止损', f'错误:{e}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    od = OrderDialog()
    od.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(app.exec())

    import pandas as pd
    a = pd.DataFrame()
