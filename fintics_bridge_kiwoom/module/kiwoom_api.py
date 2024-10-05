from PyQt5.QAxContainer import QAxWidget
import pythoncom
import queue


class KiwoomApi:

    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)
        self.login = False
        self.tr = False
        self.tr_queue = queue.Queue()

    def CommConnect(self):
        print("CommConnect")
        self.ocx.dynamicCall("CommConnect()")
        while self.login is False:
            pythoncom.PumpWaitingMessages()

    def OnEventConnect(self, code):
        self.login = True
        print("login is done", code)

    def SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def CommRqData(self, rqname, trcode, next, screen):
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
        data = []
        for i in range(repeatCnt):
            date = self.GetCommData(trcode, rqname, i, "일자")
            open = self.GetCommData(trcode, rqname, i, "시가")
            data.append([date, open])

        self.tr_queue.put((data, next))



    def GetRepeatCnt(self, trcode, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, record)
        return data