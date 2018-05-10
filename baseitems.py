#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 0023 19:04
# @Author  : Hadrianl 
# @File    : baseitems.py
# @License : (C) Copyright 2013-2017, 凯瑞投资


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.Qt import QObject, QIcon
from PyQt5.QtCore import pyqtSignal, QThread
import pymysql as pm
import datetime as dt
from queue import Queue, Empty
import time
from utils import MT4_ORDER_TYPE, FOLLOWER_STRATEGY
from spapi.spAPI import add_order


class QInfoWidget(QTableWidget):
    set_item_sig = pyqtSignal([int, int, str], [int, int, QIcon])
    update_item_sig = pyqtSignal(int, int, str)
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.set_item_sig[int, int, str].connect(lambda x, y, s: self.setItem(x, y, QTableWidgetItem(s)))
        self.set_item_sig[int, int, QIcon].connect(lambda x, y, icon: self.setItem(x, y, QTableWidgetItem(icon, '')))
        self.update_item_sig.connect(lambda x,y,s: self.item(x, y).setText(s))

class QPriceUpdate(QObject):
    price_update_sig = pyqtSignal(dict)
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

class QPubOrder(QThread):
    def __init__(self, parent=None, dbconfig=None):
        QThread.__init__(self, parent)
        self.order_queue = Queue()
        if dbconfig == None:
            try:
                dbconfig = {'host': '192.168.2.226',
                            'port': 3306,
                            'user': 'kairuitouzi',
                            'password': 'kairuitouzi',
                            'db': 'carry_investment',
                            'cursorclass': pm.cursors.DictCursor,
                            }
                self.conn = pm.connect(**dbconfig)
            except Exception:
                ...
            else:
                try:
                    with self.conn.cursor() as cursor:
                        sql = 'select MAX(OpenTime) as init_time from order_detail'
                        cursor.execute(sql)
                        self.last_time = cursor.fetchone()['init_time']
                        self.conn.commit()
                        self._active = True
                except Exception as e:
                    self.last_time = dt.datetime.now()
        print(self.last_time)

    def run(self):
        self.parent().info_sig.emit('INFO-跟单', '开始发布交易', 8000)
        orders_dict = {}
        while self._active:
            with self.conn.cursor() as cursor:
                try:
                    sql = f'select * from order_detail where OpenTime>"{self.last_time}"'
                    cursor.execute(sql)
                    new_orders = cursor.fetchall()
                    if new_orders:
                        self.last_time = max([d.get('OpenTime') for d in new_orders])
                        for d in new_orders:
                            orders_dict.update({d.get('Ticket'): d})
                            self.send_changed_order(d)

                    remaining_orders = [str(t) for t, v in orders_dict.items() if
                                        v.get('Status') == 1 or v.get('Status') == 0]
                    if remaining_orders:
                        sql = f'select * from order_detail where Ticket in ({",".join(remaining_orders)}) and CloseTime>"1970-01-01 00:00:00"'
                        cursor.execute(sql)
                        closed_orders = cursor.fetchall()
                        if closed_orders:
                            for d in closed_orders:
                                orders_dict.update({d.get('Ticket'): d})
                                self.send_changed_order(d)
                except Exception as e:
                    print('发布',e)
                finally:
                    self.conn.commit()
                    time.sleep(0.5)

    def close(self):
        self._active = False

    def send_changed_order(self, d:dict):
        if d.get('Status') == 1:
            log_info = f'账户:{d.get("Account_ID")}--于{d.get("OpenTime")}开仓--[{MT4_ORDER_TYPE.get(d.get("Type"))}-{d.get("Symbol")}@{d.get("OpenPrice")}]-#{d.get("Ticket")}'
        elif d.get('Status') == 0:
            log_info = f'账户:{d.get("Account_ID")}--于{d.get("OpenTime")}挂单--[{MT4_ORDER_TYPE.get(d.get("Type"))}-{d.get("Symbol")}@{d.get("OpenPrice")}]-#{d.get("Ticket")}'
        elif d.get('Status') == -1:
            log_info = f'账户:{d.get("Account_ID")}--于{d.get("OpenTime")}取消挂单--[{MT4_ORDER_TYPE.get(d.get("Type"))}-{d.get("Symbol")}@{d.get("OpenPrice")}]-#{d.get("Ticket")}'
        elif d.get('Status') == 2:
            tp = d.get('Comment').find('[tp]') != -1
            sl = d.get('Comment').find('[sl]') != -1
            has_comment = bool(d.get('Comment'))
            close_type = {0: '平仓', 1: d.get('Comment'), 2: '止损', 3: '止盈', 4: d.get('Comment')}.get(((tp << 1) + sl + 1) * has_comment)
            log_info = f'账户:{d.get("Account_ID")}--于{d.get("CloseTime")}{close_type}--[{MT4_ORDER_TYPE.get(d.get("Type"))}-{d.get("Symbol")}@{d.get("ClosePrice")}]-#{d.get("Ticket")}'
        else:
            log_info = f'Status:{d.get("Status")}'
        print(log_info)
        self.order_queue.put(d)

class QSubOrder(QThread):
    def __init__(self, order_queue:Queue, parent=None):
        QThread.__init__(self, parent)
        self.order_queue = order_queue
        self.orders_dict = {}
        self._active = True
        self.ProdCode = 'MHIK8'
        self.__follower_strategy = FOLLOWER_STRATEGY
        self.strategy_type = {0:{'B': 'B', 'S': 'S'}, 1:{'B': 'S', 'S': 'B'}}

    @property
    def follower_strategy(self):
        return self.__follower_strategy

    def register_follower(self, account_id, type):
        self.__follow_strategy[account_id] = type

    def unregister_follower(self, account_id):
        try:
            self.__follower_strategy.pop(account_id)
        except KeyError:...

    def run(self):
        self.parent().info_sig.emit('INFO-跟单', '开始订阅交易', 5000)
        while self._active:
            try:
                new_order = self.order_queue.get(timeout=3)
                self.orders_dict.update({new_order.get('Ticket'): new_order})
                if new_order.get('Status') == 1:
                    log_info = f'账户:{new_order.get("Account_ID")}--于{new_order.get("OpenTime")}开仓--[{MT4_ORDER_TYPE.get(new_order.get("Type"))}-{new_order.get("Symbol")}@{new_order.get("OpenPrice")}]-#{new_order.get("Ticket")}'
                elif new_order.get('Status') == 0:
                    log_info = f'账户:{new_order.get("Account_ID")}--于{new_order.get("OpenTime")}挂单--[{MT4_ORDER_TYPE.get(new_order.get("Type"))}-{new_order.get("Symbol")}@{new_order.get("OpenPrice")}]-#{new_order.get("Ticket")}'
                elif new_order.get('Status') == -1:
                    log_info = f'账户:{new_order.get("Account_ID")}--于{new_order.get("OpenTime")}取消挂单--[{MT4_ORDER_TYPE.get(new_order.get("Type"))}-{new_order.get("Symbol")}@{new_order.get("OpenPrice")}]-#{new_order.get("Ticket")}'
                elif new_order.get('Status') == 2:
                    tp = new_order.get('Comment').find('[tp]') != -1
                    sl = new_order.get('Comment').find('[sl]') != -1
                    has_comment = bool(new_order.get('Comment'))
                    close_type = {0: '平仓', 1: new_order.get('Comment'), 2: '止损', 3: '止盈',
                                  4: new_order.get('Comment')}.get(((tp << 1) + sl + 1) * has_comment)
                    log_info = f'账户:{new_order.get("Account_ID")}--于{new_order.get("CloseTime")}{close_type}--[{MT4_ORDER_TYPE.get(new_order.get("Type"))}-{new_order.get("Symbol")}@{new_order.get("ClosePrice")}]-#{new_order.get("Ticket")}'
                else:
                    log_info = f'Status:{new_order.get("Status")}'
                self.follow_order(new_order)
            except Empty:
                ...
            except Exception as e:
                print('订阅Exception',e)

    def close(self):
        self._active = False

    def follow_order(self,order:dict):
        print(order)
        if 'HSENG' not in order.get('Symbol','') or order['Account_ID'] not in self.follower_strategy:
        # if 'HSENG' not in order.get('Symbol', ''):
            return
        try:
            bs = self.strategy_type[self.follower_strategy[order['Account_ID']]]
            # bs = {'B': 'B', 'S': 'S'}
            if order['Status'] == 1 and order['Type'] < 6:
                Price = order['OpenPrice']
                Qty = int(order['Lots'])
                if order['Type'] == 0:
                    add_order(BuySell=bs['B'], ProdCode=self.ProdCode, Qty=Qty, Ref=f"OL-#{order['Ticket']}", OrderOptions=0, CondType=0, OrderType=6, Price=0)
                elif order['Type'] == 1:
                    add_order(BuySell=bs['S'], ProdCode=self.ProdCode, Qty=Qty, Ref=f"OS-#{order['Ticket']}", OrderOptions=0, CondType=0, OrderType=6, Price=0)
            elif order['Status'] == 2 and order['Type'] < 6:
                Price = order['OpenPrice']
                Qty = int(order['Lots'])
                if order['Type'] == 0:
                    add_order(BuySell=bs['S'], ProdCode=self.ProdCode, Qty=Qty, Ref=f"OL-#{order['Ticket']}", OrderOptions=0,
                              CondType=0, OrderType=6, Price=0)
                elif order['Type'] == 1:
                    add_order(BuySell=bs['B'], ProdCode=self.ProdCode, Qty=Qty, Ref=f"OS-#{order['Ticket']}", OrderOptions=0,
                              CondType=0, OrderType=6, Price=0)
        except Exception as e:
            self.parent().info_sig.emit('WARING-跟单错误', str(e), 0)






# class QHandler(QThread):
#     def __init__(self, parent=None, queue=None):
#         QThread.__init__(self, parent)
#         self.handle_queue = queue
#
#
#     def run(self):
#         while True:
#             handler, arg, kwargs = self.handle_queue.get()
#             try:
#                 handler(*arg, **kwargs)
#             except Exception as e:
#                 print(e)