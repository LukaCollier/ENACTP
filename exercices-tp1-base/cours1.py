#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QLCDNumber, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


def changed(nw_value):
    print(nw_value)

print("2")
app = QApplication(sys.argv)
container = QWidget()
lcd = QLCDNumber()
sld = QSlider(Qt.Horizontal)
vbox = QVBoxLayout()
vbox.addWidget(lcd)
vbox.addWidget(sld)
container.setLayout(vbox)
sld.valueChanged.connect(lcd.display)
sld.valueChanged.connect(changed)
container.setGeometry(300, 300, 250, 150)
container.show()
print("3")
app.exec()
print("4")
