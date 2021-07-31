#!/usr/bin/python3


import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from random import *
from PIL import Image


class testWindow(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(testWindow, self).__init__(parent)
        self.setWindowFlag(int(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        self.setAutoFillBackground(False)
        self.playGIF('Resources/test.gif', False)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    '''鼠标移动, 则宠物也移动'''

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()
    '''鼠标释放时, 取消绑定'''

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

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
        self.movie = QMovie(path)
        self.movie.setScaledSize(QSize(self.curWidth, self.curHeight))
        self.label.setMovie(self.movie)
        # print(self.label.movie().isValid())

        self.resize(self.curWidth, self.curHeight)
        self.label.movie().start()
        self.lockToCorner()


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
