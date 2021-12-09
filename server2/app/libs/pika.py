from flask_pika import Pika
from app.models.client import Client
from datetime import datetime
from flask import g
import json 
import queue 
 
fpika = Pika()
agent_cmd_queue = {}
def notify_all_client(message):
    """通知所有客户端""" 
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
            "body":message,
        })
        channel.basic_publish(exchange='',routing_key=queue_name,body=msg)
    fpika.return_broken_channel(channel)
    fpika.return_channel(channel)

def put_cmd_to_queue(agent_guid,cmd_id,cmd):
    """将命令放入被控端对应的命令队列中"""
    channel = fpika.channel()
    queue_name = 'cmd_queue::agent_guid::'+agent_guid
    channel.queue_declare(queue=queue_name)
    cmd = json.dumps({'cmd_id':cmd_id,'client_id':g.client_id,'cmd':cmd})
    channel.basic_publish(exchange='',routing_key=queue_name,body=cmd)
    fpika.return_broken_channel(channel)
    fpika.return_channel(channel)

def get_cmd_from_queue(agent_guid):
    """从被控端对应的命令队列中获取命令"""
    if agent_guid in agent_cmd_queue : 
        cmd = agent_cmd_queue[agent_guid].get(block=False)
        return cmd 
    else:
        channel = fpika.channel()
        queue_name = 'cmd_queue::agent_guid::'+agent_guid
        channel.queue_declare(queue=queue_name)
        #消费消息
        def callback(ch, method, properties, body):
            q = queue.Queue()
            q.put(body)
            agent_cmd_queue[agent_guid] = q
            print("ch:%s,method:%s,properties:%s,body:%s"%(ch,method,properties,body))
            print(" [x] Received %r" % body)
        channel.basic_consume(callback ,queue=queue_name,no_ack=True)
        channel.start_consuming()
        fpika.return_broken_channel(channel)
        fpika.return_channel(channel)
        return None
def put_result_to_queue(cmd): 
    """将命令结果放入客户端对应的命令队列中"""
    channel = fpika.channel()
    queue_name = 'result_queue::client_id::'+str(cmd['client_id'])
    channel.queue_declare(queue=queue_name)
    cmd = json.dumps(cmd)
    channel.basic_publish(exchange='',routing_key=queue_name,body=cmd)
    fpika.return_broken_channel(channel)
    fpika.return_channel(channel)