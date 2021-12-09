from flask import Blueprint
from app.api.v1 import agent,client 

def create_blueprint_v1():
    bp_v1=Blueprint('v1',__name__)
    agent.api.register(bp_v1,url_prefix='/agent')
    client.api.register(bp_v1,url_prefix='/client')
    return bp_v1