from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
import sys

## KOMENTARZ

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.winWidth = 640
        self.winHeight = 480
        self.winXPos = 300
        self.winYPos = 400

        self.setGeometry(self.winXPos, self.winYPos, self.winWidth, self.winHeight)
        self.setWindowTitle("Code Racer!")
        self.setStyleSheet("background-color: #0e2a45")
        self.initUI()
##KOMENTARZ MUJ
    def initUI(self):
        
        # Logo
        self.labelLogo = QtWidgets.QLabel(self) # utworzenie widgetu label
        self.labelLogo.setText("Code Racer") # ustawienie tekstu
        self.labelLogo.setStyleSheet("color: #dbce18;") # dodanie styli css
        self.labelLogo.setGeometry(QRect(20, 20, 600, 40)) # ustawienie pozycji i rozmiaru widgetu
        self.labelLogo.setFont(QFont('Arial', 20)) # ustawienie czcionki
        self.labelLogo.setAlignment(Qt.AlignCenter) # ustawienie pozycji tekstu wewnątrz widgetu

        # Code
        self.labelCode = QtWidgets.QLabel(self)
        self.labelCode.setText("def myFunction(arg):\n\tpass")
        self.labelCode.setGeometry(QRect(20, 80, 600, 300))
        self.labelCode.setStyleSheet("background-color: #0a102e; color: #ffffff; padding: 10px; border-radius: 5px")
        self.labelCode.setFont(QFont('Arial', 18))
        self.labelCode.setAlignment(Qt.AlignLeft)

        # Input
        self.userInput = QtWidgets.QLineEdit(self)
        self.userInput.setGeometry(QRect(20, 400, 600, 40))
        self.userInput.setStyleSheet("background-color: #596ed9; border: 1px solid red; border-radius: 5px;")
        self.userInput.setFont(QFont('Arial', 18))

        self.userInput.textEdited.connect(self.onTextChange)

    def onTextChange(self):
        self.labelCode.setText(self.userInput.text())

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()