import pythoncom
from PyQt5.QAxContainer import QAxWidget
from queue import Queue

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from typing import List


class KiwoomDomestic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.response_queue = Queue()
        self.ocx.OnEventConnect.connect(self.__OnEventConnect)
        self.ocx.OnReceiveTrData.connect(self.__OnReceiveTrData)
        self.output_names = []

        # connect
        self.__CommConnect()

    def __CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        # while True:
        #     pythoncom.PumpWaitingMessages()

    def __OnEventConnect(self, result_code):
        print(f"connect result_code:${result_code}")

    def __SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def __CommRqData(self, rqname, trcode, next, screen):
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)
        self.tr = False
        while self.tr is False:
            pythoncom.PumpWaitingMessages()

    def __GetCommData(self, tr_code, rq_name, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, index, item)
        return data.strip()

    def __OnReceiveTrData(self, screen, rq_name, tr_code, record, next):
        print(screen, rq_name, tr_code, record, next)
        self.tr = True

        repeat_cnt = self.__GetRepeatCnt(tr_code, record)
        if repeat_cnt == 0:
            repeat_cnt = 1

        rows = []
        for i in range(repeat_cnt):
            row = {}
            for output_name in self.output_names:
                row[output_name] = self.__GetCommData(trcode, rqname, i, output_name)
            # date = self.GetCommData(trcode, rqname, i, "일자")
            # open = self.GetCommData(trcode, rqname, i, "시가")
            rows.append(row)

        self.response_queue.put(rows)

    def __GetRepeatCnt(self, tr_code, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, record)
        return data

    def request(self, tr_code: str, input_data: dict, output_names):
        for name, value in input_data.items():
            self.__SetInputValue(name, value)

        self.output_names = output_names
        self.__CommRqData("myrequest", tr_code, 0, "0101")
        return self.response_queue.get()

