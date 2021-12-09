"""What does this file do?"""
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.models.base import Base, db


class Command(Base):
    """命令表"""
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    cmd = Column(String(255))
    agent_id = Column(Integer, ForeignKey('agents.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    result = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @staticmethod
    def add(cmd, agent_id, client_id):
        """I am not sure what this method does"""
        with db.auto_commit():
            command = Command()
            command.cmd = cmd
            command.agent_id = agent_id
            command.client_id = client_id
            command.created_at = datetime.datetime.now()
            command.updated_at = datetime.datetime.now()
            db.session.add(command)
            return command.id
