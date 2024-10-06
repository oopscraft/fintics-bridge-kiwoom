# -*- coding: utf-8 -*-
import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from flask import Flask
import nest_asyncio
from fintics_bridge_kiwoom.module.kiwoom_api import KiwoomApi
from fintics_bridge_kiwoom.route.domestic import domestic
from fintics_bridge_kiwoom.route import overseas
import queue
import threading
import pythoncom
import queue
from fintics_bridge_kiwoom.module.kiwoom import Kiwoom

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# flask
flask = Flask(__name__)
flask.config['JSON_AS_ASCII'] = False
flask.register_blueprint(domestic, url_prefix='/domestic')
# flask.register_blueprint(overseas, url_prefix='/overseas')

# nest_asyncio 적용
nest_asyncio.apply()


if __name__ == "__main__":
    # login
    try:
        app = QApplication(sys.argv)
        kiwoom = Kiwoom()
        app.exec_()
    except KeyboardInterrupt:
        sys.exit(0)


    # # test kiwoom api
    # kiwoom_api = KiwoomApi()
    # kiwoom_api.SetInputValue("종목코드", "005930")
    # kiwoom_api.SetInputValue("기준일자", "20240920")
    # kiwoom_api.SetInputValue("수정주가구분", "0")
    # kiwoom_api.CommRqData("myrequest", "opt10081", 0, "0101", ["종목코드"])
    # tr_data = kiwoom_api.tr_queue.get()
    # print(tr_data)

    # kiwoom_api.SetInputValue("종목코드", "005930")
    # kiwoom_api.CommRqData("test2", "opt10001", 0, "0101", ["종목코드","종목명","시가총액"])
    # response = kiwoom_api.tr_queue.get()
    # print(response)


    # run
    flask.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
        use_reloader=False
    )
