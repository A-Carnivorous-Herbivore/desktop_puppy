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
import socket
from PyQt5 import *
from random import *
from datetime import *
import requests

import json
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
        self.lockToCorner()
        '''First Timer'''
        self.firstTimerValue = 5000
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.responseTimer)
        '''Second Timer'''
        self.secondTimer = QTimer(self)
        self.secondTimer.timeout.connect(self.secondTimerResponse)
        self.direct = 1;
        # self.timerCall()
        '''Count-down Timer'''
        self.countDTimer = QTimer(self)
        self.countDTimer.timeout.connect(self.countDTimerResponse)
        '''使用地天气，疫情信息等'''
        # self.getIPInformation()
        # self.diseaseInfo()
        # self.information()

        self.is_running_action = True
        self.timer.start(self.firstTimerValue)
        # self.action_images = []
        # self.action_pointer = 1
        # self.action_max_len = 0
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.randomAct)
        # self.timer.start(500)

    # def showWindow(self):
    #     self.show()
    #
    # def hideWindow(self):
    #     self.hide()

    def lockToCorner(self):
        sizeInfo = QDesktopWidget().screenGeometry()
        self.horz = sizeInfo.width() - self.curWidth
        self.vert = sizeInfo.height() - self.curHeight
        self.move(self.horz, self.vert)

    def getIPInformation(self):
        send_url = "http://api.ipstack.com/check?access_key=22557fbf2c4e3657e6a194bac14ce8da"
        geo_req = requests.get(send_url)
        geo_json = json.loads(geo_req.text)
        self.latitude = geo_json['latitude']
        self.longitude = geo_json['longitude']
        self.city = geo_json['city']
        self.country = geo_json['country_name']
        #print(self.country)
        #self.country = geo_json['country']
        #print(self.country)
        #print(str(self.latitude)+" "+str(self.longitude)+ " "+self.city)
        #temp_url = "9d531ce76790e4d6030ab8d0ffdccdcd"
        #BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        #URL = BASE_URL + "q=" + "Hyderabad" + "&appid=" + temp_url
        #host = socket.gethostbyname(socket.gethostname())
        #data = requests.get("http://api.ipstack.com/" + host + "?access_key=" + "22557fbf2c4e3657e6a194bac14ce8da")
        #data = data.json()
        #lat = data['latitude']
        #lon = data['longitude']
        #print(lat)
        self.weather = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="+str(self.latitude)+"&lon="+str(self.longitude)+"&appid="+"5d48290001297c0b05a77ad26cbf3907")
        self.weather = self.weather.json()
        #print(weather)
        self.location = self.city
        self.description = self.weather['weather'][0]['description']
        temperature = self.weather['main']['temp']
        temperature -= 273.15
        self.temperature = int(temperature)
        # print(self.description)
        # print(self.temperature)
        # print(self.location)

    # def changeImage(self, path: str, lock: bool):
    #     self.label = QLabel(self)
    #     if not os.path.isfile(path=path):
    #         raise ValueError
    #     self.pixmap = QPixmap(path)
    #     self.label.setPixmap(self.pixmap)
    #     self.resize(self.curWidth, self.curHeight)
    #     if lock:
    #         self.lockToCorner()
        #response = requests.get(URL)
        #print(108)
        #data = response.json()
        #print(data)

    def diseaseInfo(self):
        disease = requests.get("https://api.covid19api.com/dayone/country/"+self.country+"/status/confirmed")
        disease = disease.json()
        self.totalCase = disease[len(disease)-1]["Cases"]
        self.increasedCase = self.totalCase - disease[len(disease)-2]["Cases"]
        print(self.increasedCase)
        #print(disease)

    '''重载鼠标单击事件'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            # self.mouse_drag_pos = event.globalPos() - self.pos()
            self.mouse_drag_x = event.globalX() - self.x()
            self.mouse_drag_y = event.globalY() - self.y()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.timer.stop()
            self.initX = self.x()

            #self.movie.start()

    '''重载鼠标双击事件'''
    def mouseDoubleClickEvent(self, event):
        if self.is_running_action:
            self.rest()
            self.is_running_action = False

    '''重载鼠标移动事件'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            #print(self.mouse_drag_pos.x())
            #print(event.globalX())
            #print(self.x())
            #event.globalX() - self.x()
            if self.x() < self.initX:
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
            tempX = event.globalX() - self.mouse_drag_x
            tempY = event.globalY() - self.mouse_drag_y
            if tempX > self.horz:
                tempX = self.horz
            elif tempX < 0:
                tempX = 0
            if tempY > self.vert:
                tempY = self.vert
            elif tempY < 0:
                tempY = 0
            # self.move(event.globalPos() - self.mouse_drag_pos)
            self.move(tempX, tempY)
            event.accept()

    '''重载鼠标释放事件'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.is_running_action = True
        self.timer.start(self.firstTimerValue)

    # def moveEvent(self, event):
    #     pass
    #     # print('moving')
    #     # if random.randint(0, 10) % 2:
    #     #     self.changeImage('shime1.png', False)
    #     #     print("case 1")
    #     # else:
    #     #     self.changeImage('shime4.png', False)
    #     #     print("case 2")
    #     # event.accept()



    # 右键打开context menu
    def contextMenuEvent(self, event):
        menu = self.menu
        action = menu.exec_(self.mapToGlobal(event.pos()))
        #pass

    # def randomAct(self):
    #     if not self.is_running_action:
    #         self.is_running_action = True
    #         # self.action_images = random.choice(self.pet_images)
    #         # self.action_max_len = len(self.action_images)
    #         self.action_pointer = 1
    #     self.runFrame()
    # '''完成动作的每一帧'''

    # def runFrame(self):
    #     if self.action_pointer == self.action_max_len:
    #         self.is_running_action = False
    #         # self.action_pointer = 0
    #         # self.action_max_len = 0
    #     print('shime' + str(self.action_pointer) + '.png')
    #     self.changeImage('shime' + str(self.action_pointer) + '.png', False)
    #     self.action_pointer += 1

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
        self.menu1 = QMenu()
        self.menu1.setTitle("Manage")
        # self.stopAction = QAction("Stop", self, triggered=self.stop)
        self.restAction = QAction("Rest", self, triggered=self.rest)
        self.hideAction = QAction("Hide", self, triggered=self.hide)
        self.showAction = QAction("Show", self, triggered=self.show)
        self.timerAction = QAction("Timer", self, triggered=self.setTime)
        self.quitAction = QAction("Quit", self, triggered=self.quit)
        self.infoAction = QAction("Info", self, triggered=self.info)
        self.barkAction = QAction("Bark", self, triggered=self.bark)

        self.menu.addAction(self.timerAction)
        self.menu.addAction(self.infoAction)
        self.menu1.addAction(self.restAction)
        # self.menu.addAction(self.stopAction)
        self.menu1.addAction(self.hideAction)
        self.menu1.addAction(self.showAction)
        self.menu1.addAction(self.barkAction)
        self.menu.addMenu(self.menu1)
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

    def info(self):
        self.infoWindow.show()

    # def stop(self):
    #     if not self.is_running_action:
    #         self.movie.stop()

    def rest(self):
        '''替换狗子图片为休息'''
        self.is_running_action = False
        self.movie = QMovie('Resources/rest.gif')
        self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
        self.label.setMovie(self.movie)
        self.resize(self.curWidth, self.curHeight)
        self.movie.start()
        self.lockToCorner()
        self.timer.stop()


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

    # def timerCall(self):
    #     # self.text.setText("Current time is "+timeDisplay)
    #     self.startTimer()

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
        if self.counter < 20:
            while not self.checkPos():
                self.deltaX = (random.random() * 10) - 5
                self.deltaY = (random.random() * 10) - 5
            self.move(int(self.x()-self.deltaX), int(self.y()-self.deltaY))
            self.counter += 1
        else:
            self.secondTimer.stop()
            self.startTimer()

    def checkPos(self):
        temp_x = self.x() - self.deltaX
        temp_y = self.y() - self.deltaY
        # sizeInfo = QDesktopWidget().screenGeometry()
        # horz = sizeInfo.width() - self.curWidth
        # vert = sizeInfo.height() - self.curHeight
        if temp_x>self.horz or temp_y>self.vert or temp_x<0 or temp_y<0:
            return False
        else:
            return True


    def countDTimerResponse(self):
        self.countDTimer.stop()
        self.bark()
        output = QMessageBox.about(self, "Break Time!", "Time for a walk")

    def information(self):
        self.infoWindow = QWidget()
        self.infoWindow.setWindowTitle("Information")
        '''time display'''
        label_t1 = QLabel("Current time is:")
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        label_t2 = QLabel(timeDisplay)
        '''Weather display'''
        label_w1 = QLabel("City: " + self.location)
        label_w2 = QLabel("Weather: " + self.description)
        label_w3 = QLabel("Temperature: " + str(self.temperature) + "℃")
        '''COVID display'''
        label_c1 = QLabel("COVID-19 Info")
        label_c2 = QLabel("Daily increase: " + str(self.increasedCase))
        label_c3 = QLabel("Total cases: " + str(self.totalCase))
        '''display info in infoWindow'''
        icon = QPushButton("OK")
        icon.clicked.connect(self.closeInfoWindow)
        layout = QGridLayout()
        layout.addWidget(label_t1,0,0)
        layout.addWidget(label_t2,1,0)
        layout.addWidget(label_w1,2,0)
        layout.addWidget(label_w2,3,0)
        layout.addWidget(label_w3,4,0)
        layout.addWidget(label_c1,5,0)
        layout.addWidget(label_c2,7,0)
        layout.addWidget(label_c3,8,0)
        layout.addWidget(icon,9,3)
        self.infoWindow.setLayout(layout)

        self.infoWindow.show()

    def closeInfoWindow(self):
        self.infoWindow.close()





if __name__ == '__main__':

    # print(Qt.FramelessWindowHint)
    app = QApplication(sys.argv)
    tW = testWindow()
    # tW.changeImage('shime1.png', True)
    tW.show()
    #print(tW.width(), tW.height())
    # for i in range(1, 30):
    #     tW.changeImage('shime' + str(i) + '.png', False)
    #     time.sleep(1)
    # # print(QDesktopWidget().screenGeometry())

    sys.exit(app.exec_())
