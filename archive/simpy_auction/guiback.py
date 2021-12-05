import sys

from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.uic import loadUi

import sqlite3
from PyQt5.QtCore import pyqtSlot

class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi('dashboard.ui', self)
        self.setparam.clicked.connect(self.on_setparam_clicked)

    def on_setparam_clicked(self):
        # switch pages
        widget.addWidget(Param())
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Param(QDialog):
    def __init__(self):
        super(Param, self).__init__()
        loadUi('param.ui', self)
        self.run.clicked.connect(self.on_run_clicked)

    def on_run_clicked(self):
        # set parameters to input text
        mechanism = self.mechanism.text()
        print(mechanism)

        # call simulation function





# main
app = QApplication(sys.argv)
main = Dashboard()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
