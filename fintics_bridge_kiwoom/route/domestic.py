# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, make_response, current_app

domestic = Blueprint('domestic', __name__)


@domestic.route('/opt10080', methods=['GET'])
def opt10080():
    # parameter
    symbol = request.args.get('종목코드')

    # calls api
    input_data: dict = {
        "종목코드": symbol,
        "기준일자": '20240505',
        "수정주가구분": '01'
    }
    output_names = ['종목코드', '현재가']
    send_kiwoom_request = current_app.config['SEND_KIWOOM_REQUEST']
    output_data = send_kiwoom_request('opt10080', input_data, output_names)

    # kiwoom_api = current_app.config['KIWOOM_API']
    # kiwoom_api.SetInputValue("종목코드", "005930")
    # kiwoom_api.CommRqData("test2", "opt10001", 0, "0101", ["종목코드","종목명","시가총액"])
    # output_data = kiwoom_api.tr_queue.get()

    # response
    response = json.dumps(output_data, ensure_ascii=False)
    return make_response(response)
