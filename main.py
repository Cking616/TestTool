# -*- coding: utf-8 -*-

"""
@version: 1.0
@license: Apache Licence 
@author:  kht,cking616
@contact: cking616@mail.ustc.edu.cn
@software: PyCharm Community Edition
@file: main.py
@time: 2018/6/3
"""

from serial_thread import SdvBoard, LoopTimer
import time

g_board = None


if __name__ == '__main__':
    g_board = SdvBoard('/dev/ttyUSB0', 115200)
    timer = LoopTimer(0.1, g_board.timer_thread)
    timer.start()
    while not g_board.is_start():
        time.sleep(1)
        print("Wait for system init!")
    while True:
        time.sleep(3)
        print("1.Speed:200 pluse / 10 ms,Target Position:300000,a: 1 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(300000, 200, 1)
        g_board.start_wheel(300000, 200, 1)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:200 pluse / 10 ms,Target Position:-300000,a: 4 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(-300000, 200, 4)
        g_board.start_wheel(-300000, 200, 4)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:220 pluse / 10 ms,Target Position:500000,a: 5 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(500000, 220, 5)
        g_board.start_wheel(500000, 220, 5)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:120 pluse / 10 ms,Target Position:300000,a: 1 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(300000, 120, 1)
        g_board.start_wheel(300000, 120, 1)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:180 pluse / 10 ms,Target Position:0,a: 3 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(0, 180, 3)
        g_board.start_wheel(0, 180, 3)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())
