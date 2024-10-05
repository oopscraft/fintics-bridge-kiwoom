import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
from flask import Flask
import nest_asyncio
from fintics_bridge_kiwoom.module.kiwoomapi import KiwoomApi

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# app
app = Flask(__name__)

# nest_asyncio 적용
nest_asyncio.apply()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.OnEventConnect.connect(self.event_connect)

    def event_connect(self, err_code):
        if err_code == 0:
            print('로그인 성공')
            self.close()

if __name__ == "__main__":
    # login
    try:
        login_app = QApplication(sys.argv)
        #login_window = LoginWindow()
        #login_window.show()
        #login_app.exec_()
        kiwoom_api = KiwoomApi()
        kiwoom_api.comm_connect()
    except KeyboardInterrupt:
        sys.exit(0)

    # run
    app.run(
        host="0.0.0.0",
        port="8080",
        debug=True,
        use_reloader=False
    )

