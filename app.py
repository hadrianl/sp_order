#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 0018 15:45
# @Author  : Hadrianl 
# @File    : app.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.QtWidgets import QApplication, QMessageBox
from SpInfo_ui import SpLoginDialog, OrderDialog, AccInfoWidget
from Spfunc import *
import sys



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


def init_spapi():
    host = Login.lineEdit_host.text()
    port = Login.lineEdit_port.text()
    License = Login.lineEdit_license.text()
    app_id = Login.lineEdit_app_id.text()
    user_id = Login.lineEdit_user_id.text()
    password = Login.lineEdit_password.text()
    info = {'host':host, 'port': int(port), 'License':License, 'app_id':app_id, 'user_id':user_id, 'password': password}
    # info.update(user_id=user_id, password=password)
    if initialize() == 0:
        info_handle('<API>','初始化成功')
        set_login_info(**info)
        info_handle('<连接>', f"设置登录信息-host:{info['host']} port:{info['port']} license:{info['License']} app_id:{info['app_id']} user_id:{info['user_id']}")
        login()
        Order.show()
        AccInfo.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = SpLoginDialog()
    Order = OrderDialog()
    AccInfo = AccInfoWidget()
    Login.accepted.connect(init_spapi)
    AccInfo.tabWidget_acc_info.currentChanged.connect(lambda n:print([get_orders_by_array,
                                                                      get_all_pos_by_array,
                                                                      get_all_trades_by_array,
                                                                      get_all_accbal_by_array][n]()))
    Login.show()
    sys.exit(app.exec_())
