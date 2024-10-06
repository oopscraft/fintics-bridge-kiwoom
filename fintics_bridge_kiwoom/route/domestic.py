# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, make_response, current_app

domestic = Blueprint('domestic', __name__)


@domestic.route('/opt10080', methods=['GET'])
def opt10080():
    # parameter
    symbol = request.args.get('종목코드')

    # calls api
    kiwoom_domestic = current_app.config['KIWOOM_DOMESTIC']
    input_data: dict = {
        "종목코드": symbol,
        "기준일자": '20240505',
        "수정주가구분": '0'
    }
    output_names = ['종목코드', '현재가']
    output_data = kiwoom_domestic.request_tr("opt10080", input_data, output_names)

    # response
    response = json.dumps(output_data, ensure_ascii=False)
    return make_response(response)
