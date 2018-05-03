#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 0023 19:04
# @Author  : Hadrianl 
# @File    : baseitems.py
# @License : (C) Copyright 2013-2017, 凯瑞投资


from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.Qt import QObject, QIcon
from PyQt5.QtCore import pyqtSignal, QThread
from queue import Queue

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