from PyQt5 import QtCore, QtGui, QtWidgets
import base64
import main
import img_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1089, 715)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1089, 715))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("position: center;")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(510, 270, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setStyleSheet("color: black;")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.lineEditLogin = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLogin.setGeometry(QtCore.QRect(380, 320, 321, 41))
        self.lineEditLogin.setPlaceholderText("login")
        self.lineEditLogin.setStyleSheet("border: none;\n"
"border-color: rgb(255, 255, 255);\n"
"background-color: rgb(193, 193, 193);")
        self.lineEditLogin.setObjectName("lineEditLogin")
        self.lineEditPasswrd = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPasswrd.setGeometry(QtCore.QRect(380, 390, 321, 41))
        self.lineEditPasswrd.setPlaceholderText("password")
        self.lineEditPasswrd.setStyleSheet("border: none;\n"
"border-color: rgb(255, 255, 255);\n"
"background-color: rgb(193, 193, 193);")
# "border-radius: 10px;")
        self.lineEditPasswrd.setObjectName("lineEditPasswrd")
        self.pushButtonSign = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSign.setGeometry(QtCore.QRect(470, 460, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(17)
        self.pushButtonSign.setFont(font)
        self.pushButtonSign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSign.setStyleSheet("border: none;\n"
"background-color: rgb(255, 126, 14);\n"
"font-family: Yu Gothic UI Semilight;")
        self.pushButtonSign.setObjectName("pushButtonSign")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 100, 371, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("image: url(:/newPrefix/img/Axenix_logo.png);\n"
"border-bottom: 2px solid orange;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButtonSign.clicked.connect(self.on_click)

    def on_click(self):
        login_value = self.lineEditLogin.text()
        passwd_value = self.lineEditPasswrd.text()
        print(login_value, passwd_value)
        if main.check_user(login_value, passwd_value):
            import interface_table
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("Неправильный пароль!")
            msg.setWindowTitle("Wrong password")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "login"))
        self.pushButtonSign.setText(_translate("MainWindow", "sign in"))
