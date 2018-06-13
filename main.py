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
import threading

g_board = None


def test_loop():
    time.sleep(1)
    g_board.set_wheel_param(5, 1800)
    g_board.set_wheel_param(1, 37)
    g_board.set_wheel_param(2, 10)
    g_board.start_wheel(44000, 220, 4)
    g_board.start_wheel(44000, 220, 4)

def __test_loop():
    g_board.set_wheel_param(1, 32)
    g_board.set_wheel_param(2, 14)
    g_board.set_wheel_param(3, 14)
    g_board.set_wheel_param(5, 2040)
    while True:
        time.sleep(1)
        print("1.Speed:200 pluse / 10 ms,Target Position:300000,a: 1 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(30000, 220, 4)
        g_board.start_wheel(30000, 220, 4)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:200 pluse / 10 ms,Target Position:-300000,a: 4 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(0, 200, 4)
        g_board.start_wheel(0, 200, 4)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)

        print("2.Speed:120 pluse / 10 ms,Target Position:300000,a: 1 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(30000, 120, 6)
        g_board.start_wheel(30000, 120, 6)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())

        time.sleep(3)
        print("2.Speed:180 pluse / 10 ms,Target Position:0,a: 3 pulse/ 50 ms * 10 ms")
        g_board.start_wheel(0, 180, 6)
        g_board.start_wheel(0, 180, 6)
        time.sleep(0.5)

        while g_board.get_wheel_flag() != 0x11:
            print("Running,Current Encoder: ", g_board.get_wheel_encoder())
            time.sleep(2)
        time.sleep(2)
        print("End running,Current Encoder",g_board.get_wheel_encoder())


if __name__ == '__main__':
    g_board = SdvBoard('/dev/ttyUSB0', 115200)
    timer = LoopTimer(0.1, g_board.timer_thread)
    timer.start()
    g_board.power_on()
    while not g_board.is_start():
        time.sleep(1)
        print("Wait for system init!")
    # test_loop()
    workthread = threading.Thread(target = test_loop)
    workthread.start()
    input("Anything To Stop")
    g_board.power_off()
    import os
    os._exit(0)

