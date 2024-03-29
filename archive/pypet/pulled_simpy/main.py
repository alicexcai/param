# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Parameters(object):
    def setupUi(self, Parameters):
        Parameters.setObjectName("Parameters")
        Parameters.resize(475, 191)
        self.gridLayout_3 = QtWidgets.QGridLayout(Parameters)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Parameters)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Parameters)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Parameters)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Parameters)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(Parameters)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Parameters)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(Parameters)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Parameters)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Parameters)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.retranslateUi(Parameters)
        self.buttonBox.rejected.connect(Parameters.reject)
        self.buttonBox.accepted.connect(Parameters.accept)
        QtCore.QMetaObject.connectSlotsByName(Parameters)

    def retranslateUi(self, Parameters):
        _translate = QtCore.QCoreApplication.translate
        Parameters.setWindowTitle(_translate("Parameters", "Dialog"))
        self.label_2.setText(_translate("Parameters", "Seeds"))
        self.label_3.setText(_translate("Parameters", "Permutations"))
        self.label_5.setText(_translate("Parameters", "Reserve"))
        self.label_6.setText(_translate("Parameters", "Mechanism"))
        self.label.setText(_translate("Parameters", "# of Rounds"))
        self.label_4.setText(_translate("Parameters", "Budget"))
        self.label_7.setText(_translate("Parameters", "Set Parameters"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Parameters = QtWidgets.QDialog()
    ui = Ui_Parameters()
    ui.setupUi(Parameters)
    Parameters.show()
    sys.exit(app.exec_())
