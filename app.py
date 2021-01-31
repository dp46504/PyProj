from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QComboBox
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QFont
import sys
import time
import numpy as np
from Logic import getRandomExample, checkSpelling
import matplotlib.pyplot as plt


class Application():
    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.window = QStackedWidget()

        self.title = "Code Racer!"

        resolution = self.app.primaryScreen()
        size = resolution.size()
        screenWidth = size.width()
        screenHeight = size.height()

        print(screenWidth * 0.33)
        print(screenHeight * 0.42)
        self.winWidth = 640
        self.winHeight = 480
        self.winXPos = 300
        self.winYPos = 400

        self.window.setWindowTitle(self.title)
        self.window.setGeometry(self.winXPos, self.winYPos, self.winWidth, self.winHeight)
        self.window.setStyleSheet("background-color: #0e2a45")
        
        self.errors = np.array([0, 0, 0])
        self.examplesLength = np.array([0, 0, 0])
        self.timeForExample = np.array([0, 0, 0])

        self.initGameUI()
        self.initMenuUI()
        self.window.setCurrentWidget(self.menu)

        self.window.show()
        self.app.exec_()

    def initGameUI(self):
        """
        initGameUI initializes game UI

        :param: None
        :return: None
        """
        self.game = QWidget()
        self.gameLayout = QVBoxLayout()

        # Labels
        self.gameLabels = QHBoxLayout()

        self.roundLabel = QLabel("Code Racer") # utworzenie widgetu label
        self.roundLabel.setStyleSheet("color: #dbce18;") # dodanie styli css
        self.roundLabel.setFont(QFont('Arial', 20)) # ustawienie czcionki

        self.gameTimer = QLabel("00:00:00")
        self.gameTimer.setStyleSheet("color: #dbce18;")
        self.gameTimer.setFont(QFont('Arial', 20))

        self.gameLabels.addWidget(self.roundLabel)
        self.gameLabels.addWidget(self.gameTimer)
        self.gameLabels.setAlignment(self.roundLabel, Qt.AlignLeft)
        self.gameLabels.setAlignment(self.gameTimer, Qt.AlignRight)

        # Code
        self.labelCode = QLabel()
        self.labelCode.setFixedSize(640, 250)
        self.labelCode.setStyleSheet("background-color: #0a102e; color: #ffffff; padding: 10px; border-radius: 5px")
        self.labelCode.setFont(QFont('Arial', 18))
        self.labelCode.setAlignment(Qt.AlignLeft)

        # Input
        self.userInput = QPlainTextEdit()
        self.userInput.setFixedSize(640, 250)
        self.userInput.setStyleSheet("background-color: #596ed9; border: 1px solid #596ed9; border-radius: 5px;")
        self.userInput.setFont(QFont('Arial', 18))
        self.userInput.textChanged.connect(self.nextRound)

        self.gameLayout.addLayout(self.gameLabels)
        self.gameLayout.addWidget(self.labelCode)
        self.gameLayout.addWidget(self.userInput)

        self.game.setLayout(self.gameLayout)
        self.window.addWidget(self.game)

    def initMenuUI(self):
        """
        initMenuUI initializes menu UI

        :param: None
        :return: None
        """
        self.menu = QWidget()
        self.menu.setStyleSheet("QPushButton { background-color: #596ed9; color: #0e2a45; border: none; border-radius: 5px; width: 200px; height: 50px; } QComboBox { background-color: #596ed9; text-decoration: none; color: black; border: none; border-radius: 5px; } QAbstractItemView { background-color: #596ed9; }")

        self.menuLayout = QVBoxLayout()

        self.menuLabelLogo = QLabel(self.title)
        self.menuLabelLogo.setStyleSheet("color: #dbce18")
        self.menuLabelLogo.setFont(QFont('Arial', 20))
        self.menuLabelLogo.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.menuLabelLogo)

        self.menuText = QLabel("Welcome to Code Racer! This is a great place to practice your code typing skill. Choose from different programming languages and difficulties and start coding!\n\n Choose programming language:")
        self.menuText.setStyleSheet("color: #ffffff;")
        self.menuText.setFont(QFont('Arial', 14))
        self.menuText.setWordWrap(True)
        self.menuText.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.menuText)
        self.menuLayout.addStretch()

        self.select = QComboBox()
        self.select.addItems(["Python", "C++", "Java"])
        self.select.setFixedSize(200, 50)
        self.select.setFont(QFont('Arial', 18))
        self.menuLayout.addWidget(self.select)

        self.menuLayout.addStretch()
        self.menuButton1 = QPushButton("Easy")
        self.menuButton1.setStyleSheet("background-color: #32a852")
        self.menuButton1.setFont(QFont('Arial', 18))
        self.menuButton1.clicked.connect(lambda: self.startGame(self.menuButton1.text()))
        self.menuLayout.addWidget(self.menuButton1)

        self.menuButton2 = QPushButton("Medium")
        self.menuButton2.setStyleSheet("background-color: #dbce18;")
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

    def initSummaryUI(self):
        """
        initSummaryUI initializes summary UI

        :param: None
        :return: None
        """

        self.summary = QWidget()
        self.summaryLayout = QVBoxLayout()

        self.summaryLabel = QLabel("Podsumowanie")
        self.summaryLabel.setStyleSheet("color: #dbce18;")
        self.summaryLabel.setFont(QFont('Arial', 20))
        self.summaryLabel.setAlignment(Qt.AlignCenter)

        self.summaryLayout.addWidget(self.summaryLabel)
        self.summaryLayout.setAlignment(Qt.AlignTop)

        self.summary.setLayout(self.summaryLayout)
        self.window.addWidget(self.summary)

        # GENEROWANIE WYKRESU BLEDOW I CZASU \/
        # MOZNA DODAC ZAPISANIE DO PLIKU BO JAKIES MUSI BYC Xd

        # plt.subplot(1,2,1)
        # x=np.array(["Errors 1", "Errors 2", "Errors 3"])
        # y=np.array([self.errors[0], self.errors[1], self.errors[2]])
        # plt.bar(x, y, color='blue')

        # plt.subplot(1,2,2)
        # x=np.array(["Time 1", "Time 2", "Time 3"])
        # y=np.array([self.timeForExample[0], self.timeForExample[1], self.timeForExample[2]])
        # plt.bar(x, y, color='red')
        # plt.title("Results")
        # plt.show()


    def startGame(self, txt):
        """
        startGame starts game by setting up parameters and changing UI

        :param: None
        :return: None
        """
        self.rounds = 3
        self.currentRound = 1
        
        self.t1=time.perf_counter()
        self.t2=time.perf_counter()

        self.language = self.select.currentText()
        self.language = self.language.lower()
        self.difficulty = txt.lower()

        self.roundLabel.setText("Runda" + str(self.currentRound)) 
        self.code = getRandomExample(self.language, self.difficulty, self)
        self.t1 = time.perf_counter()
        self.labelCode.setText(self.code)
        self.window.setCurrentWidget(self.game)

    def nextRound(self):
        """
        nextRound runs new round or ends game

        :param: None
        :return: None
        """
        res = checkSpelling(self, self.code, self.userInput)
        
        if res == 1:
            if self.currentRound == self.rounds:
                self.t2 = time.perf_counter()
                self.timeForExample[self.currentRound-1] = self.t2-self.t1

                self.initSummaryUI()
                self.window.setCurrentWidget(self.summary)
            else:
                self.currentRound += 1

                self.t2 = time.perf_counter()
                self.timeForExample[self.currentRound-2] = self.t2-self.t1

                self.code = getRandomExample(self.language, self.difficulty, self)
                self.roundLabel.setText("Runda " + str(self.currentRound))
                self.labelCode.setText(self.code)
                self.t1 = time.perf_counter()
        elif res==-1:
            self.errors[self.currentRound-1]+=1
      
app = Application()