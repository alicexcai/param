import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import pyqtSlot
import sqlite3

def runGUI():

    class Params():

        ### AUTOGENERATE
        
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

    class Init(QMainWindow):
        def __init__(self):
            super().__init__()
            uic.loadUi('init.ui', self)
            self.folder = QtCore.QDir.currentPath()
            self.dirlabel.setText(self.folder)

        @pyqtSlot()
        def on_usegui_clicked(self):
            widget.addWidget(Dashboard())
            widget.setCurrentIndex(widget.currentIndex() + 1)
        
        @pyqtSlot()
        def on_selectdir_clicked(self):
            print("run function")
            self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.folder))
            QtCore.QDir.setCurrent(self.folder)
            QMessageBox.information(self, "Directory Selected", QtCore.QDir.currentPath())
            self.dirlabel.setText(self.folder)
            self.selectdir.setText("Change Directory")

        
    class Dashboard(QDialog):

        def __init__(self):
            super(Dashboard, self).__init__()
            uic.loadUi('dash.ui', self)

            # self.title = QLabel('Dashboard')
            # self.title.setFont(QtGui.QFont('Helvetica', 20))
            # self.title.setAlignment(QtCore.Qt.AlignCenter)

            # self.intboxl = 40
            # self.inaddboxl = 80
            # self.outtboxl = 40
            # self.outaddboxl = 80
            # self.incounter = 1
            # self.outcounter = 1
            # inoutlayout = QHBoxLayout()
            # # layout = QVBoxLayout()

            # # layout = QHBoxLayout()
            # # # Create a button in the window
            # # self.inbutton = QPushButton('Add Input', self)
            # inlayout = QGroupBox()
            # self.ingroup = QVBoxLayout()
            # inlayout.setLayout(self.ingroup)
            # self.ingroup.addWidget(self.addin)
            # # inoutlayout.addWidget(inlayout, 5)

            # # self.outbutton = QPushButton('Add Output', self)
            # outlayout = QGroupBox()
            # self.outgroup = QVBoxLayout()
            # outlayout.setLayout(self.outgroup)
            # self.outgroup.addWidget(self.addout)
            # # inoutlayout.addWidget(outlayout, 5)

            # inoutgroup = QGroupBox()
            # inoutgroup.setLayout(inoutlayout)
            # inoutgroup.show()

            # # self.parambutton = QPushButton('Set Parameters', self)
            # # self.parambutton.clicked.connect(self.on_parambutton_clicked)
            
            # # layout.addWidget(inoutgroup)   
            # # # layout.addWidget(self.parambutton)    
            # # self.setLayout(layout)

            # # connect button to function on_click
            # # self.inbutton.clicked.connect(self.add_in)
            # # self.outbutton.clicked.connect(self.add_out)
            # # self.show()

        @pyqtSlot()
        def on_addin_clicked(self):
            #this creates a new field and label everytime the button is clicked
            self.textbox = QLineEdit(self)
            # self.inlabel = QLabel(self)
            # self.inlayout.addWidget(self.label)
            self.inlayout.addWidget(self.textbox)

            # self.inlabel.setText("Input" + str(self.incounter))
            # self.label.move(5, self.intboxl)
            # self.inbutton.move(20, self.inaddboxl)
            # self.textbox.move(20, self.intboxl)
            # self.textbox.resize(280, 40)
            # #dynamic object names
            # self.textbox.setObjectName("input" + str(self.incounter))
            # self.textbox.show()
            # self.label.show()
            # self.intboxl += 40
            # self.inaddboxl += 40
            # self.incounter += 1
            print(self.textbox.objectName())
        
        @pyqtSlot()
        def on_addout_clicked(self):
            #this creates a new field and label everytime the button is clicked
            self.textbox = QLineEdit(self)
            # self.outlabel = QLabel(self)
            # self.outlayout.addWidget(self.label)
            self.outlayout.addWidget(self.textbox)

            # self.outlabel.setText("Output" + str(self.outcounter))
            # self.label.move(5, self.outtboxl)
            # self.outbutton.move(20, self.outaddboxl)
            # self.textbox.move(20, self.outtboxl)
            # self.textbox.resize(280, 40)
            # #dynamic object names
            # self.textbox.setObjectName("output" + str(self.outcounter))
            # self.textbox.show()
            # self.label.show()
            # self.outtboxl += 40
            # self.outaddboxl += 40
            # self.outcounter += 1
            print(self.textbox.objectName())


        def on_setparams_clicked(self):
            ### AUTOGENERATE - parameters UI
            print("SETPARAMS CLICKED")
            widget.addWidget(PrimaryParam())
            widget.setCurrentIndex(widget.currentIndex() + 1)

    # connect input text with Param() via template engine

    class PrimaryParam(QDialog):
        def __init__(self):
            super(PrimaryParam, self).__init__()
            uic.loadUi('primparam.ui', self)
            self.save.clicked.connect(self.on_save_clicked)
            self.moreparams.clicked.connect(self.on_moreparams_clicked)
        
        def on_save_clicked(self):
            # switch pages
            print("RUN!")

            # backend
            print("RUN FUCTNION STARTING...")

            ### AUTOGENERATE - set parameter ranges

            param_ranges = {
                'seed': self.seed.text(),
                'max_perms': self.permutations.text(),
                'num_rounds': self.num_rounds.text(),
                'mechanism': self.mechanism.currentText(),
                'budget': self.budget.text(),
                'reserve': self.reserve.text()
            }

            widget.addWidget(Output())
            widget.setCurrentIndex(widget.currentIndex() + 1)

            return param_ranges

        
        def on_moreparams_clicked(self):
            ### AUTOGENERATE - parameters UI
            print("MOREPARAMS CLICKED")
            widget.addWidget(MoreParams())
            widget.setCurrentIndex(widget.currentIndex() + 1)

    class MoreParams(QDialog):
        def __init__(self):
            super(MoreParams, self).__init__()
            uic.loadUi('moreparams.ui', self)
            self.save.clicked.connect(self.on_save_clicked)

        def on_save_clicked(self):
            widget.setCurrentIndex(widget.currentIndex() - 1)

    class Output(QDialog):
        def __init__(self):
            super(Output, self).__init__()
            uic.loadUi('output.ui', self)
            self.quit.clicked.connect(self.on_quit_clicked)

            # call simulation function
        
        def on_quit_clicked(self):
            # switch pages
            print("YOU QUIT")
            sys.exit(app.exec_())


    
    app = QApplication(sys.argv)
    main = Init()
    widget = QtWidgets.QStackedWidget()

    widget.addWidget(main)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

runGUI()