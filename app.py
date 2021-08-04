#!/usr/bin/python3


import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtGui import QMovie
from PyQt5 import *
from random import *
from datetime import *
import random
from PIL import Image

# class gifLabel(QLabel):
#     def __init__(self, *args, **kwargs):
#         QLabel.__init__(self, *args, **kwargs)
#
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.is_follow_mouse = True
#             self.mouse_drag_pos = event.globalPos() - self.pos()
#             event.accept()
#             self.setCursor(QCursor(Qt.OpenHandCursor))
#
#     def mouseMoveEvent(self, event):
#         if self.is_follow_mouse and Qt.LeftButton:
#             self.move(event.globalPos() - self.mouse_drag_pos)
#             event.accept()
#
#     def mouseReleaseEvent(self, event):
#         self.is_follow_mouse = False
#         self.setCursor(QCursor(Qt.ArrowCursor))



class testWindow(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(testWindow, self).__init__(parent)
        self.setWindowFlag(int(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        self.setAutoFillBackground(False)
        self.playGIF('Resources/test.gif', False)
        self.showTrayMenu()
        self.counter = 0
        self.boolIndicator = 0
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.is_running_action = False
        self.lockToCorner()
        '''First Timer'''
        self.firstTimerValue = 5000
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.responseTimer)
        '''Second Timer'''
        self.secondTimer = QTimer(self)
        self.secondTimer.timeout.connect(self.secondTimerResponse)
        self.direct = 1;
        self.timerCall()
        '''Count-down Timer'''
        self.countDTimer = QTimer(self)
        self.countDTimer.timeout.connect(self.countDTimerResponse)
        # self.is_running_action = False
        # self.action_images = []
        # self.action_pointer = 1
        # self.action_max_len = 0
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.randomAct)
        # self.timer.start(500)

    def showWindow(self):
        self.show()

    def hideWindow(self):
        self.hide()

    def lockToCorner(self):
        sizeInfo = QDesktopWidget().screenGeometry()
        horz = sizeInfo.width() - self.curWidth
        vert = sizeInfo.height() - self.curHeight
        self.move(horz, vert)

    def changeImage(self, path: str, lock: bool):
        self.label = QLabel(self)
        if not os.path.isfile(path=path):
            raise ValueError
        self.pixmap = QPixmap(path)
        self.label.setPixmap(self.pixmap)
        self.resize(self.curWidth, self.curHeight)
        if lock:
            self.lockToCorner()

    '''重载鼠标单击事件'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.timer.stop()
            self.initX = self.x()

            #self.movie.start()

    '''重载鼠标双击事件'''
    def mouseDoubleClickEvent(self, event):
        if not self.is_running_action:
            self.is_running_action = True
            self.movie.start()
            #self.moveEvent()
        else:
            self.is_running_action = False
            self.movie.stop()

    '''重载鼠标移动事件'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            #print(self.mouse_drag_pos.x())
            #print(event.globalX())
            #print(self.x())
            #event.globalX() - self.x()
            if  self.x() < self.initX:
                #self.direct = 1
                self.movie = QMovie('Resources/test.gif')
                self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
                self.label.setMovie(self.movie)
                self.resize(self.curWidth, self.curHeight)
                self.movie.start()
            elif self.x() > self.initX:
                #self.direct = 0
                self.movie = QMovie('Resources/mirrored.gif')
                self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
                self.label.setMovie(self.movie)
                self.resize(self.curWidth, self.curHeight)
                self.movie.start()
            self.initX = self.x()
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''重载鼠标释放事件'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.timer.start(self.firstTimerValue)

        #self.movie.stop()

    def moveEvent(self, event):
        pass
        # print('moving')
        # if random.randint(0, 10) % 2:
        #     self.changeImage('shime1.png', False)
        #     print("case 1")
        # else:
        #     self.changeImage('shime4.png', False)
        #     print("case 2")
        # event.accept()



    # 右键打开context menu
    def contextMenuEvent(self, event):
        menu = self.menu
        action = menu.exec_(self.mapToGlobal(event.pos()))
        #pass

    def randomAct(self):
        if not self.is_running_action:
            self.is_running_action = True
            # self.action_images = random.choice(self.pet_images)
            # self.action_max_len = len(self.action_images)
            self.action_pointer = 1
        self.runFrame()
    '''完成动作的每一帧'''

    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            # self.action_pointer = 0
            # self.action_max_len = 0
        print('shime' + str(self.action_pointer) + '.png')
        self.changeImage('shime' + str(self.action_pointer) + '.png', False)
        self.action_pointer += 1

    def playGIF(self, path: str, lock: bool):
        # with Image.open(path) as gif:
        #     gif.seek(0)
        #     width = gif.size[0]
        #     height = gif.size[1]
        self.curWidth = self.curHeight = 128
        if not os.path.isfile(path=path):
            raise ValueError
        self.label = QLabel(self)
        #self.label = gifLabel(self)
        self.movie = QMovie(path)
        self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
        self.label.setMovie(self.movie)
        # print(self.label.movie().isValid())

        self.resize(self.curWidth, self.curHeight)
        self.label.movie().start()
        if lock:
            self.lockToCorner()

    def showTrayMenu(self):
        self.menu = QMenu()
        self.stopAction = QAction("Stop", self, triggered=self.stop)
        self.restAction = QAction("Rest", self, triggered=self.rest)
        self.hideAction = QAction("Hide", self, triggered=self.hide)
        self.showAction = QAction("Show", self, triggered=self.show)
        self.timerAction = QAction("Timer", self, triggered=self.setTime)
        self.quitAction = QAction("Quit", self, triggered=self.quit)
        self.barkAction = QAction("Bark", self, triggered=self.bark)

        self.menu.addAction(self.timerAction)
        self.menu.addAction(self.restAction)
        self.menu.addAction(self.stopAction)
        self.menu.addAction(self.barkAction)
        self.menu.addAction(self.hideAction)
        self.menu.addAction(self.showAction)
        self.menu.addAction(self.quitAction)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('Resources/trayIcon_duck.png'))
        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def setTime(self):
        self.timeWindow = QWidget()
        self.timeWindow.setWindowTitle("Timer")
        genLabel = QLabel("Take a Break After: ")
        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        hourButton = QLabel("Hours")
        minuteButton = QLabel("Minutes")
        secondButton = QLabel("Second")
        finish = QPushButton("OK")
        layout = QGridLayout()
        layout.addWidget(genLabel,0,0)
        layout.addWidget(self.line1,1,0)
        layout.addWidget(hourButton,1,1)
        layout.addWidget(self.line2,2,0)
        layout.addWidget(minuteButton,2,1)
        layout.addWidget(self.line3,3,0)
        layout.addWidget(secondButton,3,1)
        layout.addWidget(finish,4,2)
        self.timeWindow.setLayout(layout)
        finish.clicked.connect(self.showDialog)

        self.timeWindow.show()

    def showDialog(self):
        cdHour = 0
        cdMin = 0
        cdSec = 0
        if self.line1.text() != '':
            cdHour = int(self.line1.text())
        if self.line2.text() != '':
            cdMin = int(self.line2.text())
        if self.line3.text() != '':
            cdSec = int(self.line3.text())
        reply = QMessageBox.information(self, "Timer Setup", "Start Alarm Clock",
                                        QMessageBox.Yes | QMessageBox.No)
        if reply:
            time = cdHour*3600 + cdMin*60 + cdSec
            self.countDTimer.start(time * 1000)
            self.timeWindow.close()
            # print(cdHour, cdMin, cdSec)


    def stop(self):
        if not self.is_running_action:
            self.movie.stop()

    def rest(self):
        self.movie.stop()
        self.lockToCorner()
        # 替换狗子图片为蹲坐（暂无图源）

    def hide(self):
        if not self.is_running_action:
            self.movie.stop()
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def quit(self):
        qApp.quit()
        sys.exit()

    def bark(self):
        QtMultimedia.QSound.play('Resources/bark.wav')

    def timerCall(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        '''display time in pop-up window'''
        time = QMessageBox.about(self, "Current Time", timeDisplay)
        
        # self.label.setText(timeDisplay)
        self.text = QLabel(self)
        # self.text.setText("Current time is "+timeDisplay)
        self.startTimer()

    def startTimer(self):
        self.timer.start(self.firstTimerValue)


    def responseTimer(self):
        self.counter = 0
        self.timer.stop()
        random.seed(datetime.now())
        self.deltaX = (random.random()*10) - 5
        self.deltaY = (random.random()*10) - 5
        #print(self.deltaX)

        if self.deltaX >= 0:
            print("To the left")
            #self.label = QLabel(self)
            self.movie = QMovie('Resources/test.gif')
            self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
            self.label.setMovie(self.movie)
            self.resize(self.curWidth, self.curHeight)
            self.movie.start()
        elif self.deltaX < 0:
            print("To the right")
            #self.label = QLabel(self)
            self.movie = QMovie('Resources/mirrored.gif')
            self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
            self.label.setMovie(self.movie)
            self.resize(self.curWidth, self.curHeight)
            self.movie.start()
        #print(self.deltaX)
        self.startTimer2()

    def startTimer2(self):
        #print(2)
        self.secondTimer.start(40)

    def secondTimerResponse(self):
        #print("timer2 counter" + self.counter)
        if self.counter < 20:
                 # print("timer2 update")
                self.move(int(self.x()-self.deltaX), int(self.y()-self.deltaY))
                self.counter += 1
        else:
           # print("timer1 update")
            self.secondTimer.stop()
            self.startTimer()

    def countDTimerResponse(self):
        self.countDTimer.stop()
        self.bark()
        output = QMessageBox.about(self, "Break Time!", "Time for a walk")







        



if __name__ == '__main__':

    # print(Qt.FramelessWindowHint)
    app = QApplication(sys.argv)
    tW = testWindow()
    # tW.changeImage('shime1.png', True)
    tW.show()
    print(tW.width(), tW.height())
    # for i in range(1, 30):
    #     tW.changeImage('shime' + str(i) + '.png', False)
    #     time.sleep(1)
    # # print(QDesktopWidget().screenGeometry())

    sys.exit(app.exec_())
