from flask import Blueprint, request,make_response
from app.libs.redprint import Redprint
from app.validators.forms import AddCmdForm
from app.models.command import Command
api = Redprint('client')

# 控制端
@api.route('/cmd', methods=['POST'])
def add_cmd_handler():
    """从控制端接收命令"""
    #1.接收参数
    data = request.get_json()
    #2.校验参数
    form = AddCmdForm(data=data)
    if not form.validate():
        return "error"
    #3.业务处理
    id = Command.add(data['cmd'],data['agent_id'],data['client_id'])
    return make_response(id,200)
    # #3.处理业务
    # #4.返回结果
    # return 'add_cmd_handler'

@api.route('/agents', methods=['GET'])
def get_agents_handler():
    """获取所有被控端agent的信息"""
    return 'get_agents_handler'
