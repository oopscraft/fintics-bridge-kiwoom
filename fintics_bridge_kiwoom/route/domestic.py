# -*- coding: utf-8 -*-
import json
from flask import Blueprint, request, make_response, current_app
from datetime import datetime


domestic = Blueprint('domestic', __name__)


@domestic.route('/opt10080', methods=['GET'])
def opt10080():
    """
    [ OPT10080 : 주식분봉차트조회요청 ]
    """
    # parameter
    symbol = request.args.get('종목코드')

    # calls api
    kiwoom_domestic = current_app.config['KIWOOM_DOMESTIC']
    input_data: dict = {
        "종목코드": symbol,
        "틱범위": '1',
        "수정주가구분": '0'
    }
    output_names = ['종목코드', '체결시간', '현재가', '시가', '고가', '저가', '거래량', '수정주가구분']
    output_data = kiwoom_domestic.request_tr("opt10080", input_data, output_names)

    # response
    response = json.dumps(output_data, ensure_ascii=False, indent=4)
    return make_response(response, 200, {"Content-Type": "application/json"})


@domestic.route('/opt10081', methods=['GET'])
def opt10081():
    """
    [ OPT10081 : 주식일봉차트조회요청 ]
    """
    # parameter
    symbol = request.args.get('종목코드')

    # calls api
    kiwoom_domestic = current_app.config['KIWOOM_DOMESTIC']
    input_data: dict = {
        "종목코드": symbol,
        "기준일자": datetime.today().strftime('%Y%m%d'),
        "수정주가구분": '0'
    }
    output_names = ['종목코드', '일자', '현재가', '시가', '고가', '저가', '거래량', '수정주가구분']
    output_data = kiwoom_domestic.request_tr("opt10081", input_data, output_names)

    # response
    response = json.dumps(output_data, ensure_ascii=False, indent=4)
    return make_response(response, 200, {"Content-Type": "application/json"})