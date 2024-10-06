from celery import shared_task
from PyQt5.QAxContainer import QAxWidget
import pythoncom
import queue
from typing import List


class KiwoomApi:

    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)
        self.login = False
        self.tr = False
        self.output_names = []
        self.tr_queue = queue.Queue()

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def CommRqData(self, rqname, trcode, next, screen, output_names):
        self.output_names = output_names
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)
        while self.tr is False:
            pythoncom.PumpWaitingMessages()

    def GetCommData(self, trcode, rqname, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
        return data.strip()

    def OnReceiveTrData(self, screen, rqname, trcode, record, next):
        print(screen, rqname, trcode, record, next)
        self.tr = True

        repeatCnt = self.GetRepeatCnt(trcode, record)
        if repeatCnt == 0:
            repeatCnt = 1

        rows = []
        for i in range(repeatCnt):
            row = {}
            for output_name in self.output_names:
                row[output_name] = self.GetCommData(trcode, rqname, i, output_name)
            # date = self.GetCommData(trcode, rqname, i, "일자")
            # open = self.GetCommData(trcode, rqname, i, "시가")
            rows.append(row)

        self.tr_queue.put(rows)

    def GetRepeatCnt(self, trcode, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, record)
        return data


# kiwoom_api = KiwoomApi()
# kiwoom_api = {}

# request_api = {}
# def request_api(tr_code: str, input_data: dict, output_names):
#
#     # input
#     for key, value in input_data.items():
#         kiwoom_api.SetInputValue(key, value)
#
#     # request
#     kiwoom_api.CommRqData("test", tr_code, 0, "screen", output_names)
#
#     # response
#     return kiwoom_api.tr_queue.get()
