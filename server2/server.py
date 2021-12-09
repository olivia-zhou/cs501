from app.app import create_app
from app.libs.error import APIException
from werkzeug.exceptions import HTTPException
from app.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    """统一处理所有未知异常"""
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

if __name__ == '__main__':
    app.run(debug=True)

