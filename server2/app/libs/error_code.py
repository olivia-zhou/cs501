from app.libs.error import APIException



class ParameterException(APIException):
    """传参不正确"""
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class ServerError(APIException):
    """未知错误"""
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999

class NotFound(APIException):
    code = 404
    msg = 'the resource are not found'
    error_code = 1001

class AuthFailed(APIException):
    """认证失败"""
    code = 401
    error_code = 1005
    msg = 'authorization failed'
