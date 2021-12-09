from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from app.models.base import Base, db
from app.models.agent import Agent
from app.models.client import Client 
from datetime import datetime 

class Command(Base):
    """命令表"""
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    cmd =Column(String(255))
    agent_id = Column(Integer, ForeignKey('agent.id'))
    client_id = Column(Integer, ForeignKey('client.id'))
    result = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
 
    @staticmethod
    def add(cmd,agent_id,client_id): 
        with db.auto_commit():
            command = Command()
            command.cmd = cmd
            command.agent_id = agent_id
            command.client_id = client_id
            command.created_at = datetime.utcnow()
            command.updated_at = datetime.utcnow()
            db.session.add(command)
            return command.id
    @staticmethod
    def is_exist(cmd_id): 
        with db.auto_commit():
            command = Command.query.filter_by(id=cmd_id).first()
            if command:
                return True
            return False
    @staticmethod
    def update(cmd_id,result): 
        with db.auto_commit():
            command = Command.query.filter_by(id=cmd_id)
            command.result = result
            command.updated_at = datetime.now()
            db.session.add(command)
            return command.id

