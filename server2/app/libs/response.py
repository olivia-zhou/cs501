from flask import make_response,jsonify

def resp_success(msg,data={}):
    """成功时返回的响应""" 
    resp = {
        'code': 666,
        'msg': msg,
        'data': data
    }
    return make_response(resp, 200)

