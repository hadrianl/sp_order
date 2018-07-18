#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 0009 11:35
# @Author  : Hadrianl 
# @File    : utils.py
# @License : (C) Copyright 2013-2017, 凯瑞投资
import datetime as dt
import configparser

MT4_ORDER_TYPE = {0: '买入',
                  1: '卖出',
                  2: '限价买入',
                  3: '止损买入',
                  4: '限价卖出',
                  5: '止损卖出',
                  6: '存入'}

FOLLOWER_STRATEGY = {8946946:0,
                     8942813:0,
                     8946490:0}

parser = configparser.ConfigParser()
parser.read('info.conf')

HOST = parser.get('MYSQL', 'HOST')
PORT= parser.getint('MYSQL', 'PORT')
USER= parser.get('MYSQL', 'USER')
PASSWD= parser.get('MYSQL', 'PASSWD')
DB= parser.get('MYSQL', 'DB')

def get_order_cond(order):
    order_kwargs = {}
    if not isinstance(order, dict):
        for name, c_type in order._fields_:
            v = getattr(order, name)
            v = v.decode() if isinstance(v, bytes) else v
            order_kwargs[name] = v
    else:
        order_kwargs = order

    _stoptype_text = {'L': '损>=' if order_kwargs['BuySell'] == 'B' else '损<=',
                      'U': '升>=',
                      'D': '跌<='}
    cond = ''
    if order_kwargs['CondType'] == 0:
        if all(k in order_kwargs for k in ('UpLevel', 'UpPrice', 'DownLevel', 'DownPrice')) and any(order_kwargs.get(k, 0)!=0 for k in ('UpLevel', 'UpPrice', 'DownLevel', 'DownPrice')):
            if order_kwargs['BuySell'] == 'B':
                _profit = order_kwargs['UpLevel'] - order_kwargs['Price']
                _loss = order_kwargs['Price'] - order_kwargs['DownLevel']
                _loss_toler = order_kwargs['DownLevel'] - order_kwargs['DownPrice']
                cond = f"牛市 = 赚{_profit} 损{_loss}(+{_loss_toler})"
            elif order_kwargs['BuySell'] == 'S':
                _profit = order_kwargs['Price'] - order_kwargs['DownLevel']
                _loss = order_kwargs['UpLevel'] - order_kwargs['Price']
                _loss_toler = order_kwargs['UpPrice'] - order_kwargs['UpLevel']
                cond = f"熊市 = 赚{_profit} 损{_loss}(+{_loss_toler})"
    elif order_kwargs['CondType'] == 1:
        cond = f"{_stoptype_text[order_kwargs['StopType']]} {order_kwargs['StopLevel']}"
    elif order_kwargs['CondType'] == 6:
        if order_kwargs['BuySell'] == 'B':
            cond = f"{_stoptype_text[order_kwargs['StopType']]} {order_kwargs['StopLevel']}（追<={order_kwargs['UpLevel'] - order_kwargs['DownLevel']})"
        elif order_kwargs['BuySell'] == 'S':
            cond = f"{_stoptype_text[order_kwargs['StopType']]} {order_kwargs['StopLevel']}（追>={order_kwargs['DownLevel'] + order_kwargs['UpLevel']})"
    elif order_kwargs['CondType'] == 4:
        if order_kwargs['BuySell'] == 'B':
            cond = f"双向 损:{order_kwargs['UpPrice']}(>={order_kwargs['UpLevel']})"
        elif order_kwargs['BuySell'] == 'S':
            cond = f"双向 损:{order_kwargs['DownPrice']}(<={order_kwargs['DownLevel']})"
    elif order_kwargs['CondType'] == 3:
        _sched_time = dt.datetime.fromtimestamp(order_kwargs['SchedTime'])
        cond = f">={_sched_time}"

    return cond


def print_info(ctype_data):
    info_dict = {}
    for name, c_type in ctype_data._fields_:
        info_dict[name] = getattr(ctype_data, name)
    print(info_dict)
    return  info_dict
