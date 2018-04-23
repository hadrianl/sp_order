#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 0018 15:45
# @Author  : Hadrianl 
# @File    : app.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from SpInfo_ui import SpLoginDialog, OrderDialog, AccInfoWidget
import sys
from spapi.spAPI import *
import datetime as dt
from spapi.conf.util import ORDER_STATUS
import pickle
from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSignal


local_login = False
def addOrder(**kwargs):
    if local_login:
        add_order(**kwargs)
    else:
        print(2, kwargs)

def info_handle(type, info, info_struct=None, handle_type=0):
    if handle_type == 0:
        print('*LOCAL*' + type + info)
    elif handle_type == 1:
        print('*LOCAL*' + type + info)
    try:
        is_struct = map(lambda x: isinstance(info_struct, x),
                     [SPApiOrder, SPApiPos, SPApiTrade, SPApiAccBal, SPApiAccInfo])
        update_func = [_update_order, _update_postion, _update_trade, _update_accbals, _update_acc_info]
        for b, f in zip(is_struct, update_func):
            if b:
                f(info_struct)
    except Exception as e:
        print(e)

def update_acc_info():
    try:
        acc_info = get_acc_info()
        _update_acc_info(acc_info)
    except Exception as e:
        print(e)
        raise e

def _update_acc_info(acc_info):
    acc_info_dict = {}
    for name, c_type in acc_info._fields_:
        acc_info_dict[name] = getattr(acc_info, name)

    global base_ccy
    base_ccy = acc_info_dict['BaseCcy'].decode()
    AccInfo.tableWidget_acc_info.set_item_sig.emit(0, 0, f"{acc_info_dict['BuyingPower']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(1, 0, f"{acc_info_dict['NAV']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(2, 0, f"{acc_info_dict['MarginCall']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(3, 0, f"{acc_info_dict['CommodityPL']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(4, 0, f"{acc_info_dict['IMargin']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(5, 0, f"{acc_info_dict['MMargin']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(6, 0, '')
    AccInfo.tableWidget_acc_info.set_item_sig.emit(7, 0, f"{acc_info_dict['MaxMargin']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(8, 0, acc_info_dict['MarginPeriod'].decode())
    AccInfo.tableWidget_acc_info.set_item_sig.emit(9, 0, f"{acc_info_dict['CashBal']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(10, 0, f"{acc_info_dict['CreditLimit']:,} {base_ccy}")
    AccInfo.tableWidget_acc_info.set_item_sig.emit(11, 0, acc_info_dict['CtrlLevel'].decode())
    AccInfo.tableWidget_acc_info.set_item_sig.emit(12, 0, acc_info_dict['MarginClass'].decode())
    AccInfo.tableWidget_acc_info.set_item_sig.emit(13, 0, acc_info_dict['AEId'].decode())
    print('acc_info:', acc_info_dict)
    return acc_info_dict


def update_orders():
    try:
        orders_array = get_orders_by_array()
        print(orders_array)
        orders = []
        for i in range(AccInfo.tableWidget_orders.rowCount()):
            AccInfo.tableWidget_orders.removeRow(0)

        for o in orders_array:
            orders.append(_update_order(o))

    except Exception as e:
        print('order_Error:',e)
        raise e
def _update_order(o):
    order_dict = {}
    for name, c_type in o._fields_:
        order_dict[name] = getattr(o, name)
    r = 0
    for i in range(AccInfo.tableWidget_orders.rowCount()):
        if order_dict['IntOrderNo'] == int(AccInfo.tableWidget_orders.item(i, 0).text()):
            r = i
            break
    else:
        AccInfo.tableWidget_orders.insertRow(0)

    AccInfo.tableWidget_orders.set_item_sig.emit(r, 0, str(order_dict['IntOrderNo']))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 1, order_dict['ProdCode'].decode())
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 2, '')
    if order_dict['BuySell'].decode() == 'B':
        AccInfo.tableWidget_orders.set_item_sig.emit(r, 3, str(order_dict['Qty']))
    else:
        AccInfo.tableWidget_orders.set_item_sig.emit(r, 4, str(order_dict['Qty']))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 5, f"{order_dict['Price']:,}")
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 6, str(dt.datetime.fromtimestamp(order_dict['ValidTime'])))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 7, '')
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 8, ORDER_STATUS[order_dict['Status']])
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 9, str(order_dict['TradedQty']))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 10, str(order_dict['Initiator'].decode()))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 11, order_dict['Ref'].decode('GBK'))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 12, str(dt.datetime.fromtimestamp(order_dict['TimeStamp'])))
    AccInfo.tableWidget_orders.set_item_sig.emit(r, 13, str(order_dict['ExtOrderNo']))
    print('order:', order_dict)
    return order_dict


def update_positions():
    try:
        pos_array = get_all_pos_by_array()
        pos = []
        for i in range(AccInfo.tableWidget_pos.rowCount()):
            AccInfo.tableWidget_pos.removeRow(0)
        for p in pos_array:
            pos.append(_update_postion(p))
    except Exception as e:
        print('pos_Error:',e)
        raise e

def _update_postion(p):
    pos_dict = {}
    for name, c_type in p._fields_:
        pos_dict[name] = getattr(p, name)

    r = 0
    for i in range(AccInfo.tableWidget_pos.rowCount()):
        if pos_dict['ProdCode'].decode() == AccInfo.tableWidget_pos.item(i, 0).text():
            r = i
            break
    else:
        AccInfo.tableWidget_pos.insertRow(0)

    AccInfo.tableWidget_pos.set_item_sig.emit(r, 0, pos_dict['ProdCode'].decode())
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 1, '')
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 2, str(pos_dict['Qty']))
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 3, str(pos_dict['DepQty']))
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 4, f"{pos_dict['LongQty']}@{(pos_dict['LongTotalAmt']/pos_dict['LongQty']):,.2f}")
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 5, f"{-pos_dict['ShortQty']}@{(pos_dict['ShortTotalAmt']/pos_dict['ShortQty']):,.2f}")
    net_pos = pos_dict['LongQty'] - pos_dict['ShortQty']
    net_pos_amt = pos_dict['LongTotalAmt'] - pos_dict['ShortTotalAmt']
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 6, str(net_pos))
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 7, f"{net_pos}@{net_pos_amt/(1 if net_pos==0 else net_pos):,.2f}")
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 8, '')
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 9, f"{pos_dict['PL']:,}")
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 10, )
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 11, f"{pos_dict['ExchangeRate']:,}")
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 12, f"{pos_dict['PLBaseCcy']:,}")
    AccInfo.tableWidget_pos.set_item_sig.emit(r, 13, )
    print('pos:', pos_dict)
    return pos_dict


def update_trades():
    try:
        trades_array = get_all_trades_by_array()
        trades = []
        for i in range(AccInfo.tableWidget_trades.rowCount()):
            AccInfo.tableWidget_trades.removeRow(0)

        for t in trades_array:
            trades.append(_update_trade(t))

    except Exception as e:
        print('trade_Error:',e)
        raise e

def _update_trade(t):
    trade_dict = {}
    for name, c_type in t._fields_:
        trade_dict[name] = getattr(t, name)

    r = 0
    for i in range(AccInfo.tableWidget_trades.rowCount()):
        if trade_dict['IntOrderNo'] == int(AccInfo.tableWidget_trades.item(i, 11).text()):
            r = i
            break
    else:
        AccInfo.tableWidget_trades.insertRow(0)

    AccInfo.tableWidget_trades.set_item_sig.emit(r, 0, trade_dict['ProdCode'].decode())
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 1, '')
    if trade_dict['BuySell'].decode() == 'B':
        AccInfo.tableWidget_trades.set_item_sig.emit(r, 2, str(trade_dict['Qty']))
    else:
        AccInfo.tableWidget_trades.set_item_sig.emit(r, 3, str(trade_dict['Qty']))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 4, f"{trade_dict['AvgPrice']:,}")
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 5, str(trade_dict['TradeNo']))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 6, ORDER_STATUS[trade_dict['Status']])
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 7, str(trade_dict['Initiator'].decode()))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 8, str(trade_dict['Ref'].decode()))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 9, str(dt.datetime.fromtimestamp(trade_dict['TradeTime'])))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 10, f"{trade_dict['OrderPrice']:,}")
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 11, str(trade_dict['IntOrderNo']))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 12, str(trade_dict['ExtOrderNo']))
    AccInfo.tableWidget_trades.set_item_sig.emit(r, 13, str(trade_dict['RecNO']))
    print('trade:', trade_dict)
    return trade_dict



def update_accbals():
    try:
        accbal_array = get_all_accbal_by_array()
        accbal = []
        for i in range(AccInfo.tableWidget_bal.rowCount()):
            AccInfo.tableWidget_bal.removeRow(0)
        for b in accbal_array:
            accbal.append(_update_accbals(b))
    except Exception as e:
        print('accbal_Error:', e)
        raise e

def _update_accbals(b):
    accbal_dict = {}
    for name, c_type in b._fields_:
        accbal_dict[name] = getattr(b, name)

    r = 0
    for i in range(AccInfo.tableWidget_bal.rowCount()):
        if accbal_dict['Ccy'].decode() == AccInfo.tableWidget_bal.item(i, 0).text():
            r = i
            break
    else:
        AccInfo.tableWidget_bal.insertRow(0)

    AccInfo.tableWidget_bal.set_item_sig.emit(r, 0, accbal_dict['Ccy'].decode())
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 1, f"{accbal_dict['CashBF']:,}")
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 2, f"{accbal_dict['NotYetValue']:,}")
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 3, f"{accbal_dict['TodayCash']:,}")
    total_cash = accbal_dict['CashBF'] + accbal_dict['NotYetValue'] + accbal_dict['TodayCash']
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 4, str(total_cash))
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 5, f"{accbal_dict['Unpresented']:,}")
    ccy = get_ccy_rate_by_ccy(accbal_dict['Ccy'].decode()).value
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 6, str(ccy))
    AccInfo.tableWidget_bal.set_item_sig.emit(r, 7, f"{total_cash * ccy:,}")
    # b['Todayout']
    AccInfo.tableWidget_bal.repaint()
    AccInfo.tableWidget_bal.update()
    print('accbal:', accbal_dict)
    return accbal_dict

def update_ccy_rate():
    try:
        ccy_list = ['CAD', 'CHF', 'EUR', 'GBP', 'HKD', 'JPY', 'KRW', 'MYR', 'SGD', 'USD']
        ccy_dict = {ccy:get_ccy_rate_by_ccy(ccy).value for ccy in ccy_list}
        for i in range(AccInfo.tableWidget_ccy_rate.rowCount()):
            AccInfo.tableWidget_ccy_rate.removeRow(0)
        for i, (ccy, rate) in enumerate(ccy_dict.items()):
            AccInfo.tableWidget_ccy_rate.insertRow(i)
            AccInfo.tableWidget_ccy_rate.setVerticalHeaderItem(i, QTableWidgetItem(ccy))
            AccInfo.tableWidget_ccy_rate.set_item_sig.emit(i, 0, str(rate))
    except Exception as e:
        print('ccy_Error:', e)
        raise e

info_update = [update_acc_info,
               update_orders,
               update_positions,
               update_trades,
               update_accbals,
               update_ccy_rate]

@on_account_info_push  # 普通客户登入后返回登入前的户口信息
def account_info_push(acc_info):
    info_handle('<账户>',
                f'{acc_info.ClientId.decode()}信息--NAV:{acc_info.NAV}-BaseCcy:{acc_info.BaseCcy.decode()}-BuyingPower:{acc_info.BuyingPower}-CashBal:{acc_info.CashBal}', acc_info)

@on_load_trade_ready_push  # 登入后，登入前已存的成交信息推送
def trade_ready_push(rec_no, trade):
    info_handle('<成交>',
                f'历史成交记录--NO:{rec_no}--{trade.OpenClose.decode()}成交@{trade.ProdCode.decode()}--{trade.BuySell.decode()}--Price:{trade.AvgPrice}--Qty:{trade.Qty}')

@on_account_position_push  # 普通客户登入后返回登入前的已存在持仓信息
def account_position_push(pos):
    info_handle('<持仓>',
                f'历史持仓信息--ProdCode:{pos.ProdCode.decode()}-PLBaseCcy:{pos.PLBaseCcy}-PL:{pos.PL}-Qty:{pos.Qty}-DepQty:{pos.DepQty}',
                pos)

@on_business_date_reply  # 登录成功后会返回一个交易日期
def business_date_reply(business_date):
    info_handle('<日期>', f'当前交易日--{dt.datetime.fromtimestamp(business_date)}')

@on_login_reply  # 登录调用
def reply(user_id, ret_code, ret_msg):
    if ret_code == 0:
        global local_login
        info_handle('<账户>', f'{user_id.decode()}登录成功')
        local_login = True
    else:
        info_handle('<账户>', f'{user_id.decode()}登录失败--errcode:{ret_code}--errmsg:{ret_msg.decode()}')
        local_login = False

# ----------------------------------------行情数据主推---------------------------------------------------------------------------------------------------
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
    # AccInfo.tableWidget_acc_info.item(6, 0).setText()
    AccInfo.tableWidget_acc_info.set_item_sig.emit(6, 0, str(price.Bid[0]))
# # -------------------------------------------------------------------------------------------------------------------------------------------------------

@on_connecting_reply  # 连接状态改变时调用
def connecting_reply(host_id, con_status):
    info_handle('<连接>', f'{HOST_TYPE[host_id]}状态改变--{HOST_CON_STATUS[con_status]}')

# -----------------------------------------------登入后的新信息回调------------------------------------------------------------------------------
@on_order_request_failed  # 订单请求失败时候调用
def order_request_failed(action, order, err_code, err_msg):
    info_handle('<订单>', f'请求失败--ACTION:{action}-@{order.ProdCode.decode()}-Price:{order.Price}-Qty:{order.Qty}-BuySell:{order.BuySell.decode()}      errcode;{err_code}-errmsg:{err_msg.decode()}')

@on_order_before_send_report  # 订单发送前调用
def order_before_snd_report(order):
    info_handle('<订单>', f'即将发送请求--@{order.ProdCode.decode()}-Price:{order.Price}-Qty:{order.Qty}-BuySell:{order.BuySell.decode()}')

@on_order_report  # 订单报告的回调推送
def order_report(rec_no, order):
    info_handle('<订单>', f'编号:{rec_no}-@{order.ProdCode.decode()}-Status:{ORDER_STATUS[order.Status]}', order)

@on_trade_report  # 成交记录更新后回调出推送新的成交记录
def trade_report(rec_no, trade):
    info_handle('<成交>', f'{rec_no}新成交{trade.OpenClose.decode()}--@{trade.ProdCode.decode()}--{trade.BuySell.decode()}--Price:{trade.AvgPrice}--Qty:{trade.Qty}', trade)

@on_updated_account_position_push  # 新持仓信息
def updated_account_position_push(pos):
    info_handle('<持仓>', f'信息变动--@{pos.ProdCode.decode()}-PLBaseCcy:{pos.PLBaseCcy}-PL:{pos.PL}-Qty:{pos.Qty}-DepQty:{pos.DepQty}', pos)

@on_updated_account_balance_push  # 户口账户发生变更时的回调，新的账户信息
def updated_account_balance_push(acc_bal):
    info_handle('<结余>', f'信息变动-{acc_bal.Ccy.decode()}-CashBF:{acc_bal.CashBF}-TodayCash:{acc_bal.TodayCash}-NotYetValue:{acc_bal.NotYetValue}-Unpresented:{acc_bal.Unpresented}-TodayOut:{acc_bal.TodayOut}', acc_bal)

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


def init_spapi():
    host = Login.lineEdit_host.text()
    port = Login.lineEdit_port.text()
    License = Login.lineEdit_license.text()
    app_id = Login.lineEdit_app_id.text()
    user_id = Login.lineEdit_user_id.text()
    password = Login.lineEdit_password.text()
    info = {'host':host, 'port': int(port), 'License':License, 'app_id':app_id, 'user_id':user_id}
    with open('info.plk', 'wb') as f:
        pickle.dump(info, f)
    # info.update(user_id=user_id, password=password)
    if initialize() == 0:
        info_handle('<API>','初始化成功')
        set_login_info(**info, password=password)
        info_handle('<连接>', f"设置登录信息-host:{info['host']} port:{info['port']} license:{info['License']} app_id:{info['app_id']} user_id:{info['user_id']}")
        login()
        Order.show()
        AccInfo.show()
        import time
        time.sleep(1.5)
        # AccInfo.toolButton_update_info.released.emit()
        # load_instrument_list()
        # load_productinfolist_by_code('HSI')
        # get_instrument_by_code('HSI')
        # print(get_product_by_array())
        # get_product_info('HSIJ8')
        # subscribe_price('HSIJ8', 1)
        # import time
        # time.sleep(2)
        # del time

def deinit_spapi():
    if logout() == 0:
        info_handle('<连接>',f'{c_char_p_user_id.value.decode()}登出请求发送成功')
        if unintialize() == 0:
            info_handle('<API>','释放成功')
            global local_login
            local_login = False


def get_product_info(code):
    global product_info
    try:
        product_info = get_product_by_code(code)
        print(product_info)
    except Exception as e:
        print(e)
        Order.checkBox_lock.setChecked(False)

def __get_current_order_info():
    row = AccInfo.tableWidget_orders.currentRow()
    if row >= 0:
        order_no = int(AccInfo.tableWidget_orders.item(AccInfo.tableWidget_orders.currentRow(), 0).text())
        prodcode = AccInfo.tableWidget_orders.item(AccInfo.tableWidget_orders.currentRow(),1).text()
        return  order_no, prodcode
    else:
        raise Exception('未选择订单')

def _del_current_selected_order():
    try:
        order_no, prodcode = __get_current_order_info()
        delete_order_by(order_no, prodcode)
    except Exception as e:
        print(e)

def _activate_selected_order():
    try:
        order_no, prodcode = __get_current_order_info()
        activate_order_by(order_no)
    except Exception as e:
        print(e)

def _inactivate_selected_order():
    try:
        order_no, prodcode = __get_current_order_info()
        inactivate_order_by(order_no)
    except Exception as e:
        print(e)

def addOrder(**kwargs):
    if local_login:
        add_order(**kwargs)
    else:
        print('未登录：', kwargs)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = SpLoginDialog()
    Order = OrderDialog()
    AccInfo = AccInfoWidget()
    Login.accepted.connect(lambda :init_spapi())
    Order.checkBox_lock.toggled.connect(lambda x: subscribe_price(Order.lineEdit_ProdCode.text(), 1) if x else subscribe_price(Order.lineEdit_ProdCode.text(), 0))

    def print_info(info_array):
        info_dict = {}
        for i in info_array:
            for name, c_type in i._fields_:
                info_dict[name] = getattr(i, name)
            print(info_dict)


    # AccInfo.tabWidget_acc_info.currentChanged.connect(lambda n: info_update[n]())
    AccInfo.pushButton_del_order.released.connect(lambda :_del_current_selected_order())
    AccInfo.pushButton_activate_order.released.connect(lambda :_activate_selected_order())
    AccInfo.pushButton_inactivate_order.released.connect(lambda :_inactivate_selected_order())
    AccInfo.pushButton_del_all_orders.released.connect(lambda :delete_all_orders())
    AccInfo.pushButton_activate_all_orders.released.connect(lambda :activate_all_orders())
    AccInfo.pushButton_inactivate_all_orders.released.connect(lambda :inactivate_all_orders())
    AccInfo.pushButton_inactivate_order.released.connect(lambda :print(AccInfo.tableWidget_orders.item(AccInfo.tableWidget_orders.currentRow(), 0).text()))
    AccInfo.toolButton_update_info.released.connect(lambda :[func() for func in info_update])

    Login.show()
    sys.exit(app.exec_())
