# Hand-coded Dashboard

class Dashboard(QDialog):

        def __init__(self):
            super(Dashboard, self).__init__()

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
            ### AUTOGENERATE - parameters UI
            print("PARAMBUTTON CLICKED")
            widget.addWidget(PrimaryParam())
            widget.setCurrentIndex(widget.currentIndex() + 1)