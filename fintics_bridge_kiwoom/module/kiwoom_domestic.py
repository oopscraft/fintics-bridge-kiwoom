# -*- coding: utf-8 -*-
import pythoncom
from PyQt5.QAxContainer import QAxWidget
from queue import Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from typing import List


class KiwoomDomestic(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ocx = None
        self.output_names = []
        self.response = False
        self.response_queue = Queue()

    def start(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)

    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.response = False
        while self.response is False:
            pythoncom.PumpWaitingMessages()

    def OnEventConnect(self, result_code):
        print(f"connect result_code:${result_code}")
        self.response = True

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def SetOutputNames(self, output_names):
        self.output_names = output_names

    def CommRqData(self, rq_name, tr_code, next, screen):
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rq_name, tr_code, next, screen)
        self.response = False
        while self.response is False:
            pythoncom.PumpWaitingMessages()

    def GetCommData(self, tr_code, rq_name, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, index, item)
        return data.strip()

    def OnReceiveTrData(self, screen, rq_name, tr_code, record, next):
        print(screen, rq_name, tr_code, record, next)
        self.response = True

        repeat_cnt = self.GetRepeatCnt(tr_code, record)
        if repeat_cnt == 0:
            repeat_cnt = 1

        rows = []
        for i in range(repeat_cnt):
            row = {}
            for output_name in self.output_names:
                row[output_name] = self.GetCommData(tr_code, rq_name, i, output_name)
            rows.append(row)

        self.response_queue.put(rows)

    def GetRepeatCnt(self, tr_code, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, record)
        return data

    def request_tr(self, tr_code: str, input_data: dict, output_names):
        for name, value in input_data.items():
            self.SetInputValue(name, value)

        self.output_names = output_names
        self.CommRqData("myrequest", tr_code, 0, "0101")
        return self.response_queue.get()

