from PyQt5.QAxContainer import QAxWidget

class KiwoomApi():
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
    def comm_connect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.ocx.OnEventConnect.connect(self.comm_connect_callback)
    def comm_connect_callback(self, message):
        print(message)

