from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import main
import table_rc


class Table(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1420, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1420, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1420, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(530, -10, 391, 131))
        self.label.setStyleSheet("image: url(:/newPrefix/img/Axenix_logo_table.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 110, 1400, 715))
        self.tableWidget.setMinimumSize(QtCore.QSize(1400, 700))
        self.tableWidget.setMaximumSize(QtCore.QSize(1400, 700))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(14)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("border: none;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(350)
        MainWindow.setCentralWidget(self.centralwidget)
        self.tableWidget.setSortingEnabled(True)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def add_rows(self):
        data = main.get_all_data()
        for el in data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(el[0]))
            self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(round(el[1] * 10, 2))))
            if round(el[1] * 10, 2) >= 40:
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem('😩'))
            elif 31 <= round(el[1] * 10, 2) < 40:
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem('😐'))
            else:
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem('😁'))
            self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(round(el[2] * 10, 2))))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Сотрудник"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Текущий процент выгорания"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Настроение"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Через месяц"))
        self.add_rows()
