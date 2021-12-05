import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sqlite3

from sim import simulation

test_param_ranges = {
    'loglevel': ['info'], # ['info', 'debug']
    'mechanism': ['vcg'], # ['vcg', 'gsp', 'switch']
    'num_rounds': [3], # int
    'min_val': [25], # int
    'max_val': [175],
    'budget': [500000], # int
    'reserve': [0, 10, 50], # int
    'max_perms': [10],# int
    'iters': [1], # int
    'seed': [1, 2], # int
    'agent_class_names': [['Truthful', 'Truthful', 'Truthful', 'NANewbb']] # Truthful, NANewbb
}
simulation(test_param_ranges)

class Params():
    
    def __init__(self, loglevel='info', mechanism='vcg', num_rounds=48, min_val=25, max_val=175, budget=500000, reserve=0, max_perms=120, iters=1, seed=None, agent_class_names=['Truthful', 'Truthful', 'Truthful']):
        self.loglevel = loglevel
        self.mechanism = mechanism
        self.num_rounds = num_rounds
        self.min_val = min_val
        self.max_val = max_val
        self.budget = budget
        self.reserve = reserve
        self.max_perms = max_perms
        self.iters = iters
        self.seed = seed
        self.agent_class_names = agent_class_names

ParamsDefault = Params(loglevel='info', mechanism='gsp', num_rounds=48, min_val=25, max_val=175, budget=500000, reserve=0, max_perms=120, iters=1, seed=None, agent_class_names=['Truthful', 'Truthful', 'Truthful'])


###


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.title = QLabel('Dashboard')
        self.title.setFont(QtGui.QFont('Helvetica', 20))
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.intboxl = 40
        self.inaddboxl = 80
        self.outtboxl = 40
        self.outaddboxl = 80
        self.incounter = 1
        self.outcounter = 1
        inoutlayout = QHBoxLayout()
        layout = QVBoxLayout()

        # layout = QHBoxLayout()
        # Create a button in the window
        self.inbutton = QPushButton('Add Input', self)
        inlayout = QGroupBox()
        self.ingroup = QVBoxLayout()
        inlayout.setLayout(self.ingroup)
        self.ingroup.addWidget(self.inbutton)
        inoutlayout.addWidget(inlayout, 5)

        self.outbutton = QPushButton('Add Output', self)
        outlayout = QGroupBox()
        self.outgroup = QVBoxLayout()
        outlayout.setLayout(self.outgroup)
        self.outgroup.addWidget(self.outbutton)
        inoutlayout.addWidget(outlayout, 5)

        inoutgroup = QGroupBox()
        inoutgroup.setLayout(inoutlayout)

        self.parambutton = QPushButton('Set Parameters', self)
        self.parambutton.clicked.connect(self.on_parambutton_clicked)
        
        layout.addWidget(self.title)
        layout.addWidget(inoutgroup)   
        layout.addWidget(self.parambutton)    
        self.setLayout(layout)

        # connect button to function on_click
        self.inbutton.clicked.connect(self.add_in)
        self.outbutton.clicked.connect(self.add_out)
        self.show()

    @pyqtSlot()
    def add_in(self):
        #this creates a new field and label everytime the button is clicked
        self.textbox = QLineEdit(self)
        self.label = QLabel(self)
        self.ingroup.addWidget(self.label)
        self.ingroup.addWidget(self.textbox)

        self.label.setText("Input" + str(self.incounter))
        self.label.move(5, self.intboxl)
        self.inbutton.move(20, self.inaddboxl)
        self.textbox.move(20, self.intboxl)
        self.textbox.resize(280, 40)
        #dynamic object names
        self.textbox.setObjectName("input" + str(self.incounter))
        self.textbox.show()
        self.label.show()
        self.intboxl += 40
        self.inaddboxl += 40
        self.incounter += 1
        print(self.textbox.objectName())

    def add_out(self):
         #this creates a new field and label everytime the button is clicked
        self.textbox = QLineEdit(self)
        self.label = QLabel(self)

        self.outgroup.addWidget(self.label)
        self.outgroup.addWidget(self.textbox)

        self.label.setText("Output" + str(self.outcounter))
        self.label.move(5, self.outtboxl)
        self.outbutton.move(20, self.outaddboxl)
        self.textbox.move(20, self.outtboxl)
        self.textbox.resize(280, 40)
        #dynamic object names
        self.textbox.setObjectName("output" + str(self.outcounter))
        self.textbox.show()
        self.label.show()
        self.outtboxl += 40
        self.outaddboxl += 40
        self.outcounter += 1
        print(self.textbox.objectName())


    def on_parambutton_clicked(self):
        # switch pages
        print("SET PARAM CLICKED")
        param = PrimaryParam()
        widget.addWidget(param)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# connect input text with Param() via template engine


class PrimaryParam(QDialog):
    def __init__(self):
        super(PrimaryParam, self).__init__()
        uic.loadUi('primparam.ui', self)
        self.run.clicked.connect(self.on_run_clicked)

        # call simulation function
    
    def on_run_clicked(self):
        # switch pages

        # seed = self.seed.text()
        # max_perms = self.permutations.text()
        # num_rounds = self.num_rounds.text()
        # mechanism = self.mechanism.currentText()
        # budget = self.budget.text()
        # reserve = self.reserve.text()

        # print(num_rounds, seed, max_perms, mechanism, budget, reserve)
        print("RUN!")

        # backend
        print("BACKEND STARTING")
        param_ranges = {
            'seed': self.seed.text(),
            'max_perms': self.permutations.text(),
            'num_rounds': self.num_rounds.text(),
            'mechanism': self.mechanism.currentText(),
            'budget': self.budget.text(),
            'reserve': self.reserve.text()
        }
        print("PARAM RANGES", param_ranges)
    
        simulation(param_ranges)


app = QApplication(sys.argv)
main = Dashboard()
widget = QtWidgets.QStackedWidget()

widget.addWidget(main)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
