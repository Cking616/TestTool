# -*- coding: utf-8 -*-

"""
@version: 1.0
@license: Apache Licence 
@author:  kht,cking616
@contact: cking616@mail.ustc.edu.cn
@software: PyCharm Community Edition
@file: serial_thread
@time: 2018/6/3
"""
import threading
import serial
import time


def int32(x):
    if x > 0xFFFFFFFF:
        raise OverflowError
    elif x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
        if x < 2147483648:
            return -x
        else:
            return -2147483648
    return x


class SdvBoard:
    def __init__(self, _port, _baud):
        self.PD4_encoder = [0, 0, 0, 0]
        self.BLDC_encoder = 0
        self.BLDC_flag = 0
        self.PD4_flag = [0, 0, 0, 0]
        self.com_port = serial.Serial(port=_port, baudrate=_baud, bytesize=8, stopbits=1, timeout=2)
        self._tmp_buf = []
        self._cmd_start = False
        self._cur = 0
        self._cmd_len = 0
        self._tick = 0
        self.wheel_real_time = False
        self.pd4_real_time = False
        self.bStarted = False

    def _parse_cmd(self):
        cmd = self._tmp_buf[1]
        if cmd == 0x26:
            self.bStarted = True
            print("System Start")
        elif cmd == 0x25:
            self.PD4_flag[0] = self._tmp_buf[2]
            self.PD4_flag[1] = self._tmp_buf[3]
            self.PD4_flag[2] = self._tmp_buf[4]
            self.PD4_flag[3] = self._tmp_buf[5]
            self.BLDC_flag = self._tmp_buf[6]
        elif cmd == 0x65:
            _id = self._tmp_buf[2]
            _buf = self._tmp_buf[3:7]
            self.PD4_encoder[_id - 1] = int.from_bytes(_buf, byteorder='little')
            self.PD4_encoder[_id - 1] = int32(self.PD4_encoder[_id - 1])
        elif cmd == 0x63:
            # print(self._tmp_buf)
            _buf = self._tmp_buf[2:6]
            self.BLDC_encoder = int.from_bytes(_buf, byteorder='little')
            self.BLDC_encoder = int32(self.BLDC_encoder)
        elif cmd == 0x3F:
            print("Cmd Error receive")
        else:
            print("Unknow cmd receive")
            print(self._tmp_buf)
        self._tmp_buf = []
        self._cur = 0
        self._cmd_start = False
        self._cmd_len = 0

    def timer_thread(self):
        self._tick = self._tick + 1
        num = self.com_port.in_waiting
        raw_cmd = self.com_port.read(num)
        for _rev in raw_cmd:
            if self._cmd_start:
                if self._cur == 0:
                    self._tmp_buf.append(_rev)
                    self._cur = self._cur + 1
                    self._cmd_len = _rev
                else:
                    self._tmp_buf.append(_rev)
                    self._cur = self._cur + 1
                    if self._cur == self._cmd_len:
                        self._parse_cmd()
            else:
                if _rev == 0x23:
                    self._cmd_start = True
        if self._tick == 3:
            if self.bStarted:
                self._read_wheel_encoder()
        if self._tick == 5:
            if self.bStarted:
                self._read_pd4_encoder(1)
                self._read_pd4_encoder(2)
                self._read_pd4_encoder(3)
                self._read_pd4_encoder(4)
            self._tick = 0

    def _send_cmd(self, cmd):
        cmd[0] = len(cmd)
        cmd.insert(0, 0x23)
        cmd = bytearray(cmd)
        # print(cmd)
        self.com_port.write(cmd)

    def _read_wheel_encoder(self):
        cmd = [0, 0x43, 0]
        self._send_cmd(cmd)

    def _read_pd4_encoder(self, node_id):
        cmd = [0, 0x45, node_id, 0]
        self._send_cmd(cmd)

    def stop_wheel(self):
        cmd = [0, 0x42, 0]
        self._send_cmd(cmd)

    def start_wheel(self, pos, speed, a):
        cmd = [0, 0x41, pos & 0xff, (pos & 0xff00) >> 8, (pos & 0xff0000) >> 16, (pos & 0xff000000) >> 24, speed, a]
        self._send_cmd(cmd)
        time.sleep(0.2)

    def get_wheel_encoder(self):
        return self.BLDC_encoder

    def get_pd4_encoder(self, node_id):
        return self.PD4_encoder[node_id - 1]

    def get_wheel_flag(self):
        return self.BLDC_flag

    def get_pd4_flag(self, node_id):
        return self.PD4_flag[node_id - 1]

    def is_start(self):
        return self.bStarted

    def set_pd4_speed(self, node_id, speed):
        cmd = [0, 0x46, node_id, speed & 0xff, (speed & 0xff00) >> 8,
               (speed & 0xff0000) >> 16, (speed & 0xff000000) >> 24]
        self._send_cmd(cmd)
        time.sleep(0.2)

    def start_pd4_motor(self, node_id, pos):
        cmd = [0, 0x44, node_id, pos & 0xff, (pos & 0xff00) >> 8,
               (pos & 0xff0000) >> 16, (pos & 0xff000000) >> 24]
        self._send_cmd(cmd)
        time.sleep(0.2)

    def stop_pd4_pos(self, node_id):
        cmd = [0, 0x47, node_id]
        self._send_cmd(cmd)
        time.sleep(0.2)


class _Timer(threading.Thread):
    def __init__(self, interval, func):
        threading.Thread.__init__(self)
        self.interval = interval
        self.func = func
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.func()
        self.finished.set()


class LoopTimer(_Timer):
    def __init__(self, interval, func):
        _Timer.__init__(self, interval, func)

    def run(self):
        while True:
            if not self.finished.is_set():
                self.finished.wait(self.interval)
                self.func()
            else:
                break
