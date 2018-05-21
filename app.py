#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 0018 15:45
# @Author  : Hadrianl 
# @File    : app.py
# @License : (C) Copyright 2013-2017, 凯瑞投资

from PyQt5.QtWidgets import QApplication
from SpInfo_ui import  MainWindow
from spapi.spAPI import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setWindowTitle('Sharp Point Order System --- Carry Investment')  # 设置窗口标题
    win.Login.lineEdit_password.setFocus()  # 焦点到密码输入
    win.Login.show()
    sys.exit(app.exec_())
