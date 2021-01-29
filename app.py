from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QPlainTextEdit, QComboBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
import sys
from Logic import getRandomExample, checkSpelling

class Application():
    def __init__(self):
        super().__init__()

        self.app = QApplication([])
        self.window = QStackedWidget()

        self.title = "Code Racer!"
        self.winWidth = 640
        self.winHeight = 480
        self.winXPos = 300
        self.winYPos = 400

        self.window.setWindowTitle(self.title)
        self.window.setGeometry(self.winXPos, self.winYPos, self.winWidth, self.winHeight)
        self.window.setStyleSheet("background-color: #0e2a45")
        
        self.initGameUI()
        self.initMenuUI()
        self.window.setCurrentWidget(self.menu)

        self.window.show()
        self.app.exec_()

    def initGameUI(self):
        """
        initGameUI inicjalizuje interfejs gry

        :param: brak
        :return: brak
        """
        self.game = QWidget()
        self.gameLayout = QVBoxLayout()

        # Logo
        self.labelLogo = QLabel("Code Racer") # utworzenie widgetu label
        self.labelLogo.setStyleSheet("color: #dbce18;") # dodanie styli css
        self.labelLogo.setGeometry(QRect(20, 20, 600, 40)) # ustawienie pozycji i rozmiaru widgetu
        self.labelLogo.setFont(QFont('Arial', 20)) # ustawienie czcionki
        self.labelLogo.setAlignment(Qt.AlignCenter) # ustawienie pozycji tekstu wewnątrz widgetu

        # Code
        self.labelCode = QLabel()
        self.labelCode.setFixedSize(640, 250)
        self.labelCode.setStyleSheet("background-color: #0a102e; color: #ffffff; padding: 10px; border-radius: 5px")
        self.labelCode.setFont(QFont('Arial', 18))
        self.labelCode.setAlignment(Qt.AlignLeft)

        # Input
        self.userInput = QPlainTextEdit()
        self.userInput.textChanged.connect(lambda: checkSpelling(self.text, self.userInput))
        
        self.userInput.setFixedSize(640, 250)
        self.userInput.setStyleSheet("background-color: #596ed9; border: 1px solid #596ed9; border-radius: 5px;")
        self.userInput.setFont(QFont('Arial', 18))
        #self.userInput.textChanged.connect(lambda: checkSpelling(self.text, self.userInput))

        self.gameLayout.addWidget(self.labelLogo)
        self.gameLayout.addWidget(self.labelCode)
        self.gameLayout.addWidget(self.userInput)

        self.game.setLayout(self.gameLayout)
        self.window.addWidget(self.game)

    def initMenuUI(self):
        """
        initMenuUI inicjalizuje interfejs menu

        :param: brak
        :return: brak
        """
        self.menu = QWidget()
        self.menu.setStyleSheet("QPushButton { background-color: #dbce18; color: #0e2a45; border: none; border-radius: 5px; width: 200px; height: 50px; } QComboBox { background-color: #596ed9; text-decoration: none; color: black; border: none; border-radius: 5px; } QAbstractItemView { background-color: #596ed9; }")

        self.menuLayout = QVBoxLayout()

        self.menuLabelLogo = QLabel(self.title)
        self.menuLabelLogo.setStyleSheet("color: #dbce18")
        self.menuLabelLogo.setFixedSize(600, 100)
        self.menuLabelLogo.setFont(QFont('Arial', 20))
        self.menuLabelLogo.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.menuLabelLogo)

        self.select = QComboBox()
        self.select.addItems(["Python", "C++", "Java"])
        self.select.setFixedSize(200, 50)
        self.select.setFont(QFont('Arial', 18))
        self.menuLayout.addWidget(self.select)

        self.menuButton1 = QPushButton("Easy")
        self.menuButton1.setStyleSheet("background-color: #32a852")
        self.menuButton1.setFont(QFont('Arial', 18))
        self.menuButton1.clicked.connect(lambda: self.startGame(self.menuButton1.text()))
        self.menuLayout.addWidget(self.menuButton1)

        self.menuButton2 = QPushButton("Medium")
        self.menuButton2.setFont(QFont('Arial', 18))
        self.menuButton2.clicked.connect(lambda: self.startGame(self.menuButton2.text()))
        self.menuLayout.addWidget(self.menuButton2)

        self.menuButton3 = QPushButton("Hard")
        self.menuButton3.setStyleSheet("background-color: #ad3238")
        self.menuButton3.setFont(QFont('Arial', 18))
        self.menuButton3.clicked.connect(lambda: self.startGame(self.menuButton3.text()))
        self.menuLayout.addWidget(self.menuButton3)

        self.menuButton4 = QPushButton("Exit")
        self.menuButton4.setFont(QFont('Arial', 18))
        self.menuButton4.clicked.connect(self.app.exit)

        self.menuLayout.addStretch()
        self.menuLayout.addWidget(self.menuButton4)

        self.menuLayout.setAlignment(self.select, Qt.AlignHCenter)
        self.menuLayout.setAlignment(self.menuButton1, Qt.AlignHCenter)
        self.menuLayout.setAlignment(self.menuButton2, Qt.AlignHCenter)
        self.menuLayout.setAlignment(self.menuButton3, Qt.AlignHCenter)
        self.menuLayout.setAlignment(self.menuButton4, Qt.AlignHCenter)

        self.menuLayout.addStretch()
        self.menu.setLayout(self.menuLayout)
        self.window.addWidget(self.menu)

    def onTextChange(self):
        self.labelCode.setText(self.userInput.text())

    def startGame(self, text):

        language = self.select.currentText()
        language = language.lower()
        difficulty = text.lower()
        self.text = getRandomExample(language, difficulty)
        self.labelCode.setText(self.text)
        self.window.setCurrentWidget(self.game)

app = Application()