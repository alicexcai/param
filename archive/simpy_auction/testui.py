import sys
from PyQt5.QtWidgets import *
# QMainWindow, QGridLayout, QListWidget, QApplication, QWidget, QHBoxLayout, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
# from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.intboxl = 40
        self.inaddboxl = 80
        self.outtboxl = 40
        self.outaddboxl = 80
        self.incounter = 1
        self.outcounter = 1
        layout = QHBoxLayout()

        # layout = QHBoxLayout()
        # Create a button in the window
        self.inbutton = QPushButton('Add Input', self)
        inlayout = QGroupBox("Input Group")
        self.ingroup = QVBoxLayout()
        inlayout.setLayout(self.ingroup)
        self.ingroup.addWidget(self.inbutton)
        layout.addWidget(inlayout)

        self.outbutton = QPushButton('Add Output', self)
        outlayout = QGroupBox("Output Group")
        self.outgroup = QVBoxLayout()
        outlayout.setLayout(self.outgroup)
        self.outgroup.addWidget(self.outbutton)
        layout.addWidget(outlayout)
        
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dashboard()
    sys.exit(app.exec_())