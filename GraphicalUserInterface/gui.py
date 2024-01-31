# basic_window.py
# Import necessary modules
import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QScrollArea, QFrame, \
    QPushButton, QSizePolicy, QStackedLayout, QLineEdit, QComboBox
import gui
from color_wd import *
from PyQt5 import QtCore, QtGui
import bluetooth as ble
from multiprocessing import Process
from queue import Queue
from PyQt5.QtCore import QTimer, QEvent
from PyQt5.QtGui import QPixmap, QMovie
from queue import Queue
import numpy as np
import asyncio
import scipy.io.wavfile as wf
import soundfile
import pygame
import time
import os

RATE = 2500

class MainWindow(QMainWindow):
    def __init__(self, queue, ble_handle, app, device_list):
        super().__init__()  # create default constructor for QWidget
        self.mainlayout = QVBoxLayout()
        # self.mainlayout.setSpacing(0)

        self.movie_label = QLabel(self)
        self.movie = QMovie("assets/spinner.gif")
        self.layout = QStackedLayout()

        self.mainwidget = QWidget()

        self.scroll = QScrollArea()

        self.scrollwidget = QWidget()

        self.vbox = QVBoxLayout()
        self.firstwidget = QWidget()
        self.secondwidget = QWidget()
        self.ble = ble_handle
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.queue = queue
        self.app = app
        self.device_list = device_list

        self.window = self
        self.info_queue = Queue()

        self.initializeUI()

    def initializeUI(self):
        print(time.localtime())
        self.setGeometry(650, 200, 400, 300)  # H, V 650 200 400 300
        self.setFixedSize(390, 300)

        toplayout = QHBoxLayout()

        text_1 = QLabel(self)
        text_1.setText("Devices")
        text_1.setStyleSheet("font-weight: bold; font-family: Helvetica Neue; font-size: 11px;")
        text_1.move(10, 10)
        text_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignBaseline)
        text_1.setFixedHeight(15)

        self.movie.setScaledSize(QtCore.QSize(15, 15))
        self.movie_label.setMovie(self.movie)
        self.movie_label.setMaximumSize(self.movie.scaledSize())
        self.movie_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.movie_label.setAutoFillBackground(True)
        self.movie.setBackgroundColor(QtCore.Qt.GlobalColor.white)
        self.movie_label.hide()
        self.movie.start()

        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setStyleSheet("color : rgb(221, 221, 221);")
        h_line.setLineWidth(1)

        self.app.focusChanged.connect(self.focusChanged)

        toplayout.addWidget(text_1)
        toplayout.addWidget(self.movie_label)

        self.mainlayout.addLayout(toplayout)

        self.mainlayout.addWidget(h_line)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.mainlayout.addWidget(self.scroll)

        self.DDline = QFrame()
        self.DDline.setFrameShape(QFrame.HLine)
        self.DDline.setLineWidth(1)
        #self.mainlayout.addWidget(self.DDline)

        self.firstwidget.setLayout(self.mainlayout)

        # self.firstwidget = self.scroll

        self.layout.addWidget(self.firstwidget)
        self.layout.addWidget(self.secondwidget)
        self.layout.setCurrentIndex(0)

        self.mainwidget.setLayout(self.layout)
        self.setCentralWidget(self.mainwidget)
        # self.centralWidget().setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        # self.centralWidget().resize(500,500)

        self.vbox.addStretch()

        #Important
        #Changes the size of the Device Tabs.
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(0)

        toplayout.setContentsMargins(15, 4, 30, 2) #l t r b

        self.scrollwidget.setLayout(self.vbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)
        #self.scrollwidget.setMaximumWidth(100)


        #self.scrollwidget.setFixedHeight(48)
        self.scrollwidget.setContentsMargins(0, 0, 0, 0)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        '''
        self.scrollwidget.setMaximumHeight(48)
        self.scrollwidget.setContentsMargins(0, 0, 0, 0)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll.setStyleSheet("background-color : red;")
        '''

        self.show()
        self.poll_queue()

        #d_1 = {'name': 'BLE', 'uuid': '153E524C-B6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        #self.add_device(d_1)

        '''
        d_2 = {'name': 'CLE', 'uuid': '153E524C-C6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_2)
        d_3 = {'name': 'DLE', 'uuid': '153E524C-D6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_3)
        d_4 = {'name': 'ELE', 'uuid': '153E524C-E6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_4)
        d_5 = {'name': 'BLE', 'uuid': '153E524C-F6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_5)
        d_6 = {'name': 'CLE', 'uuid': '153E524C-G6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_6)
        d_7 = {'name': 'DLE', 'uuid': '153E524C-H6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_7)
        d_8 = {'name': 'ELE', 'uuid': '153E524C-K6FF-49AF-AB0F-A96758E7AE1E', 'status': False}
        self.add_device(d_8)
        '''

    def initDiscoveredDevices(self):
        self.DDwidget = QWidget()
        self.DDscroll = QScrollArea()
        self.DDbox = QVBoxLayout()

    def initsecondwidget(self):
        self.backbutton = QPushButton(self.secondwidget)
        self.backbutton.move(10, 10)
        self.backbutton.setStyleSheet("background-color: transparent;")
        self.backbutton.setFixedSize(80, 20)
        back_button_image = "assets/back_arrow.png"
        '''
        back_text = QLabel(self.backbutton)
        back_text.setText("Devices")
        back_text.setStyleSheet("color: rgb(0, 121.6, 254.7);")
        back_text.move(25, 3)
        '''
        try:
            with open(back_button_image):
                back_button = QLabel(self.backbutton)
                back_button_pixmap = QPixmap(back_button_image)
                back_button_pixmap = back_button_pixmap.scaled(20, 20, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                               # 50, 50
                                                               QtCore.Qt.TransformationMode.SmoothTransformation)
                back_button.setPixmap(back_button_pixmap)
                # self.backbutton.setIcon(QtGui.QIcon(back_button_image))
                back_button.move(9, 2)
        except FileNotFoundError:
            print("Image not found.")

        self.backbutton.clicked.connect(self.backbuttonclicked)

        self.device_info = self.info_queue.get()
        self.name = self.device_info.get("name")
        print(self.name)

        self.title = QLabel(self.secondwidget)
        self.title.setText(str(self.name))
        self.title.setStyleSheet("font-family: Helvetica Neue; font-size: 13px;")
        self.title.move(185, 15)  # h v
        self.title.setStyleSheet("font-weight: bold;")
        #self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.name_tag = QLabel(self.secondwidget)
        self.name_tag.setText("name")
        self.name_tag.move(90, 75)
        self.name = QLineEdit(self.secondwidget)
        self.name.move(130, 75)
        self.name.resize(100, 20)  # Change size of entry field

        duration_tag = QLabel(self.secondwidget)
        duration_tag.setText("duration")
        duration_tag.move(70, 110)

        duration_list = ["5", "10"]
        duration = QComboBox(self.secondwidget)
        duration.addItems(duration_list)
        duration.move(140, 110)
        duration.setFixedWidth(60)
        duration.currentTextChanged.connect(self.duration_changed)

        collect_button = QPushButton("Collect", self.secondwidget)
        collect_button.move(75, 200)
        collect_button.clicked.connect(self.collect)

        led_button = QPushButton("Led", self.secondwidget)
        led_button.move(225, 200)
        led_button.clicked.connect(self.led)

        play_button = QPushButton("Play", self.secondwidget)
        play_button.move(150, 200)
        play_button.clicked.connect(self.play)

        self.ind = 0
        self.list = []

    def backbuttonclicked(self):
        self.title.clear()
        self.layout.setCurrentIndex(0)

    def duration_changed(self, t):
        #Send signal to the Gatt Profile
        print("Text changed:", t)

    def collect(self):
        #os.remove("mic.txt")
        self.ble.notify(self.notif_handler)
        print("Collect")

    def notif_handler(self, sender, data):
        array = []
        for d in data:
            d = hex(d)
            array.append(d[2:])
        array = [x + y for x, y in zip(array[::2], array[1::2])]
        array = [self.binary_to_decimal(line) for line in array]
        array = [str(line) + '\n' for line in array]
        array = [float(line) for line in array]
        for line in array:
            self.list.append(line)

    def binary_to_decimal(self, line):
        if int(line, 16) & 0b00000000000000001000000000000000:
            line = - (int(line, 16) & 0b00000000000000000111111111111111)
            line = line / 32767
            #print(line)
        else:
            line = int(line, 16) & 0b00000000000000000111111111111111
            line = line / 32767
            #print(line)
        return line

    def led(self):
        print("led")
        self.ble.blinkLed()

    def play(self):
        arr = np.array(self.list)
        wf.write('test.wav', RATE, arr)
        data, samplerate = soundfile.read('test.wav')
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
        pygame.init()
        my_sound = pygame.mixer.Sound('new.wav')
        my_sound.play()
        duration = len(data) / samplerate
        print("play")
        self.ble.sleep(duration)

    def timer(self):
        print("Timed Out")

    def poll_queue(self):
        if not self.movie.state():
            self.movie_label.show()
            self.movie.start()
        if not self.queue.empty():
            device = self.queue.get()  # Divide The address into 2
            self.pack_device(device)
            if not self.queue.empty():
                self.poll_queue()
            self.movie.stop()
            self.movie_label.hide()

            QTimer.singleShot(3000, self.sleep)  # Halts Scanning for 3 seconds

        else:
            QTimer.singleShot(1000, self.poll_queue)

    def pack_device(self, device):
        present = False
        name = str(device)[38:]
        uuid = str(device)[:36]
        status = False
        device_info = dict(name=name, uuid=uuid, status=status)
        # Do not append or add device if already present
        for i in self.device_list:
            if i.get("uuid") == device_info.get("uuid"):
                present = True
        if not present:
            self.device_list.append(device_info)
            self.add_device(device_info)

    def sleep(self):
        self.ble.scan(8)
        self.poll_queue()

    def add_device(self, device_info):
        self.object = DeviceTab(device_info, self.ble, self.window, self.info_queue, self.app)
        #This line will have to be changed to add the device to the DDArea
        self.vbox.insertWidget(self.vbox.count() - 1, self.object)
        self.show()

    def add_discovered_device(self, device_info):
        pass

    def focusChanged(self, previous, present):
        if not (type(previous) == QScrollArea and type(present) == gui.DeviceTab):
            if not (type(previous) == gui.DeviceTab and type(present) == QScrollArea):
                if not (type(previous) == gui.DeviceTab and type(present) == QPushButton):
                    if not (type(previous) == QPushButton and type(present) == gui.DeviceTab):
                        if self.movie.state():  # if movie is playing
                            if self.movie_label.isVisible():
                                self.movie_label.hide()
                            else:
                                self.movie_label.show()


class DeviceTab(QPushButton):
    def __init__(self, device_info, ble_handle, window, info_queue, app):
        super().__init__()
        self.window = window
        self.ble = ble_handle

        self.device_info = device_info
        self.uuid = device_info.get("uuid")
        name = device_info.get("name")

        self.info_queue = info_queue

        self.app = app
        self.app.focusChanged.connect(self.focusChanged)
        self.focusOut = False
        self.focusIn = False

        self.logo_size = 16

        # self.setFixedSize(QtCore.QSize(342, 48)) #342 60
        self.setFixedSize(QtCore.QSize(390, 48))    #342 48
        self.setStyleSheet("background-color: transparent;")
        self.clicked.connect(self.buttonClicked)

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

        layout = QHBoxLayout()
        self.setLayout(layout)
        # layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        widget = QWidget()
        widget.setFixedHeight(50)

        image = "assets/bee.png"
        try:
            with open(image):
                bee_image = QLabel(widget)
                pixmap = QPixmap(image)
                pixmap = pixmap.scaled(40, 40, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,  # 50, 50
                                       QtCore.Qt.TransformationMode.SmoothTransformation)
                bee_image.setPixmap(pixmap)
                bee_image.move(5, -5)
        except FileNotFoundError:
            print("Image not found.")

        self.middle_up = QLabel(widget)
        self.middle_up.setText(str(name))
        self.middle_up.setStyleSheet("font-family: Helvetica Neue; font-size: 13px;")
        self.middle_up.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.middle_up.move(60, -3)
        self.middle_up.setFixedWidth(100)

        self.middle_down = QLabel(widget)
        self.middle_down.setText("Not Connected")
        self.middle_down.setStyleSheet("color : rgb(192, 192, 192); font-family: Helvetica Neue; font-size: 11px;")
        self.middle_down.setFixedSize(1000, 20)
        self.middle_down.move(60, 14)  # h v

        black_logo_image = "assets/settings_gray.png"
        try:
            with open(black_logo_image):
                self.right_logo = QLabel(widget)
                right_pixmap = QPixmap(black_logo_image)
                right_pixmap = right_pixmap.scaled(self.logo_size, self.logo_size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                   QtCore.Qt.TransformationMode.SmoothTransformation)
                self.right_logo.setPixmap(right_pixmap)
                self.right_logo.move(314, 4)  # h v
        except FileNotFoundError:
            print("Image not found.")

        #middle.addWidget(self.middle_up)
        #middle.addWidget(self.middle_down)

        layout.addWidget(widget)
        #layout.addWidget(self.right_logo)
        #self.right_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        #self.right_logo.setStyleSheet("background-color : red")

        self.right_logo.mousePressEvent = self.right_logo_clicked
        self.right_logo.setHidden(True)
        retain = QSizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.right_logo.setSizePolicy(retain)
        self.show()

    def right_logo_clicked(self, e):
        # switch to information widget
        self.info_queue.put(self.device_info)
        self.window.initsecondwidget()
        self.window.layout.setCurrentIndex(1)

    def buttonClicked(self):
        if not self.device_info.get("status"):
            self.ble.connect(self.uuid, self.update_connected)
            self.device_info["status"] = True

    def update_connected(self):
        self.middle_down.setText("Connected")

    def focusInEvent(self, e):
        self.focusIn = True

    def focusOutEvent(self, e):
        self.focusOut = True

    def enterEvent(self, e):
        self.right_logo.setHidden(False)
        pass

    def leaveEvent(self, e):
        self.right_logo.setHidden(True)

    def focusChanged(self, previous, present):
        if type(previous) == gui.DeviceTab and type(present) is type(None) and self.focusOut:
            self.setStyleSheet("background-color: rgb(220, 220, 220); border: none;")  # gray
            self.middle_down.setStyleSheet("color: rgb(192, 192, 192); font-family: Helvetica Neue; font-size: 11px;")
            self.middle_up.setStyleSheet("color: black;")
            self.focusOut = False

        elif type(previous) == gui.DeviceTab and type(present) is not type(None) and self.focusOut:
            self.setStyleSheet("background-color: transparent; border: none;")
            self.middle_down.setStyleSheet("color: rgb(192, 192, 192); font-family: Helvetica Neue; font-size: 11px;")
            self.middle_up.setStyleSheet("color: black;")

            black_logo_image = "assets/settings_gray.png"
            try:
                with open(black_logo_image):
                    right_pixmap = QPixmap(black_logo_image)
                    right_pixmap = right_pixmap.scaled(self.logo_size, self.logo_size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       QtCore.Qt.TransformationMode.SmoothTransformation)
                    self.right_logo.setPixmap(right_pixmap)
            except FileNotFoundError:
                print("Image not found.")
            self.focusOut = False

        if self.focusIn:
            self.setStyleSheet("background-color: rgb(0.1, 98.6, 225.4); border: none;")  # Blue
            self.middle_down.setStyleSheet("color: white; font-family: Helvetica Neue; font-size: 11px;")
            self.middle_up.setStyleSheet("color: white;")

            white_logo_image = "assets/settings_white.png"
            try:
                with open(white_logo_image):
                    right_pixmap = QPixmap(white_logo_image)
                    right_pixmap = right_pixmap.scaled(self.logo_size, self.logo_size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                       QtCore.Qt.TransformationMode.SmoothTransformation)
                    self.right_logo.setPixmap(right_pixmap)
            except FileNotFoundError:
                print("Image not found.")
            self.focusIn = False
