from PyQt5.QAxContainer import QAxWidget
from queue import Queue

request_queue = Queue()
response_queue = Queue()


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__(self)
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.OnReceiveTrData.OnReceiveTrData.connect(self.__OnReceiveTrData)

    def __SetInputValue(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def __CommRqData(self, rqname, trcode, next, screen, output_names):
        self.output_names = output_names
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)
        while self.tr is False:
            pythoncom.PumpWaitingMessages()

    def __GetCommData(self, tr_code, rq_name, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", tr_code, rq_name, index, item)
        return data.strip()

    def __OnReceiveTrData(self, screen, rq_name, tr_code, record, next):
        print(screen, rq_name, tr_code, record, next)
        self.tr = True

        repeat_cnt = self.GetRepeatCnt(trcode, record)
        if repeat_cnt == 0:
            repeat_cnt = 1

        rows = []
        for i in range(repeat_cnt):
            row = {}
            for output_name in self.output_names:
                row[output_name] = self.GetCommData(trcode, rqname, i, output_name)
            # date = self.GetCommData(trcode, rqname, i, "일자")
            # open = self.GetCommData(trcode, rqname, i, "시가")
            rows.append(row)

        self.tr_queue.put(rows)

    def __GetRepeatCnt(self, tr_code, record):
        data = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, record)
        return data
