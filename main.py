from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from ventana import Ui

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()