import os
import socket
import sys
import threading

import time

import pygame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, qApp, \
    QFileDialog
from PyQt5.uic import loadUiType
from mss import mss
from zlib import compress, decompress

from pynput import mouse, keyboard

main,_ =loadUiType('main.ui')
ipDialogui,_ =loadUiType('ipDialog.ui')
screenDialogui,_ =loadUiType('screenDialog.ui')

all_collections = []
all_address= []
WIDTH=1920
HEIGHT=1080



class ScreenDialog(QDialog,screenDialogui):
    def __init__(self,addr1,addr2,addr3,addr4):
        QDialog.__init__(self)

        self.addr1=addr1
        self.addr2=addr2
        self.addr3=addr3
        self.addr4=addr4
        self.setupUi(self)

        self.label_4.setText(str(self.addr1[0]))
        self.label_3.setText(str(self.addr2[0]))
        self.label_2.setText(str(self.addr3[0]))
        self.label.setText(str(self.addr4[0]))
        self.pushButton_14.clicked.connect(self.pc1)
        self.pushButton_13.clicked.connect(self.pc2)
        self.pushButton_12.clicked.connect(self.pc3)
        self.pushButton_11.clicked.connect(self.pc4)

    def pc1(self):
        self.close()
        pc=1
        return pc


    def pc2(self):
        self.close()
        pc=2
        return pc

    def pc3(self):
        self.close()
        pc=3
        return pc

    def pc4(self):
        self.close()
        pc=4
        return pc


class HelpDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(HelpDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel('Lab Control System')
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'tools.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 23.35.211.233232"))
        layout.addWidget(self.buttonBox)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        self.setLayout(layout)


class IpDialog(QDialog,ipDialogui):
    def __init__(self,host,port):
        QDialog.__init__(self)

        self.host=host
        self.port=port
        self.IP=socket.gethostbyname(host)
        self.setupUi(self)
        self.label.setText("Server Name: "+str(self.host))
        self.label_3.setText("IP Address: "+str(self.IP))
        self.label_2.setText("Port: "+str(self.port))

class MainApp(QMainWindow,main,ScreenDialog):
    EXIT_CODE_REBOOT = -123
    def __init__(self):
        QWidget.__init__(self)
        self.sock=None
        self.host=None
        self.port=None
        self.conn1=None
        self.addr1=None
        self.conn2=None
        self.addr2=None
        self.conn3=None
        self.addr3=None
        self.conn4=None
        self.addr4=None
        self.command=None
        self.comb = {'1': '!',
                     '2': '@',
                     '3': '#',
                     '4': '$',
                     '5': '%',
                     '6': '^',
                     '7': '&',
                     '8': '*',
                     '9': '(',
                     '0': ')',
                     '-': '_',
                     '=': '+',
                     '`': '~',
                     '\\': '|',
                     '[': '{',
                     ']': '}',
                     ';': ':',
                     "'": '"',
                     ',': '<',
                     '.': '>',
                     '/': '?'}
        self.num = 0
        self.cap_shift = False
        self.shift = False

        self.setupUi(self)
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        #self.setStyleSheet(style)
        self.handleButtons()


    def hideConnection(self):
        self.pushButton_11.hide()
        self.pushButton_12.hide()
        self.pushButton_13.hide()
        self.pushButton_14.hide()
        self.pushButton_15.hide()
        self.pushButton_16.hide()
        self.pushButton_25.hide()
        self.pushButton_26.hide()
        self.pushButton_27.hide()
        self.pushButton_28.hide()
        self.pushButton_29.hide()
        self.pushButton_30.hide()
        self.pushButton_31.hide()
        self.pushButton_32.hide()
        self.pushButton_33.hide()
        self.pushButton_23.hide()
        self.pushButton_34.hide()
        self.pushButton_24.hide()

    def handleButtons(self):
        self.pushButton_7.clicked.connect(self.Show_IP_Address)
        self.pushButton.clicked.connect(self.Show_Help_Dialog)
        self.pushButton_5.clicked.connect(self.sleep_function)
        self.pushButton_4.clicked.connect(self.restart_function)
        self.pushButton_3.clicked.connect(self.power_off_function)
        self.pushButton_18.clicked.connect(self.serverStart)
        self.pushButton_20.clicked.connect(self.clientConnections)
        self.pushButton_5.clicked.connect(self.sleep_function)
        self.pushButton_4.clicked.connect(self.restart_function)
        self.pushButton_3.clicked.connect(self.power_off_function)
        self.pushButton_8.clicked.connect(self.file_share_function)
        self.pushButton_9.clicked.connect(self.ScreenShare)
        self.pushButton_10.clicked.connect(self.screen_view)
        self.pushButton_2.clicked.connect(self.remote_controlling)
        self.pushButton_17.clicked.connect(self.server_exit)
        self.pushButton_21.clicked.connect(self.server_restart)



    def serverStart(self):
        self.sock = socket.socket()
        self.host=socket.gethostname()
        #self.host = '127.0.0.1'
        self.port = 8080
        self.label_8.setText("Server Name: "+self.host)
        self.label_7.setText("Port: "+str(self.port))
        self.label_9.setText(self.host+"  "+str(self.port))


    def Show_IP_Address(self):
        dlg = IpDialog(self.host,self.port)
        dlg.exec_()

    def Show_Help_Dialog(self):
        dlg = HelpDialog()
        dlg.exec_()


    def clientConnections(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(4)
        self.conn1, self.addr1 = self.sock.accept()
        self.conn2, self.addr2 = self.sock.accept()
        self.conn3, self.addr3 = self.sock.accept()
        self.conn4, self.addr4 = self.sock.accept()

        self.str1 = self.label_9.text()
        self.label_9.setText(self.str1 + "\n"+ str(self.addr1[0]))
        self.pushButton_11.setEnabled(True)
        self.label.setEnabled(True)
        self.label.setText(str(self.addr1[0]))

        self.str1 = self.label_9.text()
        self.label_9.setText(self.str1 + "\n" + str(self.addr2[0]))
        self.pushButton_12.setEnabled(True)
        self.label_2.setEnabled(True)
        self.label_2.setText(str(self.addr2[0]))

        self.str1 = self.label_9.text()
        self.label_9.setText(self.str1 + "\n" + str(self.addr3[0]))
        self.pushButton_13.setEnabled(True)
        self.label_3.setEnabled(True)
        self.label_3.setText(str(self.addr3[0]))

        self.str1 = self.label_9.text()
        self.label_9.setText(self.str1 + "\n" + str(self.addr4[0]))
        self.pushButton_14.setEnabled(True)
        self.label_4.setEnabled(True)
        self.label_4.setText(str(self.addr4[0]))

    def power_off_function(self):
        self.command = 'shutdown'
        self.conn1.send(self.command.encode())
        self.conn2.send(self.command.encode())
        self.conn3.send(self.command.encode())
        self.conn4.send(self.command.encode())

    def restart_function(self):
        self.command = 'restart'
        self.conn1.send(self.command.encode())
        self.conn2.send(self.command.encode())
        self.conn3.send(self.command.encode())
        self.conn4.send(self.command.encode())

    def sleep_function(self):
        self.command = 'sleep'
        self.conn1.send(self.command.encode())
        self.conn2.send(self.command.encode())
        self.conn3.send(self.command.encode())
        self.conn4.send(self.command.encode())

    def retreive_screenshot(self):
        try:
            with mss() as sct:
                # The region to capture
                rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

                while 'recording':
                    # Capture the screen
                    img = sct.grab(rect)
                    # Tweak the compression level here (0-9)
                    pixels = compress(img.rgb, 6)

                    # Send the size of the pixels length
                    size = len(pixels)
                    size_len = (size.bit_length() + 7) // 8
                    self.conn1.send(bytes([size_len]))
                    self.conn2.send(bytes([size_len]))
                    self.conn3.send(bytes([size_len]))
                    self.conn4.send(bytes([size_len]))

                    # Send the actual pixels length
                    size_bytes = size.to_bytes(size_len, 'big')
                    self.conn1.send(size_bytes)
                    self.conn2.send(size_bytes)
                    self.conn3.send(size_bytes)
                    self.conn4.send(size_bytes)

                    # Send pixels
                    self.conn1.sendall(pixels)
                    self.conn2.sendall(pixels)
                    self.conn3.sendall(pixels)
                    self.conn4.sendall(pixels)
                    #time.sleep(10)
        finally:
            pass

    def RetrFile(self,name,conn,fileName,file):
        if os.path.isfile(fileName):
            conn.send(('EXISTS ' + str(os.path.getsize(fileName))).encode())
            conn.send(str(file).encode())
            userResponse = conn.recv(1024)
            userResponse = userResponse.decode()
            if userResponse[:2] == 'OK':
                with open(fileName, 'rb') as f:
                    bytesTosend = f.read(1024)
                    conn.send(bytesTosend)
                    while bytesTosend != '':
                        bytesTosend = f.read(1024)
                        conn.send(bytesTosend)

    def file_share_function(self):
        self.command = 'file_share'
        self.conn1.send(self.command.encode())
        self.conn2.send(self.command.encode())
        self.conn3.send(self.command.encode())
        self.conn4.send(self.command.encode())
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

        list=str(fileName).split('/')
        file=list[-1]

        t1 = threading.Thread(target=self.RetrFile, args=('retrThread', self.conn1,fileName,file))
        t1.start()

        t2 = threading.Thread(target=self.RetrFile, args=('retrThread1', self.conn2,fileName,file))
        t2.start()

        t3 = threading.Thread(target=self.RetrFile, args=('retrThread', self.conn3,fileName,file))
        t3.start()

        t4 = threading.Thread(target=self.RetrFile, args=('retrThread1', self.conn4,fileName,file))
        t4.start()

        self.str1 = self.label_9.text()
        self.label_9.setText(self.str1 + "\n" +"File Share Complete.")


    def ScreenShare(self):
        self.command='screen_share'
        self.conn1.send(self.command.encode())
        self.conn2.send(self.command.encode())
        self.conn3.send(self.command.encode())
        self.conn4.send(self.command.encode())

        self.retreive_screenshot()

    def recvall(self,conn, length):
        buf = b''
        while len(buf) < length:
            data = conn.recv(length - len(buf))

            if not data:
                return data
            buf += data
        return buf

    def remote_view(self,conn):
        size = (WIDTH, HEIGHT)
        pygame.init()
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        watching = True
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break

            size_len = int.from_bytes(conn.recv(1), byteorder='big')
            size = int.from_bytes(conn.recv(size_len), byteorder='big')
            pixels = decompress(self.recvall(conn, size))

            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            if watching:
                conn.send('ok'.encode())
                #print("ok")
            else:
                conn.send('no'.encode())
                #print('no')

    pygame.quit()



    def screen_view(self):
        screen = ScreenDialog(self.addr1,self.addr2,self.addr3,self.addr4)
        a=screen.pc1()
        screen.exec_()
        self.command = 'remote_view'
        if a==1:
            self.conn1.send(self.command.encode())
            self.remote_view(self.conn1)
            print("Hello")
            self.sock.listen(1)
            self.conn1, self.addr1 = self.sock.accept()
        elif a==2:
            self.conn2.send(self.command.encode())
            self.remote_view(self.conn2)
            print("Hello")
            self.sock.listen(1)
            self.conn2, self.addr2 = self.sock.accept()
        elif a==3:
            self.conn3.send(self.command.encode())
            self.remote_view(self.conn3)
            print("Hello")
            self.sock.listen(1)
            self.conn3, self.addr3 = self.sock.accept()
        elif a==4:
            self.conn4.send(self.command.encode())
            self.remote_view(self.conn4)
            print("Hello")
            self.sock.listen(1)
            self.conn4, self.addr4 = self.sock.accept()

    def recv_img(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (1366, 768)
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        pygame.init()
        screen = pygame.display.set_mode((1366, 768), pygame.NOFRAME)
        clock = pygame.time.Clock()
        watching = True
        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break
                    else:
                        pass

                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(self.conn1.recv(1), byteorder='big')
                size = int.from_bytes(self.conn1.recv(size_len), byteorder='big')
                pixels = decompress(self.recvall(self.conn1,size))

                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                '''img_display = QPixmap('img1.png')
                hello.window.setPixmap(img_display)
                hello.window.setScaledContents(True)
                hello.window.update()'''

                # os.remove('img1.png')

                # Display the picture
                #screen.blit(img, (0, 0))
                screen.blit(pygame.transform.scale(img, (1366, 768)), (0, 0))
                pygame.display.flip()
                clock.tick(60)
        finally:
            pass
    def event_listener(self):
        """Listens for commands committed on the computer and calls relevant functions"""
        listener_keyboard = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        listener_mouse = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        listener_mouse.start()
        listener_keyboard.start()
        listener_keyboard.join()
        listener_mouse.join()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.conn1.send("left pressed".encode())
        elif button == mouse.Button.left:
            self.conn1.send("left released".encode())
        elif button == mouse.Button.right and pressed:
            self.conn1.send("right pressed".encode())
        else:
            self.conn1.send("right released".encode())
    def on_move(self, x, y):
        cords = (x, y)
        string1 = str(int(x * 1.41)) + " " + str(int(y * 1.41))
        # time.sleep(0.1)
        if self.num == 10:
            self.conn1.send(string1.encode())
            self.num = 0
        else:
            self.num += 1

    def on_scroll(self, x, y, dx, dy):
        if dy == 1:
            self.conn1.send("up".encode())
        elif dy == -1:
            self.conn1.send("down".encode())
        elif dx == 1:
            self.conn1.send("rig2".encode())
        elif dx == -1:
            self.conn1.send("lef2".encode())

    def on_press(self, key):
        """Filters keyboard presses, sends the customer which key to press"""
        if 'shift' in str(key) and (not self.shift):
            self.shift = True

        elif self.shift and ('Key' not in str(key)) and (str(key)[1] in self.comb):
            key = self.comb[str(key)[1]]
            key1 = 'press: ' + str(key)
            self.conn1.send(key1.encode())

        elif self.cap_shift and ('Key' not in str(key)):
            key = str(key)[1].upper()
            key1 = 'press: ' + str(key)
            self.conn1.send(key1.encode())

        elif 'shift' not in str(key):
            key1 = 'press: ' + str(key)
            self.conn1.send(key1.encode())

    def on_release(self, key):
        """Filters keyboard releases, sends the customer which key to releases"""
        if 'caps_lock' in str(key) and (not self.cap_shift):
            self.cap_shift = True
        elif 'caps_lock' in str(key) and self.cap_shift:
            self.cap_shift = False

        if self.shift and 'alt_l' in str(key):
            self.conn1.send("change_lang".encode())

        if 'shift' in str(key) and self.shift:
            self.shift = False
        elif 'shift' not in str(key):
            key1 = "release: " + str(key)
            self.conn1.send(key1.encode())


    def event_listener2(self):
        """Listens for commands committed on the computer and calls relevant functions"""
        listener_keyboard = keyboard.Listener(
            on_press=self.on_press2,
            on_release=self.on_release2)

        listener_mouse = mouse.Listener(
            on_move=self.on_move2,
            on_click=self.on_click2,
            on_scroll=self.on_scroll2)

        listener_mouse.start()
        listener_keyboard.start()
        listener_keyboard.join()
        listener_mouse.join()

    def on_click2(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.conn2.send("left pressed".encode())
        elif button == mouse.Button.left:
            self.conn2.send("left released".encode())
        elif button == mouse.Button.right and pressed:
            self.conn2.send("right pressed".encode())
        else:
            self.conn2.send("right released".encode())

    def on_move2(self, x, y):
        cords = (x, y)
        string1 = str(int(x * 1.41)) + " " + str(int(y * 1.41))
        # time.sleep(0.1)
        if self.num == 10:
            self.conn2.send(string1.encode())
            self.num = 0
        else:
            self.num += 1

    def on_scroll2(self, x, y, dx, dy):
        if dy == 1:
            self.conn2.send("up".encode())
        elif dy == -1:
            self.conn2.send("down".encode())
        elif dx == 1:
            self.conn2.send("rig2".encode())
        elif dx == -1:
            self.conn2.send("lef2".encode())

    def on_press2(self, key):
        """Filters keyboard presses, sends the customer which key to press"""
        if 'shift' in str(key) and (not self.shift):
            self.shift = True

        elif self.shift and ('Key' not in str(key)) and (str(key)[1] in self.comb):
            key = self.comb[str(key)[1]]
            key1 = 'press: ' + str(key)
            self.conn2.send(key1.encode())

        elif self.cap_shift and ('Key' not in str(key)):
            key = str(key)[1].upper()
            key1 = 'press: ' + str(key)
            self.conn2.send(key1.encode())

        elif 'shift' not in str(key):
            key1 = 'press: ' + str(key)
            self.conn2.send(key1.encode())

    def on_release2(self, key):
        """Filters keyboard releases, sends the customer which key to releases"""
        if 'caps_lock' in str(key) and (not self.cap_shift):
            self.cap_shift = True
        elif 'caps_lock' in str(key) and self.cap_shift:
            self.cap_shift = False

        if self.shift and 'alt_l' in str(key):
            self.conn2.send("change_lang".encode())

        if 'shift' in str(key) and self.shift:
            self.shift = False
        elif 'shift' not in str(key):
            key1 = "release: " + str(key)
            self.conn2.send(key1.encode())


    def event_listener3(self):
        """Listens for commands committed on the computer and calls relevant functions"""
        listener_keyboard = keyboard.Listener(
            on_press=self.on_press3,
            on_release=self.on_release3)

        listener_mouse = mouse.Listener(
            on_move=self.on_move3,
            on_click=self.on_click3,
            on_scroll=self.on_scroll3)

        listener_mouse.start()
        listener_keyboard.start()
        listener_keyboard.join()
        listener_mouse.join()

    def on_click3(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.conn3.send("left pressed".encode())
        elif button == mouse.Button.left:
            self.conn3.send("left released".encode())
        elif button == mouse.Button.right and pressed:
            self.conn3.send("right pressed".encode())
        else:
            self.conn3.send("right released".encode())
    def on_move3(self, x, y):
        cords = (x, y)
        string1 = str(int(x * 1.41)) + " " + str(int(y * 1.41))
        # time.sleep(0.1)
        if self.num == 10:
            self.conn3.send(string1.encode())
            self.num = 0
        else:
            self.num += 1

    def on_scroll3(self, x, y, dx, dy):
        if dy == 1:
            self.conn3.send("up".encode())
        elif dy == -1:
            self.conn3.send("down".encode())
        elif dx == 1:
            self.conn3.send("rig2".encode())
        elif dx == -1:
            self.conn3.send("lef2".encode())

    def on_press3(self, key):
        """Filters keyboard presses, sends the customer which key to press"""
        if 'shift' in str(key) and (not self.shift):
            self.shift = True

        elif self.shift and ('Key' not in str(key)) and (str(key)[1] in self.comb):
            key = self.comb[str(key)[1]]
            key1 = 'press: ' + str(key)
            self.conn3.send(key1.encode())

        elif self.cap_shift and ('Key' not in str(key)):
            key = str(key)[1].upper()
            key1 = 'press: ' + str(key)
            self.conn3.send(key1.encode())

        elif 'shift' not in str(key):
            key1 = 'press: ' + str(key)
            self.conn3.send(key1.encode())

    def on_release3(self, key):
        """Filters keyboard releases, sends the customer which key to releases"""
        if 'caps_lock' in str(key) and (not self.cap_shift):
            self.cap_shift = True
        elif 'caps_lock' in str(key) and self.cap_shift:
            self.cap_shift = False

        if self.shift and 'alt_l' in str(key):
            self.conn3.send("change_lang".encode())

        if 'shift' in str(key) and self.shift:
            self.shift = False
        elif 'shift' not in str(key):
            key1 = "release: " + str(key)
            self.conn3.send(key1.encode())

    def event_listener4(self):
        """Listens for commands committed on the computer and calls relevant functions"""
        listener_keyboard = keyboard.Listener(
            on_press=self.on_press4,
            on_release=self.on_release4)

        listener_mouse = mouse.Listener(
            on_move=self.on_move4,
            on_click=self.on_click4,
            on_scroll=self.on_scroll4)

        listener_mouse.start()
        listener_keyboard.start()
        listener_keyboard.join()
        listener_mouse.join()

    def on_click4(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.conn4.send("left pressed".encode())
        elif button == mouse.Button.left:
            self.conn4.send("left released".encode())
        elif button == mouse.Button.right and pressed:
            self.conn4.send("right pressed".encode())
        else:
            self.conn4.send("right released".encode())
    def on_move3(self, x, y):
        cords = (x, y)
        string1 = str(int(x * 1.41)) + " " + str(int(y * 1.41))
        # time.sleep(0.1)
        if self.num == 10:
            self.conn4.send(string1.encode())
            self.num = 0
        else:
            self.num += 1

    def on_scroll4(self, x, y, dx, dy):
        if dy == 1:
            self.conn4.send("up".encode())
        elif dy == -1:
            self.conn4.send("down".encode())
        elif dx == 1:
            self.conn4.send("rig2".encode())
        elif dx == -1:
            self.conn4.send("lef2".encode())

    def on_press4(self, key):
        """Filters keyboard presses, sends the customer which key to press"""
        if 'shift' in str(key) and (not self.shift):
            self.shift = True

        elif self.shift and ('Key' not in str(key)) and (str(key)[1] in self.comb):
            key = self.comb[str(key)[1]]
            key1 = 'press: ' + str(key)
            self.conn4.send(key1.encode())

        elif self.cap_shift and ('Key' not in str(key)):
            key = str(key)[1].upper()
            key1 = 'press: ' + str(key)
            self.conn4.send(key1.encode())

        elif 'shift' not in str(key):
            key1 = 'press: ' + str(key)
            self.conn4.send(key1.encode())

    def on_release4(self, key):
        """Filters keyboard releases, sends the customer which key to releases"""
        if 'caps_lock' in str(key) and (not self.cap_shift):
            self.cap_shift = True
        elif 'caps_lock' in str(key) and self.cap_shift:
            self.cap_shift = False

        if self.shift and 'alt_l' in str(key):
            self.conn4.send("change_lang".encode())

        if 'shift' in str(key) and self.shift:
            self.shift = False
        elif 'shift' not in str(key):
            key1 = "release: " + str(key)
            self.conn4.send(key1.encode())



    def remote_controlling(self):
        screen = ScreenDialog(self.addr1,self.addr2,self.addr3,self.addr4)
        a = screen.pc1()
        screen.exec_()
        self.command='remote_controlling'
        if a == 1:
            self.conn1.send(self.command.encode())
            recv_img_thread=threading.Thread(target=self.recv_img )
            recv_img_thread.start()
            try:
                self.event_listener()
            finally:
                pass
            recv_img_thread.join()
        elif a == 2:
            self.conn2.send(self.command.encode())
            recv_img_thread = threading.Thread(target=self.recv_img1,)
            recv_img_thread.start()
            try:
                self.event_listener2()
            finally:
                pass
            recv_img_thread.join()
        elif a == 3:
            self.conn3.send(self.command.encode())
            recv_img_thread = threading.Thread(target=self.recv_img, args=(self.conn3))
            recv_img_thread.start()
            try:
                self.event_listener3()
            finally:
                pass
            recv_img_thread.join()
        else:
            self.conn4.send(self.command.encode())
            recv_img_thread = threading.Thread(target=self.recv_img, args=(self.conn4))
            recv_img_thread.start()
            try:
                self.event_listener4()
            finally:
                pass
            recv_img_thread.join()

    def server_exit(self):
        self.sock.close()
        app.exec_()

    def server_restart(self):
        self.sock.close()
        qApp.exit(MainApp.EXIT_CODE_REBOOT)



def main():
    currentExitCode = MainApp.EXIT_CODE_REBOOT
    while currentExitCode == MainApp.EXIT_CODE_REBOOT:
        app=QApplication(sys.argv)
        window=MainApp()
        window.show()
        currentExitCode=app.exec_()
        app=None


if __name__ == '__main__':
    main()