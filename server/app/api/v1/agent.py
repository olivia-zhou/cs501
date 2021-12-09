from flask import Blueprint 
from app.libs.redprint import Redprint
api = Redprint('agent')
# 被控端
@api.route('/ping/<agent_id>', methods=['POST'])
def ping_handler(agent_id):
    """被控端向服务器上报状态，保持心跳"""
    return 'ping_handler'

@api.route('/cmd/<agent_id>', methods=['GET'])
def get_cmd_handler(agent_id):
    """被控端从服务器获取命令"""
    return 'get_cmd_handler'

@api.route('/result', methods=['POST'])
def send_result_handler():
    """被控端向服务器上报执行结果"""
    return 'send_result_handler'