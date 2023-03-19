from PyQt5 import QtWidgets
from Table import Table
import sys


class MyWindowTable(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindowTable, self).__init__()
        self.ui = Table()
        self.ui.setupUi(self)

    def closeEvent(self, a0):
        a0.accept()
        quit()


app_t = QtWidgets.QApplication([])
application_t = MyWindowTable()
application_t.show()
app_t.exec_()
