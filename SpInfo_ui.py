#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/30 0030 11:40
# @Author  : Hadrianl 
# @File    : Spfunc.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.Qt import QDialog, QDesktopWidget, QTableWidget, QIcon, QColor, QFont, QMessageBox,pyqtSignal, QTableWidgetItem
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui, Qt
import datetime as dt
from ui.order_dialog import Ui_Dialog_order
from ui.acc_info import Ui_Form_acc_info
from ui.sp_login import Ui_Dialog_sp_login
from ui.quick_order_dialog import Ui_Dialog_quick_order
from ui.order_comfirm_dialog import Ui_Dialog_order_comfirm
from ui.close_position_dialog import Ui_Dialog_close_position
from baseitems import QPriceUpdate, QPubOrder, QSubOrder
from ui.order_assistant_widget import Ui_Form_OrderAssistant
from ui.time_widget import Ui_Form_time
from spapi.spAPI import *
from spapi.conf.util import ORDER_VALIDTYPE
import os
import pickle
import datetime as dt
import time
from functools import reduce
from operator import add
# from sp_func.local import addOrder

class OrderDialog(QDialog, Ui_Dialog_order):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog_order.__init__(self)
        self.setupUi(self)
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
        self._price_flag = True
        self._sl_flag = True
        self._sl2_flag = True
        self._oco_sl_flag = True
        # desktop = QDesktopWidget()
        # self.move(desktop.width() - self.width(),(desktop.height() - self.height())/2 - 70)
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
            _stoptype_text = {'L': '损>=' if order_kwargs['BuySell'] == 'B' else '损<=',
                              'U': '升>=',
                              'D': '跌<='}
            if _condtype_index == 0:
                _order_type = (self.checkBox_Auction.checkState() << 1) + self.checkBox_Market.checkState()
                order_kwargs['OrderType'] = {0: 0, 2: 6, 4: 2}[_order_type]
                order_kwargs['Price'] = {0: self.spinBox_Price.value(), 2: 0, 4: 0x7fffffff}[_order_type]
                order_kwargs['ValidType'] = self.comboBox_ValidType.currentIndex()
                cond = ''
                if order_kwargs['ValidType'] == 4:
                    order_kwargs['ValidTime'] = int(dt.datetime.strptime(self.dateEdit_ValidTime.date().toPyDate().strftime('%Y/%m/%d'),
                                                         '%Y/%m/%d').timestamp())
                if self.checkBox_stop_tri.isChecked():
                    order_kwargs['StopType'] = {0: 'L', 1: 'U', 2: 'D', 3: 'L'}[self.comboBox_StopType.currentIndex()]
                    order_kwargs['StopLevel'] = self.spinBox_StopLevel.value()
                    order_kwargs['CondType'] = 1
                    cond = f"{_stoptype_text[order_kwargs['StopType']]} {order_kwargs['StopLevel']}"

                else:
                    order_kwargs['StopLevel'] = 0
            elif _condtype_index == 1:
                order_kwargs['StopType'] = 'L'
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = (self.spinBox_StopLevel2.value() + self.spinBox_toler.value()) if BuySell == 'B' \
                    else (self.spinBox_StopLevel2.value() - self.spinBox_toler.value())
                order_kwargs['StopLevel'] = self.spinBox_StopLevel2.value()
                cond = f"{_stoptype_text[order_kwargs['StopType']]} {order_kwargs['StopLevel']}"
                if self.checkBox_Trailing_Stop.isChecked():
                    order_kwargs['CondType'] = 6

                    if BuySell == 'B':
                        order_kwargs['UpLevel'] = current_price.Ask[0]
                        order_kwargs['UpPrice'] = order_kwargs['StopLevel']
                        order_kwargs['DownLevel'] = self.spinBox_trailing_stop_step.value()
                        cond = cond + f"（追<={order_kwargs['UpLevel'] - order_kwargs['DownLevel']})"
                    else:
                        order_kwargs['DownLevel'] = current_price.Bid[0]
                        order_kwargs['DownPrice'] = order_kwargs['StopLevel']
                        order_kwargs['UpLevel'] = self.spinBox_trailing_stop_step.value()
                        cond = cond + f"（追>={order_kwargs['DownLevel'] + order_kwargs['UpLevel']})"
            elif _condtype_index == 2:
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = self.spinBox_Price.value()
                if BuySell == 'B':
                    order_kwargs['UpLevel'] = self.spinBox_oco_StopLevel.value()
                    order_kwargs['UpPrice'] = self.spinBox_oco_StopLevel.value() + self.spinBox_oco_toler.value()
                    cond = f"双向 损:{order_kwargs['UpPrice']}(>={order_kwargs['UpLevel']})"
                else:
                    order_kwargs['DownLevel'] = self.spinBox_oco_StopLevel.value()
                    order_kwargs['DownPrice'] = self.spinBox_oco_StopLevel.value() - self.spinBox_oco_toler.value()
                    cond = f"双向 损:{order_kwargs['DownPrice']}(<={order_kwargs['DownLevel']})"

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
                    cond = f"牛市 = 赚{_profit} 损{_loss}(+{_loss_toler})"
                else:
                    order_kwargs['DownLevel'] = Price - _profit
                    order_kwargs['DownPrice'] = Price - _profit
                    order_kwargs['UpLevel'] = Price + _loss
                    order_kwargs['UpPrice'] = Price + _loss + _loss_toler
                    cond = f"熊市 = 赚{_profit} 损{_loss}(+{_loss_toler})"

            elif _condtype_index == 4:
                order_kwargs['ValidType'] = 0
                order_kwargs['Price'] = self.spinBox_Price.value()
                _sched_time = self.dateTimeEdit_sched_time.dateTime().toPyDateTime()
                order_kwargs['SchedTime'] = int(_sched_time.timestamp())
                cond = f">={_sched_time}"
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

class AccInfoWidget(QtWidgets.QWidget, Ui_Form_acc_info):
    warning_sig = pyqtSignal(str, str)
    info_sig = pyqtSignal(str, str)
    acc_info_sig = pyqtSignal(float)
    pos_info_sig = pyqtSignal(dict)
    order_info_sig = pyqtSignal(dict)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_acc_info.__init__(self)
        self.setupUi(self)
        desktop = QDesktopWidget()
        self.move(desktop.width() - self.width(), (desktop.height() + self.height()) / 2)
        # self.move(self.parent().width() - self.width(), (self.parent().height() + self.height()) / 2)
        self.setWindowFlags(Qt.Qt.Window)
        self.Order = OrderDialog(self.parent())
        self.QuickOrder = QuickOrderDialog(self.parent())
        self.qprice = QPriceUpdate()
        self.OrderAssistant = OrderAssistantWidget(self)
        self.time = TimeWidget(self)
        self.message = QMessageBox(self)
        self.message.setModal(True)
        self.acc_info = {}
        self.trades_info = []
        self.pos_info = {}
        self.order_info = {}
        self.PL = {}
        self.init_signal()

    def bind_account(self, account_id):
        self.Order.comboBox_account.addItem(account_id)

    def init_signal(self):
        self.qprice.price_update_sig.connect(self.QuickOrder.price_table_update)
        self.qprice.price_update_sig.connect(self.QuickOrder.price_info_update)
        self.qprice.price_update_sig.connect(self.QuickOrder.holding_profit)
        self.qprice.price_update_sig.connect(self.update_pos_info)
        self.pushButton_Order.toggled.connect(self.Order.setVisible)
        self.pushButton_QuickOrder.toggled.connect(self.QuickOrder.setVisible)
        self.Order.lineEdit_ProdCode.textChanged.connect(lambda text: self.QuickOrder.lineEdit_ProdCode.setText(text))
        self.QuickOrder.lineEdit_ProdCode.textChanged.connect(lambda text: self.Order.lineEdit_ProdCode.setText(text))
        self.Order.checkBox_lock.toggled.connect(self.QuickOrder.checkBox_Lock.setChecked)
        self.QuickOrder.checkBox_Lock.toggled.connect(self.Order.checkBox_lock.setChecked)
        self.warning_sig.connect(lambda title, text: self.message.warning(self.parent(), title, text))
        self.info_sig.connect(lambda title, text: self.message.information(self.parent(), title, text))
        # self.pushButton_test.released.connect(lambda :print(get_product_by_code('HSIK8')))
        self.acc_info_sig.connect(self.update_acc_info)
        self.pushButton_OrderAssistant.toggled.connect(self.OrderAssistant.setVisible)
        self.pos_info_sig.connect(self.OrderAssistant.calc_amount_base)
        # self.OrderAssistant.pushButton_calc_tp_sl.released.connect(lambda :self.OrderAssistant.calc_amount_base(self.pos_info))
        self.OrderAssistant.oco_close_sig.connect(self.Order.oco_close)

    def update_pos_info(self, price_dict):
        for t in range(self.tableWidget_pos.rowCount()):
            prodcode = price_dict['ProdCode'].decode()
            if  prodcode == self.tableWidget_pos.item(t, 0).text():
                # AccInfo.tableWidget_pos.update_item_sig.emit(t, 8, str(price_dict['Last'][0]))
                pos = self.pos_info[price_dict['ProdCode'].decode()]
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

    def update_trade_info(self, trade_dict):
        self.trades_info.append(trade_dict)

    def update_acc_info(self, PL):
        ccy = self.acc_info['BaseCcy'].decode()
        BuyingPower = self.acc_info['CashBal'] + self.acc_info['CreditLimit'] + PL - self.acc_info['IMargin']
        NAV = self.acc_info['CashBal'] + PL
        MarginCall = self.acc_info['IMargin'] - (self.acc_info['CashBal'] + self.acc_info['CreditLimit'] + PL) if (self.acc_info['CashBal'] + self.acc_info['CreditLimit'] + PL) < self.acc_info['IMargin'] else 0
        CommodityPL = PL
        try:
            MarginLevel = (self.acc_info['CashBal'] + self.acc_info['CreditLimit'] + PL) / \
                          self.acc_info['IMargin']
            ML = f'{MarginLevel:.2%}'
        except ZeroDivisionError:
            ML = '-'

        self.tableWidget_acc_info.setItem(0, 0, QTableWidgetItem(f"{BuyingPower:,} {ccy}"))
        self.tableWidget_acc_info.setItem(1, 0, QTableWidgetItem(f"{NAV:,} {ccy}"))
        self.tableWidget_acc_info.setItem(2, 0, QTableWidgetItem(f"{MarginCall:,} {ccy}"))
        self.tableWidget_acc_info.setItem(3, 0, QTableWidgetItem(f"{CommodityPL:,.2f} {ccy}"))
        self.tableWidget_acc_info.setItem(6, 0, QTableWidgetItem(ML))
        # self.tableWidget_acc_info.setItem(0, 0, f"{BuyingPower:,} {ccy}")

    #
    # def create_cond_text(self, **kwargs):
    #     _stoptype_text = {'L': '损>=' if kwargs['BuySell'] == 'B' else '损<=',
    #                       'U': '升>=',
    #                       'D': '跌<='}

        # condtype = kwargs['CondType']
        #
        # if condtype == 0:
        #     ...
        # elif condtype==


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

class ClosePositionDialog(QtWidgets.QDialog, Ui_Dialog_close_position):
    def __init__(self, BuySell, ProdCode, Qty, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Dialog_close_position.__init__(self)
        self.setupUi(self)
        self.pushButton_Long.setVisible(BuySell == 'B')
        self.pushButton_Short.setVisible(BuySell == 'S')
        self.lineEdit_ProdCode.setText(ProdCode)
        self.spinBox_Qty.setValue(Qty)
        self.init_signal()
        self.show()
        self.sub_prodcode(ProdCode)

    def init_signal(self):
        self.pushButton_Long.released.connect(lambda :self.close_position('B'))
        self.pushButton_Short.released.connect(lambda :self.close_position('S'))


    def sub_prodcode(self, prodcode):
        if subscribe_price(prodcode, 1) != 0:
            mb = QMessageBox()
            mb.warning(self, f'WARING-订阅', f'订阅{prodcode}数据失败')
            mb.accepted.connect(self.close)
        else:
            QMessageBox.information(self, f'INFO-订阅成功', f'订阅{prodcode}数据成功')


    def close_position(self, BuySell):
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




class QuickOrderDialog(QtWidgets.QDialog, Ui_Dialog_quick_order):
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
            cond = ''
        except Exception as e:
            raise e
        else:
            comfirm_order = ComfirmDialog(self, Cond=cond, **order_kwargs)
            comfirm_order.show()
            comfirm_order.accepted.connect(lambda : add_order(**order_kwargs))

    def close_all_position(self):
        try:
            prodcode = self.lineEdit_ProdCode.text()
            pos = get_pos_by_product(prodcode)
            net_pos = (pos.Qty + pos.LongQty - pos.ShortQty) if pos.LongShort ==b'B' else (-pos.Qty + pos.LongQty - pos.ShortQty)
            if net_pos > 0:
                ClosePositionDialog('S', prodcode, net_pos, parent=self)
            elif net_pos < 0:
                ClosePositionDialog('B', prodcode, -net_pos, parent=self)
            else:
                QMessageBox.warning(self, 'WARNING-平仓', f'{prodcode}没有仓位')
        except Exception as e:
            QMessageBox.warning(self, 'ERROR-平仓', f'{e}或{prodcode}没有仓位')


    def init_signal(self):
        # self.checkBox_Lock.toggled.connect(lambda x: subscribe_price(self.lineEdit_ProdCode.text(), 1) if x else subscribe_price(self.lineEdit_ProdCode.text(), 0))
        self.pushButton_price_to_middle.released.connect(lambda :self.adjust_ui(25))
        self.tableWidget_Price.itemDoubleClicked.connect(lambda i: self.doubleclick_order(i.row(), i.column()))
        self.pushButton_long.released.connect(lambda :self.addition_toler_order('B'))
        self.pushButton_short.released.connect(lambda: self.addition_toler_order('S'))
        self.checkBox_Lock.toggled.connect(lambda b: [subscribe_price(self.lineEdit_ProdCode.text(), 1),time.sleep(0.5), self.adjust_ui(25)] if b else ...)
        self.pushButton_close_position.released.connect(self.close_all_position)



    def adjust_ui(self, n):
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
            # print(m)
            self.tableWidget_Price.verticalScrollBar().setValue(m)
            # self.tableWidget_Price.selectRow(self.tableWidget_Price.currentRow()-3)
            # self.tableWidget_Price.verticalScrollBar().


    def working_order_update(self):
        orders = get_orders_by_array()
        bid_qty_loc = []
        ask_qty_loc =[]
        for order in [o for o in orders if (o.ProdCode.decode('GBK') == self.lineEdit_ProdCode.text())&(o.Status in [1, 3, 8])]:
            price_loc = self.price_location.get(order.Price)
            print(price_loc)
            print(order.Qty)
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

    def price_table_update(self, price_dict):
        bids_loc = []
        asks_loc = []
        if self._price_active&(price_dict['ProdCode'].decode('GBK') == self.lineEdit_ProdCode.text()):
            for i in range(5):
                # bid.append((price_dict['Bid'][i], ))
                # ask.append((price_dict['Ask'][i], price_dict['AskQty'][i]))
                # print(self.price_location[price_dict['Bid'][i]], 0, price_dict['BidQty'][i])
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

    def price_info_update(self, price_dict):
        bid = price_dict['Bid'][0]
        ask = price_dict['Ask'][0]
        toler = self.spinBox_toler.value()
        self.label_long_info.setText(f'@{bid}->{bid + toler}')
        self.label_short_info.setText(f'@{ask}->{ask - toler}')

    def position_takeprofit_info_update(self, trades_info):
        # trades = get_all_trades_by_array()
        prodcode = self.lineEdit_ProdCode.text()
        current_trades = [trade for trade in trades_info if trade['ProdCode'].decode('GBK') == prodcode]
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
            print(self.trade_long_queue)
            print(self.trade_short_queue)
            long_pos_num = len(self.trade_long_queue)
            short_pos_num = len(self.trade_short_queue)

            print(f'{pre_pos}@{pre_pos_price}')
            print(long_pos_num, short_pos_num)
            holding_pos_num = long_pos_num - short_pos_num

            if  long_pos_num == short_pos_num:
                self.holding_pos = (0, 0)
            elif long_pos_num > short_pos_num:
                self.holding_pos = (holding_pos_num, sum(self.trade_long_queue[-1:-(holding_pos_num + 1):-1]) / holding_pos_num)
            else:
                self.holding_pos = (holding_pos_num, sum(self.trade_short_queue[-1:-(-holding_pos_num + 1):-1]) / -holding_pos_num)

            self.label_closed_profit.setText(f'{close_pos_takeprofit * leverage:,.2f}')

            self.label_pos.setText(f'{self.holding_pos[0]}@{self.holding_pos[1]:,.2f}')

    def holding_profit(self, price_dict):
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

    def doubleclick_order(self, row, column):
        price = float(self.tableWidget_Price.item(row, 4).text())
        if column == 3:
            buysell = 'B'
            self.order(buysell, price)
        elif column == 5:
            buysell = 'S'
            self.order(buysell, price)

    def addition_toler_order(self, buysell):
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


class OrderAssistantWidget(QtWidgets.QWidget, Ui_Form_OrderAssistant):
    oco_close_sig = pyqtSignal(str, int, float, float)
    close_position_trigger_sig = pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_OrderAssistant.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.Window)
        self.holding_qty = 0
        self.holding_pos_amt = 0
        self.trailing_best_price = None
        self.last_price = {}
        self.init_signal()

    def init_signal(self):
        self.spinBox_takeprofit_amount.editingFinished.connect(lambda :self.calc_amount_base(self.parent().pos_info))
        self.spinBox_stoploss_amount.editingFinished.connect(lambda: self.calc_amount_base(self.parent().pos_info))
        self.pushButton_OCO_close_position.released.connect(self.oco_close_position)
        self.lineEdit_ProdCode.editingFinished.connect(lambda :self.update_holding_pos(self.parent().pos_info))
        self.parent().pos_info_sig.connect(self.update_holding_pos)
        self.checkBox_trailing_stop.toggled.connect(lambda b: self.parent().qprice.price_update_sig.connect(self.update_trailing_stop) if b else self.parent().qprice.price_update_sig.disconnect(self.update_trailing_stop))
        self.parent().qprice.price_update_sig.connect(lambda p: self.lineEdit_price.setText(str(p['Last'][0])) if p['ProdCode'].decode() == self.lineEdit_ProdCode.text() else ...)
        self.parent().qprice.price_update_sig.connect(lambda p: setattr(self, 'last_price', p) if p['ProdCode'].decode() == self.lineEdit_ProdCode.text() else ...)
        self.parent().order_info_sig.connect(lambda o: self.checkBox_auto_tp.setChecked(True) if o['ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 1 and o['Ref'].decode() =='auto_tp' else ...)
        self.parent().order_info_sig.connect(lambda o: self.checkBox_auto_tp.setChecked(False) if o[ 'ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 10 and o['Ref'].decode() == 'auto_tp' else ...)
        self.checkBox_auto_tp.released.connect(lambda : self.init_auto_takeprofit() if not self.checkBox_auto_tp.isChecked() else self.deinit_auto_takeprofit())
        self.parent().order_info_sig.connect(lambda o: self.checkBox_auto_sl.setChecked(True) if o['ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 1 and o['Ref'].decode() =='auto_sl' else ...)
        self.parent().order_info_sig.connect(lambda o: self.checkBox_auto_sl.setChecked(False) if o[ 'ProdCode'].decode() == self.lineEdit_ProdCode.text() and o['Status'] == 10 and o['Ref'].decode() == 'auto_sl' else ...)
        self.checkBox_auto_sl.released.connect(lambda : self.init_auto_stoploss() if not self.checkBox_auto_sl.isChecked() else self.deinit_auto_stoploss())
        self.lineEdit_ProdCode.editingFinished.connect(lambda :self.init_auto_tp_sl())


    def init_auto_tp_sl(self):
        try:
            orders = get_orders_by_array()
            self.checkBox_auto_tp.setChecked(True)
            self.checkBox_auto_sl.setChecked(False)
            for o in orders:
                if o.Status in [1, 3] and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    if o.Ref.decode() == 'auto_tp':
                        self.checkBox_auto_tp.setChecked(True)
                    elif o.Ref.decode() =='auto_sl':
                        self.checkBox_auto_sl.setChecked(True)
        except Exception as e:
            print(e)


    def init_auto_takeprofit(self):
        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-自动止盈', '请检查合约代码')
            return
        price = self.spinBox_tp_price.value()
        if self.holding_qty > 0:
            if price <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止盈', '止盈价需高于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=int(self.holding_qty), ValidType=0, CondType=0, OrderType=0, Price=price,
                          Ref='auto_tp')
        elif self.holding_qty < 0:
            if price >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止盈', '止盈价需低于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=int(-self.holding_qty), ValidType=0, CondType=0, OrderType=0, Price=price,
                          Ref='auto_tp')

    def deinit_auto_takeprofit(self):
        try:
            orders = get_orders_by_array()
            for o in orders:
                if o.Ref.decode() == 'auto_tp' and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    delete_order_by(o.IntOrderNo, self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)

    def init_auto_stoploss(self):
        if self.lineEdit_ProdCode.text() != self.last_price.get('ProdCode', b'').decode():
            QMessageBox.critical(self, 'CRITICAL-自动止损', '请检查合约代码')
            return
        price = self.spinBox_sl_price.value()
        if self.holding_qty > 0:
            if price >= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止损', '止损价需低于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='S', OrderOptions=0,
                          Qty=int(self.holding_qty), ValidType=0, CondType=1, OrderType=0, Price=price,
                          StopType='L', StopLevel=price - self.spinBox_stoploss_toler.value(),
                          Ref='auto_sl')
        elif self.holding_qty < 0:
            if price <= self.last_price['Last'][0]:
                QMessageBox.warning(self, 'WARING-自动止损', '止损价需高于现价')
            else:
                add_order(ProdCode=self.lineEdit_ProdCode.text(), BuySell='B', OrderOptions=0,
                          Qty=int(-self.holding_qty), ValidType=0, CondType=1, OrderType=0, Price=price,
                          StopType='L', StopLevel=price + self.spinBox_stoploss_toler.value(),
                          Ref='auto_sl')

    def deinit_auto_stoploss(self):
        try:
            orders = get_orders_by_array()
            for o in orders:
                if o.Ref.decode() == 'auto_sl' and o.ProdCode.decode() == self.lineEdit_ProdCode.text():
                    delete_order_by(o.IntOrderNo, self.lineEdit_ProdCode.text())
        except Exception as e:
            print(e)

    def update_holding_pos(self, pos_info):
        pos = pos_info.get(self.lineEdit_ProdCode.text())
        if pos is not None:
            qty = pos['Qty'] if pos['LongShort'] == b'B' else -pos['Qty']
            amt = pos['TotalAmt'] if pos['LongShort'] == b'B' else -pos['TotalAmt']
            today_net_pos = pos['LongQty'] - pos['ShortQty']
            today_net_pos_amt = pos['LongTotalAmt'] - pos['ShortTotalAmt']
            self.holding_pos_amt = amt + today_net_pos_amt
            self.holding_qty = qty + today_net_pos
            holding_price = self.holding_pos_amt / self.holding_qty if self.holding_qty != 0 else self.holding_pos_amt
            self.lineEdit_holding_qty.setText(str(self.holding_qty))
            self.lineEdit_holding_price.setText(str(holding_price))
        else:
            self.lineEdit_holding_qty.setText('-')
            self.lineEdit_holding_price.setText('-')

    def update_trailing_stop(self, price):
        toler = self.spinBox_trailing_toler.value()
        if price['ProdCode'].decode() != self.lineEdit_ProdCode.text():
            return

        if self.holding_qty > 0:
            self.trailing_best_price = max(self.trailing_best_price, price['Last'][0]) if self.trailing_best_price != None else price['Last'][0]
            self.trailing_close_price = self.trailing_best_price - toler
            print(self.trailing_best_price, self.trailing_close_price)
            if self.trailing_close_price >= price['Last'][0]:
                self.close_position_trigger_sig.emit()
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
            print(self.trailing_best_price, self.trailing_close_price)
            self.horizontalSlider_toler.setValue(int(price['Last'][0]))
            if self.trailing_close_price <= price['Last'][0]:
                self.close_position_trigger_sig.emit()
                self.checkBox_trailing_stop.setChecked(False)
                self.trailing_best_price = None
                self.lineEdit_best_price.setText('-')
                self.lineEdit_sl_close_price.setText('-')
            else:
                self.lineEdit_best_price.setText(str(self.trailing_best_price))
                self.lineEdit_sl_close_price.setText(str(self.trailing_close_price))
                self.horizontalSlider_toler.setMaximum(int(self.trailing_best_price))
                self.horizontalSlider_toler.setMinimum(int(self.trailing_close_price))

    def calc_amount_base(self, pos_info):
        prodcode = self.lineEdit_ProdCode.text()
        p = pos_info.get(prodcode)
        if p:
            net_amt = p['TotalAmt'] + p['LongTotalAmt'] - p['ShortTotalAmt'] if p['LongShort'] == b'B' else -p['TotalAmt'] + p['LongTotalAmt'] - p['ShortTotalAmt']
            self.net_qty = p['Qty'] + p['LongQty'] - p['ShortQty'] if p['LongShort'] == b'B'else -p['Qty'] + p['LongQty'] - p['ShortQty']
            self.tp = (net_amt + self.spinBox_takeprofit_amount.value() / p['leverage']) / self.net_qty if self.net_qty != 0 else 0
            self.sl = (net_amt + self.spinBox_stoploss_amount.value() / p['leverage']) / self.net_qty if self.net_qty != 0 else 0
            self.lineEdit_takeprofit_price.setText(f'{self.net_qty}@{self.tp:.2f}')
            self.lineEdit_stoploss_price.setText(f'{self.net_qty}@{self.sl:.2f}')
        else:
            # QMessageBox.warning(self, 'WARING-计算', f'合约{prodcode}未有任何持仓')
            ...

    def oco_close_position(self):
        prodcode = self.lineEdit_ProdCode.text()
        net_qty = getattr(self, 'net_qty', 0)
        tp = getattr(self, 'tp', 0)
        sl = getattr(self, 'sl', 0)
        if net_qty != 0:
            self.oco_close_sig.emit(prodcode, net_qty, tp, sl)
        else:
            QMessageBox.warning(self, 'WARING-双向限价平仓', f'合约{prodcode}未有任何持仓，无法下平仓指令')




class ComfirmDialog(QtWidgets.QDialog, Ui_Dialog_order_comfirm):
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
    init_api_sig = pyqtSignal()
    info_sig = pyqtSignal(str, str, int)
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, parent, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.init_signal()
        # self.init_order_follower()
        # self.setWindowTitle('Sharp Point Order System --- Carry Investment')

    def init_signal(self):
        self.info_sig.connect(self.popup)

    def popup(self,title, context, e_time=0):
        mb = QMessageBox(self)
        mb.move(self.width() - mb.width() - 100, 0)
        mb.setWindowTitle(title)
        mb.setText(context)
        mb.show()
        if e_time != 0:
            self.timer.singleShot(5000, mb.close)


    def init_order_follower(self):
        self.order_pub = QPubOrder(self)
        self.order_sub = QSubOrder(self.order_pub.order_queue, self)
        self.order_pub.finished.connect(lambda :self.popup('<INFO-跟单>', '交易发布已停止', 8000))
        self.order_sub.finished.connect(lambda: self.popup('<INFO-跟单>', '交易订阅已停止', 5000))
        self.order_pub.start()
        self.order_sub.start()

    def deinit_order_follower(self):
        self.order_pub.close()
        self.order_sub.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '退出', "是否要退出SP下单？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            a0.accept()
            logout()
            unintialize()
            pid = os.getpid()
            os.system(f'taskkill /F /PID {pid}')
        else:
            a0.ignore()

class TimeWidget(QtWidgets.QWidget, Ui_Form_time):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Form_time.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.Window | Qt.Qt.FramelessWindowHint)
        self.timer = QtCore.QTimer(self)
        self.init_signal()
        self.move((QDesktopWidget().width() -self.width()) / 2, 30)


    def init_signal(self):
        self.timer.timeout.connect(self.update_sys_time)
        self.timer.start(1000)
        self.parent().qprice.price_update_sig.connect(lambda p:self.update_data_time(p['Timestamp']))
        self.parent().parent().login_sig.connect(self.show)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    od = OrderDialog()
    od.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(app.exec())