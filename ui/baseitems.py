#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 0023 19:04
# @Author  : Hadrianl 
# @File    : baseitems.py
# @License : (C) Copyright 2013-2017, 凯瑞投资


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal

class QInfoWidget(QTableWidget):
    set_item_sig = pyqtSignal(int, int, str)
    update_item_sig = pyqtSignal(int, int, str)
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.set_item_sig.connect(lambda x,y,s: self.setItem(x, y, QTableWidgetItem(s)))
        self.update_item_sig.connect(lambda x,y,s: self.item(x, y).setText(s))
