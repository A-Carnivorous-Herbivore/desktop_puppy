#!/usr/bin/python3


import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5 import *
from random import *
from PIL import Image

class gifLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        date = QDate.currentDate()
        print(date.toString())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if self.is_follow_mouse and Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

class testWindow(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(testWindow, self).__init__(parent)
        #self.setWindowFlag(int(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        self.setAutoFillBackground(False)
        self.playGIF('Resources/test.gif', False)
        self.showTrayMenu()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.is_running_action = False
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
            #self.movie.start()

    '''重载鼠标双击事件'''
    def mouseDoubleClickEvent(self, event):
        if not self.is_running_action:
            self.is_running_action = True
            self.movie.start()
        else:
            self.is_running_action = False
            self.movie.stop()

    '''重载鼠标移动事件'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    '''重载鼠标释放事件'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
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
        #self.label = QLabel(self)
        self.label = gifLabel(self)
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
        self.quitAction = QAction("Quit", self, triggered=self.quit)
        self.barkAction = QAction("Bark", self, triggered=self.bark)

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
