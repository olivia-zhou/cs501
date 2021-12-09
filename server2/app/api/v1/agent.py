from flask import Blueprint, request
from app.libs.redprint import Redprint
from app.validators.forms import PingForm, ResultForm
from app.models.agent import Agent
from app.models.command import Command
from app.models.client import Client 
from app.libs.response import resp_success
from app.libs.pika import fpika,get_cmd_from_queue
from datetime import datetime
import json

api = Redprint('agent')


# 被控端
@api.route('/ping/<agent_id>', methods=['POST'])
def ping_handler(agent_id):
    form= PingForm().validate_for_api()
    exist = Agent().is_exist(agent_id)
    if not exist:
        # 新被控端上线
        #1.向mysql中插入新记录
        Agent().add(guid=agent_id,
                    computer_name=form.data['host_name'],
                    username=form.data['user_login_name'],
                    intergrity=form.data['intergrity'],
                    ip=form.data['ip'],
                    session_key=form.data['session_key'])
        print('新被控端上线')
        #2.向rabbitmq中发送消息,通知所有控制端
        channel = fpika.channel()
        #查询所有控制端
        clients = Client().get_all()
        for client in clients:
            queue_name = "message_queue::%d"%(client.id)
            #声明队列
            channel.queue_declare(queue=queue_name)
            #向交换机发送消息
            msg = json.dumps({
                "title":"%s"%datetime.utcnow(),
                "body": "agent_id::%s is online" % agent_id,
            })
            channel.basic_publish(exchange='',routing_key=queue_name,body=msg)
        fpika.return_broken_channel(channel)
        fpika.return_channel(channel)

        
    else:
        Agent().update(guid=agent_id,
                       computer_name=form.data['host_name'],
                       username=form.data['user_login_name'],
                       intergrity=form.data['intergrity'],
                       ip=form.data['ip'],
                       session_key=form.data['session_key'])
    return resp_success(msg="ping success")


@api.route('/cmd/<agent_id>', methods=['GET'])
def get_cmd_handler(agent_id):
    """被控端从服务器获取命令"""
    get_cmd_from_queue(agent_id)
    return 'get_cmd_handler'



@api.route('/result', methods=['POST'])
def send_result_handler():
    """被控端向服务器上报执行结果"""
    data = ResultForm().validate_for_api()
    Command().update(cmd_id=data['cmd_id'], result=data['result'])
    return resp_success(msg="send result success")