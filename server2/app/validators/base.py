from flask import request
from wtforms import Form 
from app.libs.error_code import ParameterException 


class BaseForm(Form):
    def __init__(self): 
        # 获取json传参和get传参
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        # 调用父类的初始化方法
        super(BaseForm, self).__init__(data=data, **args)
    def validate_for_api(self):
        #校验参数
        valid = super(BaseForm, self).validate()
        #校验失败返回响应
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
