import threading
import time
import sys
import os
import socket

import pyautogui
import pygame
from mss import mss
from threading import Thread
from zlib import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def retreive_screenshot(sock):
    flag=True
    count=0
    try:
        with mss() as sct:
            rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

            while flag:

                img = sct.grab(rect)
                pixels = compress(img.rgb, 6)

                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                sock.send(bytes([size_len]))

                size_bytes = size.to_bytes(size_len, 'big')
                sock.send(size_bytes)

                sock.sendall(pixels)
                #time.sleep(0.001)
                test = sock.recv(1024)
                test = test.decode()
                if test == 'no':
                    #print('Hello')
                    flag = 0
                    break
    finally:
        sock.close()


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))

        if not data:
            return data
        buf += data
    return buf


def event_filter():
    """Filters commands sent by the handler and executes them"""
    while 1:
        data = sock.recv(1024)
        data = data.decode()
        if "right" in data and "pressed" in data:
            pyautogui.mouseDown(button='right')

        elif "right" in data and "released" in data:
            pyautogui.mouseUp(button='right')

        elif "left" in data and "pressed" in data:
            pyautogui.mouseDown(button='left')

        elif "left" in data and "released" in data:
            pyautogui.mouseUp(button='left')

        elif "up" in data:
            pyautogui.scroll(175)
        elif "down" in data:
            pyautogui.scroll(-175)
        elif "rig2" in data:
            pyautogui.hscroll(175)
        elif "lef2" in data:
            pyautogui.hscroll(-175)
        elif "change_lang" in data:
            pyautogui.hotkey('shift', 'altleft')
        elif "press:" in data:
            if 'Key' in data:
                pyautogui.keyDown(data[data.find('.') + 1:])
            else:
                pyautogui.keyDown(data[data.find(':') + 3])
        elif "release:" in data:
            if 'Key' in data:
                pyautogui.keyUp(data[data.find('.') + 1:])
            else:
                pyautogui.keyUp(data[data.find(':') + 3])
        else:
            x, y = data.split(' ')
            x = int(x)
            y = int(y)
            pyautogui.moveTo(x, y)

def run(conn):
    """Calls 2 functions necessary to the customer's functioning, start_work via thread and event_filter"""
    work_thread = threading.Thread(target=retreive_screenshot, args=(conn,))
    work_thread.start()
    event_filter()
    work_thread.join()


if __name__ == '__main__':
    # app=QApplication(sys.argv)
    # app.setApplicationName('Lab Control System')
    WIDTH = 1920
    HEIGHT = 1080
    pyautogui.FAILSAFE=False
    sock = socket.socket()
    # host=input('Server pc name:')
    host = 'Sojib-pc'
    port = 8080
    sock.connect((host, port))
    print('connect to server')
    while True:
        command = sock.recv(1024)
        command = command.decode()
        print(command)

        if command == "shutdown":
            os.system('shutdown.bat')
        elif command == 'restart':
            os.system('restart.bat')
        elif command == "sleep":
            os.system('sleep.bat')
        elif command == 'file_share':
            data = sock.recv(1024)
            data = data.decode()
            filename=sock.recv(1024)
            filename=filename.decode()

            if data[:6] == "EXISTS":
                filesize = int(data[7:])

                sock.send("OK".encode())
                f = open(filename, 'wb')
                data = sock.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = sock.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                f.close()
                print('Download Complete')

            else:
                print("File does not Exits")
        elif command == "screen_share":
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
            clock = pygame.time.Clock()
            watching = True

            try:
                while watching:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            watching = False
                            break

                    size_len = int.from_bytes(sock.recv(1), byteorder='big')
                    size = int.from_bytes(sock.recv(size_len), byteorder='big')
                    pixels = decompress(recvall(sock, size))

                    img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), "RGB")

                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)

            finally:
                pass

        elif command == 'remote_view':
            retreive_screenshot(sock)
            sock = socket.socket()
            sock.connect((host, port))
            print('connect to server')


        elif command =='remote_controlling':
            run(sock)











    # app.exec_()
