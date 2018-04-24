#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/30 0030 11:40
# @Author  : Hadrianl 
# @File    : Spfunc.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.Qt import QDialog, QDesktopWidget, QTableWidgetItem, QIcon, QSize, QColor, QFont
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
import sys
from ui.order_dialog import Ui_Dialog
from ui.acc_info import Ui_Form_acc_info
from ui.sp_login import Ui_Dialog_sp_login
import datetime as dt
from spapi.spAPI import *
import os
import pickle
from ui.quick_order import Ui_Form_quick_order
# from sp_func.local import addOrder

class OrderDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self._price_flag = True
        self.init_state()
        self.init_signal()

    def init_state(self):
        self.dateEdit_ValidTime.setDate(dt.datetime.now().date())
        self.dateTimeEdit_sched_time.setDateTime(dt.datetime.now())
        self.spinBox_market_level.setDisabled(True)
        self.label_ValidTime.setHidden(True)
        self.dateEdit_ValidTime.setHidden(True)
        self.spinBox_Price.setSpecialValueText(' ')
        self.spinBox_StopLevel.setSpecialValueText(' ')
        self.spinBox_StopLevel2.setSpecialValueText(' ')
        self.spinBox_oco_StopLevel.setSpecialValueText(' ')
        desktop = QDesktopWidget()
        self.move(desktop.width() - self.width(),(desktop.height() - self.height())/2 - 70)
        # self.spinBox_Price.set


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
                                                            setattr(self, '_price_flag', True)
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

        self.spinBox_Price.valueChanged.connect(lambda x: (self.spinBox_Price.setValue(30000), setattr(self, '_price_flag', False)) if self._price_flag else ...)
        self.spinBox_StopLevel.valueChanged.connect(lambda x: (self.spinBox_StopLevel.setValue(30000), setattr(self, '_price_flag', False)) if self._price_flag else ...)
        self.spinBox_StopLevel2.valueChanged.connect(lambda x: (self.spinBox_StopLevel2.setValue(30000), setattr(self, '_price_flag', False)) if self._price_flag else ...)
        self.spinBox_oco_StopLevel.valueChanged.connect(lambda x: (self.spinBox_oco_StopLevel.setValue(30000), setattr(self, '_price_flag', False)) if self._price_flag == 1 else ...)
        self.pushButton_buy.released.connect(lambda :self.order('B'))
        self.pushButton_sell.released.connect(lambda :self.order('S'))
        self.checkBox_lock.toggled.connect(lambda x: subscribe_price(self.lineEdit_ProdCode.text(), 1) if x else subscribe_price(self.lineEdit_ProdCode.text(), 0))


    def order(self, BuySell):
        try:
            order_kwargs = {}
            order_kwargs['BuySell'] = BuySell
            order_kwargs['ProdCode'] = self.lineEdit_ProdCode.text()
            order_kwargs['Qty'] = self.spinBox_Qty.value()
            order_kwargs['Ref'] = self.lineEdit_Ref.text()
            order_kwargs['OrderOption'] = self.checkBox_OrderOptions.checkState()
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
                order_kwargs['Price'] = (self.spinBox_StopLevel2.value() + self.spinBox_toler.value()) if BuySell == 'B' \
                    else (self.spinBox_StopLevel2.value() - self.spinBox_toler.value())
                order_kwargs['StopLevel'] = self.spinBox_StopLevel2.value()
                if self.checkBox_Trailing_Stop.isChecked():
                    order_kwargs['CondType'] = 6
                    order_kwargs['ValidType'] = 0
                    current_price = get_price_by_code(order_kwargs['ProdCode'])
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
                ...
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
                ...
            elif _condtype_index == 4:
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = self.spinBox_Price.value()
                order_kwargs['SchedTime'] = int(self.dateTimeEdit_sched_time.dateTime().toPyDateTime().timestamp())
        except Exception as e:
            raise e
        add_order(**order_kwargs)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '退出', "是否要退出SP下单？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            a0.accept()
            # pid = os.getpid()
            # os.system(f'taskkill /F /PID {pid}')
        else:
            a0.ignore()


class AccInfoWidget(QtWidgets.QWidget, Ui_Form_acc_info):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_acc_info.__init__(self)
        self.setupUi(self)
        desktop = QDesktopWidget()
        self.move(desktop.width() - self.width(), (desktop.height() + self.height()) / 2)



class SpLoginDialog(QDialog, Ui_Dialog_sp_login):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog_sp_login.__init__(self)
        self.setupUi(self)
        self.init_info()
        # self.accepted.connect(lambda :AccInfoWidget())

    def login_waring(self, text):
        QtWidgets.QMessageBox.warning(self,'登录错误',text)

    def init_info(self):
        if os.path.exists('info.plk'):
            try:
                with open('info.plk', 'rb') as f:
                    info = pickle.load(f)
                    self.lineEdit_host.setText(info['host'])
                    self.lineEdit_port.setText(str(info['port']))
                    self.lineEdit_license.setText(info['License'])
                    self.lineEdit_app_id.setText(info['app_id'])
                    self.lineEdit_user_id.setText(info['user_id'])
            except Exception as e:
                print(e)

class QuickOrderWidget(QtWidgets.QWidget, Ui_Form_quick_order):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_quick_order.__init__(self)
        self.setupUi(self)
        self.tableWidget_Price.setColumnWidth(0, 30)
        self.tableWidget_Price.setColumnWidth(3, 30)
        self.tableWidget_Price.setColumnWidth(4, 70)
        self.tableWidget_Price.setColumnWidth(5, 30)
        self.tableWidget_Price.setColumnWidth(8, 30)

        self.init_signal()
        self._price_active = False

    def order(self, BuySell, Price):
        try:
            order_kwargs = {}
            order_kwargs['ProdCode'] = self.lineEdit_ProdCode.text()
            order_kwargs['BuySell'] = BuySell
            order_kwargs['Qty'] = self.spinBox_Qty.value()
            order_kwargs['OrderOption'] = self.checkBox_OrderOptions.checkState()
            order_kwargs['ValidType'] = self.comboBox_VaildType.currentIndex()
            order_kwargs['CondType'] = 0
            order_kwargs['Price'] = Price
        except Exception as e:
            raise e
        add_order(**order_kwargs)

    def init_signal(self):
        self.checkBox_Lock.toggled.connect(lambda x: subscribe_price(self.lineEdit_ProdCode.text(), 1) if x else subscribe_price(self.lineEdit_ProdCode.text(), 0))
        self.pushButton_price_to_middle.released.connect(lambda :self.adjust_ui(20))


    def adjust_ui(self, n):
        last_price = get_price_by_code(self.lineEdit_ProdCode.text()).Last[0]
        Price = range(int(last_price + n), int(last_price - n), -1)
        self.tableWidget_Price.clearContents()
        self.tableWidget_Price.setRowCount(len(Price))
        self.price_location = {}
        a=QIcon(os.path.join('ui', 'addorder.png'))
        for i, p in enumerate(Price):
            self.price_location[p] = i
            self.tableWidget_Price.set_item_sig[int, int, QIcon].emit(i, 0, QIcon(os.path.join('ui', 'deleteorder.png')))
            self.tableWidget_Price.set_item_sig.emit(i, 2, '')
            self.tableWidget_Price.set_item_sig[int, int, QIcon].emit(i, 3, QIcon(os.path.join('ui', 'addorder.png')))
            self.tableWidget_Price.set_item_sig.emit(i, 4, str(p))
            self.tableWidget_Price.set_item_sig[int, int, QIcon].emit(i, 5, QIcon(os.path.join('ui', 'addorder.png')))
            self.tableWidget_Price.set_item_sig.emit(i, 6, '')
            self.tableWidget_Price.set_item_sig[int, int, QIcon].emit(i, 8, QIcon(os.path.join('ui', 'deleteorder.png')))
        self._price_active = True

    def price_table_update(self, price_dict):
        bids_loc = []
        asks_loc = []
        if self._price_active:
            for i in range(5):
                # bid.append((price_dict['Bid'][i], ))
                # ask.append((price_dict['Ask'][i], price_dict['AskQty'][i]))
                # print(self.price_location[price_dict['Bid'][i]], 0, price_dict['BidQty'][i])
                bid_loc = self.price_location.get(price_dict['Bid'][i])
                ask_loc = self.price_location.get(price_dict['Ask'][i])
                if bid_loc:
                    self.tableWidget_Price.update_item_sig.emit(bid_loc, 2, str(price_dict['BidQty'][i]))
                    bids_loc.append(bid_loc)
                if ask_loc:
                    self.tableWidget_Price.update_item_sig.emit(ask_loc, 6, str(price_dict['AskQty'][i]))
                    asks_loc.append(ask_loc)

            bid_empty_loc = set(self.price_location.values()) - set(bids_loc)
            ask_empty_loc = set(self.price_location.values()) - set(asks_loc)
            for n, m in zip(bid_empty_loc, ask_empty_loc):
                self.tableWidget_Price.update_item_sig.emit(n, 2, '')
                self.tableWidget_Price.update_item_sig.emit(m, 6, '')

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

                    # if last1_loc == i:
                    #     self.tableWidget_Price.item(i, 4).setBackground(QColor('#EEEE00'))
                    # else:
                    #     self.tableWidget_Price.item(i, 4).setBackground(QColor('#FFFFFF'))

        # ask_bid = ask.reverse().extend(bid)
        # for i in range(self.tableWidget_Price.rowCount()):
        #     if self.tableWidget_Price.item(i, 1).text() ==

    def price_info_update(self, price_dict):
        bid = price_dict['Bid'][0]
        ask = price_dict['Ask'][0]
        toler = self.spinBox_toler.value()
        self.label_long_info.setText(f'@{bid}->{bid + toler}')
        self.label_short_info.setText(f'@{ask}->{ask - toler}')










if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    od = OrderDialog()
    od.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(app.exec())