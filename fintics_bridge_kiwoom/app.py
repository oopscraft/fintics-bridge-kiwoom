# -*- coding: utf-8 -*-
import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from flask import Flask
import nest_asyncio
from fintics_bridge_kiwoom.route.domestic import domestic
from fintics_bridge_kiwoom.route.overseas import overseas
import queue
import threading
import pythoncom
import queue
from fintics_bridge_kiwoom.module.kiwoom_domestic import KiwoomDomestic

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# flask
flask = Flask(__name__)
flask.config['JSON_AS_ASCII'] = False
flask.register_blueprint(domestic, url_prefix='/domestic')
flask.register_blueprint(overseas, url_prefix='/overseas')

# nest_asyncio 적용
nest_asyncio.apply()


def run_flask():
    flask.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
        use_reloader=False
    )


if __name__ == "__main__":

    # Flask를 별도 스레드에서 실행
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 메인 스레드가 종료되면 Flask 스레드도 종료
    flask_thread.start()

    # login
    try:
        app = QApplication(sys.argv)
        kiwoom_domestic = KiwoomDomestic()
        kiwoom_domestic.start()
        flask.config['KIWOOM_DOMESTIC'] = kiwoom_domestic

        # connect
        kiwoom_domestic.CommConnect()

        # test 1
        print("== start request 1")
        kiwoom_domestic.SetInputValue("종목코드", "005930")
        kiwoom_domestic.SetInputValue("기준일자", "20240404")
        kiwoom_domestic.SetInputValue("수정주가구분", "0")
        kiwoom_domestic.SetOutputNames(["종목명", "현재가"])
        kiwoom_domestic.CommRqData("test1", "opt10081", 0, "0101")
        response = kiwoom_domestic.response_queue.get()
        print(response)
        print("== end request 1")

        # test 2
        print("== start request 2")
        kiwoom_domestic.SetInputValue("종목코드", "005930")
        kiwoom_domestic.SetOutputNames(["종목명", "현재가"])
        kiwoom_domestic.CommRqData("test1", "opt10001", 0, "0101")
        response = kiwoom_domestic.response_queue.get()
        print(response)
        print("== end request 2")

        app.exec_()
        print("#################")
    except KeyboardInterrupt:
        sys.exit(0)



