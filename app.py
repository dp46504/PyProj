from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QComboBox
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtChart import QBarSet, QBarSeries, QChart, QBarCategoryAxis, QValueAxis, QChartView
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from pyqtgraph import BarGraphItem, plot
from Logic import getRandomExample, checkSpelling, savechart


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

        self.winWidth = int((screenWidth / 10) * 5)
        self.winHeight = int((screenHeight / 10) * 6)
        self.winXPos = int(screenWidth / 2 - (self.winWidth / 2))
        self.winYPos = int(screenHeight / 2 - (self.winHeight / 2))

        self.window.setWindowTitle(self.title)
        self.window.setGeometry(self.winXPos, self.winYPos, self.winWidth, self.winHeight)
        self.window.setStyleSheet("background-color: #a5ba45")
        
        self.errors = np.array([0, 0, 0])
        self.examplesLength = np.array([0, 0, 0])
        self.timeForExample = np.array([0, 0, 0])

        self.initGameUI()
        self.initMenuUI()
        self.window.setCurrentWidget(self.menu)

        self.gameEnded = False
        self.secs = 0

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

        self.gameLabels = QHBoxLayout()
        self.roundLabel = QLabel("Code Racer")
        self.roundLabel.setFixedHeight(int(self.winHeight / 10))
        self.roundLabel.setStyleSheet("color: #1E5903;")
        self.roundLabel.setFont(QFont('Arial', 20))

        self.gameTimer = QLabel("00:00")
        self.gameTimer.setFixedHeight(int(self.winHeight / 10))
        self.gameTimer.setStyleSheet("color: #1E5903;")
        self.gameTimer.setFont(QFont('Arial', 20))

        self.gameLabels.addWidget(self.roundLabel)
        self.gameLabels.addWidget(self.gameTimer)
        self.gameLabels.setAlignment(self.roundLabel, Qt.AlignLeft)
        self.gameLabels.setAlignment(self.gameTimer, Qt.AlignRight)

        self.labelCode = QLabel()
        self.labelCode.setFixedHeight(int(self.winHeight / 10 * 4.5))
        self.labelCode.setStyleSheet("background-color: transparent; color: #000; padding: 10px; border-radius: 5px")
        self.labelCode.setFont(QFont('Arial', 18))
        self.labelCode.setAlignment(Qt.AlignLeft)

        self.userInput = QPlainTextEdit()
        self.userInput.setFixedHeight(int(self.winHeight / 10 * 4.5))
        self.userInput.setStyleSheet("background-color: #60A62E; color: #000; border: 5px solid transparent; border-radius: 5px;")
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
        self.menu.setStyleSheet("QPushButton { background-color: #60A62E; color: #000; border: none; border-radius: 5px; width: 200px; height: 50px; } QComboBox { background-color: #60A62E; text-decoration: none; color: #000; border: none; border-radius: 5px; } QAbstractItemView { background-color: #60A62E; color: #000;}")

        self.menuLayout = QVBoxLayout()

        self.menuLabelLogo = QLabel(self.title)
        self.menuLabelLogo.setStyleSheet("color: #1E5903")
        self.menuLabelLogo.setFont(QFont('Arial', 24, 81))
        self.menuLabelLogo.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.menuLabelLogo)

        self.menuText = QLabel("Welcome to Code Racer! This is a great place to practice your code typing skill. Choose from different programming languages and difficulties and start coding!\n\n Choose programming language:")
        self.menuText.setStyleSheet("color: #1E5903;")
        self.menuText.setFont(QFont('Arial', 16))
        self.menuText.setWordWrap(True)
        self.menuText.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.menuText)

        self.select = QComboBox()
        self.select.addItems(["Python", "C++"])
        self.select.setFixedSize(200, 50)
        self.select.setFont(QFont('Arial', 18))
        self.menuLayout.addWidget(self.select)

        self.menuLayout.addStretch()
        self.difficultyLabel = QLabel("Choose difficulty:")
        self.difficultyLabel.setStyleSheet("color: #1E5903;")
        self.difficultyLabel.setFont(QFont('Arial', 16))
        self.difficultyLabel.setAlignment(Qt.AlignCenter)
        self.menuLayout.addWidget(self.difficultyLabel)

        self.menuButton1 = QPushButton("Easy")
        self.menuButton1.setStyleSheet("background-color: #60A62E")
        self.menuButton1.setFont(QFont('Arial', 18))
        self.menuButton1.clicked.connect(lambda: self.startGame(self.menuButton1.text()))
        self.menuLayout.addWidget(self.menuButton1)

        self.menuButton2 = QPushButton("Medium")
        self.menuButton2.setStyleSheet("background-color: #46801d;")
        self.menuButton2.setFont(QFont('Arial', 18))
        self.menuButton2.clicked.connect(lambda: self.startGame(self.menuButton2.text()))
        self.menuLayout.addWidget(self.menuButton2)

        self.menuButton3 = QPushButton("Hard")
        self.menuButton3.setStyleSheet("background-color: #154001")
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
        self.summary.setStyleSheet("QPushButton { background-color: #60A62E; color: #000; border: none; border-radius: 5px; width: 200px; height: 50px; }")
        self.summaryLayout = QVBoxLayout()

        self.summaryLabel = QHBoxLayout()

        mins = str(int(np.floor(self.secs / 60)))
        secs = str(int(self.secs % 60))
        if int(mins) < 10:
            mins = "0" + mins

        if int(secs) < 10:
            secs = "0" + secs

        totalTime = "Total time: " + mins + ":" + secs

        self.totalTimeLabel = QLabel(totalTime)
        self.totalTimeLabel.setMaximumHeight(int(self.winHeight / 10))
        self.totalTimeLabel.setStyleSheet("color: #1E5903;")
        self.totalTimeLabel.setFont(QFont('Arial', 20, 75))
        self.totalTimeLabel.setAlignment(Qt.AlignCenter)

        self.summaryLabel.addWidget(self.totalTimeLabel)
        self.summaryLabel.setAlignment(self.totalTimeLabel, Qt.AlignLeft)

        totalMistakes = "Total mistakes: " + str(np.sum(self.errors))
        self.totalMistakesLabel = QLabel(totalMistakes)
        self.totalMistakesLabel.setMaximumHeight(int(self.winHeight / 10))
        self.totalMistakesLabel.setStyleSheet("color: #1E5903;")
        self.totalMistakesLabel.setFont(QFont('Arial', 20, 75))
        self.totalMistakesLabel.setAlignment(Qt.AlignCenter)

        self.summaryLabel.addWidget(self.totalMistakesLabel)
        self.summaryLabel.setAlignment(self.totalMistakesLabel, Qt.AlignRight)
        self.summaryLayout.addLayout(self.summaryLabel)

        times = QBarSet("Time")
        times.setColor(QColor(255, 0, 0, 127))
        times.append(self.timeForExample[0])
        times.append(self.timeForExample[1])
        times.append(self.timeForExample[2])

        timeSeries = QBarSeries()
        timeSeries.append(times)

        timeChart = QChart()
        timeChart.addSeries(timeSeries)
        timeChart.setTitle("Round times chart")

        categories = ["round 1", "round 2", "round 3"]
        timesAxisX = QBarCategoryAxis()

        timesAxisX.append(categories)
        timeChart.addAxis(timesAxisX, Qt.AlignBottom)
        timeSeries.attachAxis(timesAxisX)

        timesAxisY = QValueAxis()
        timesAxisY.setRange(0, np.max(self.timeForExample))
        timeChart.addAxis(timesAxisY, Qt.AlignLeft)
        timeSeries.attachAxis(timesAxisY)

        timeChart.legend().setVisible(False)

        timeChartView = QChartView(timeChart)
        timeChartView.setFixedSize(int(self.winWidth), int(self.winWidth / 3))
        self.summaryLayout.addWidget(timeChartView)

        errors = QBarSet("Mistakes")
        errors.setColor(QColor(0, 0, 255, 127))

        errors.append(self.errors[0])
        errors.append(self.errors[1])
        errors.append(self.errors[2])

        errorSeries = QBarSeries()
        errorSeries.append(errors)

        errorChart = QChart()
        errorChart.addSeries(errorSeries)
        errorChart.setTitle("Round mistakes chart")

        errorsAxisX = QBarCategoryAxis()
        errorsAxisX.append(categories)
        errorChart.addAxis(errorsAxisX, Qt.AlignBottom)
        errorSeries.attachAxis(errorsAxisX)

        errorsAxisY = QValueAxis()
        errorsAxisY.setRange(0, np.max(self.errors))
        errorChart.addAxis(errorsAxisY, Qt.AlignLeft)
        errorSeries.attachAxis(errorsAxisY) 

        errorChartView = QChartView(errorChart)
        errorChartView.setFixedSize(int(self.winWidth), int(self.winWidth / 3))
        errorChart.legend().setVisible(False)
        self.summaryLayout.addWidget(errorChartView)

        self.summaryButtons = QHBoxLayout()
        self.saveButton = QPushButton("Save to file")
        self.saveButton.setFont(QFont('Arial', 18))
        self.saveButton.clicked.connect(lambda: savechart(self.errors, self.timeForExample))

        self.playAgainButton = QPushButton("Play Again!")
        self.playAgainButton.setFont(QFont('Arial', 18))
        self.playAgainButton.clicked.connect(self.playAgain)

        self.exitButton = QPushButton("Exit")
        self.exitButton.setFont(QFont('Arial', 18))
        self.exitButton.clicked.connect(self.app.exit)

        self.summaryButtons.addWidget(self.saveButton)
        self.summaryButtons.addWidget(self.playAgainButton)
        self.summaryButtons.addWidget(self.exitButton)

        self.summaryButtons.setAlignment(self.saveButton, Qt.AlignLeft)
        self.summaryButtons.setAlignment(self.playAgainButton, Qt.AlignCenter)
        self.summaryButtons.setAlignment(self.exitButton, Qt.AlignRight)

        self.summaryLayout.addLayout(self.summaryButtons)
        self.summary.setLayout(self.summaryLayout)
        self.window.addWidget(self.summary)


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

        self.roundLabel.setText("Round " + str(self.currentRound) + " of 3")
        self.code = getRandomExample(self.language, self.difficulty, self)
        self.labelCode.setText(self.code)
        self.window.setCurrentWidget(self.game)
        self.started = False
        self.totalTimer = False

    def nextRound(self):
        """
        nextRound runs new round or ends game

        :param: None
        :return: None
        """
        if not self.started:
            self.t1 = time.perf_counter()
            self.started = True

        if not self.totalTimer:
            self.setTimer()
            self.totalTimer = True

        res = checkSpelling(self, self.code, self.userInput)
        
        if res == 1:
            if self.currentRound == self.rounds:
                self.t2 = time.perf_counter()
                self.timeForExample[self.currentRound-1] = self.t2-self.t1

                self.gameEnded = True
                self.initSummaryUI()
                self.window.setCurrentWidget(self.summary)
            else:
                self.currentRound += 1

                self.t2 = time.perf_counter()
                self.timeForExample[self.currentRound-2] = self.t2-self.t1

                self.code = getRandomExample(self.language, self.difficulty, self)
                self.roundLabel.setText("Round " + str(self.currentRound) + " of 3")
                self.labelCode.setText(self.code)
                self.started = False
        elif res==-1:
            self.errors[self.currentRound-1]+=1

    def setTimer(self):
        """
        setTimer sets timer to start from 00:00

        :param: None
        :return: None
        """
        mins = int(np.floor(self.secs / 60))
        secs = self.secs % 60
        tmp = ""
        if secs < 10:
            tmp += "0"

        tmp += str(secs)
        self.gameTimer.setText("0" + str(mins) + ":" + tmp)
        self.secs += 1

        if not self.gameEnded:
            QTimer.singleShot(1000, self.setTimer)
        
    def playAgain(self):
        self.errors = np.array([0, 0, 0])
        self.examplesLength = np.array([0, 0, 0])
        self.timeForExample = np.array([0, 0, 0])

        self.gameEnded = False
        self.secs = 0
        self.initGameUI()
        self.initMenuUI()
        self.window.setCurrentWidget(self.menu)
      
app = Application()