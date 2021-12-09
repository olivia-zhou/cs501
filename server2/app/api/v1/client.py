from flask import Blueprint, request,make_response,current_app,g
from app.libs.redprint import Redprint
from app.validators.forms import AddCmdForm,LoginForm
from app.models.command import Command
from app.models.client import Client 
from app.models.agent import Agent 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature
from app.libs.response import resp_success 
from app.libs.token_auth import auth
from app.libs.pika import fpika,notify_all_client,put_cmd_to_queue
import json 

api = Redprint('client')

# 控制端
@api.route('/cmd', methods=['POST'])
@auth.login_required
def add_cmd_handler():
    """控制端发送命令"""
    #1.校验参数
    form = AddCmdForm().validate_for_api()
    #2.向mysql中添加命令
    id = Command.add(
        cmd = form.data['cmd'],
        agent_id = form.data['agent_id'],
        client_id = g.client_id)
    #3.获取agent的guid
    agent_guid = Agent.get_guid_by_id(form.data['agent_id'])
    #3.向rabbitmq中发送命令
    put_cmd_to_queue(agent_guid,id,form.data['cmd'])
    #4.通知所有客户端
    notify_all_client("client(%d) send a cmd(%s) to agent(%s)"%(g.client_id,form.data['cmd'],agent_guid))
    # #4.返回结果
    return resp_success(msg="send cmd success")

@api.route('/agents', methods=['GET'])
@auth.login_required
def get_agents_handler():
    """获取所有被控端agent的信息"""
    agents = Agent().get_all()
    return resp_success(msg="get all agents success", data=agents)


@api.route("/login", methods=['POST'])
def login_handler():
    """控制端登录"""
    #1.校验参数
    form  = LoginForm().validate_for_api()
    #2.校验用户名和密码
    client_id =  Client.verify(form.data['username'],form.data['password'])
    #3.生成token
    token = generate_auth_token(client_id)
    #4.通知所有客户端
    notify_all_client("client(id:%d,username:%s) login"%(client_id,form.data['username']))
    #4.返回响应
    return resp_success(msg="login success",data=token.decode("utf-8"))

def generate_auth_token(client_id):
    """生成token"""
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=current_app.config['TOKEN_EXPIRATION'])
    return s.dumps({'id':client_id})