from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from app.models.base import Base, db
from datetime import datetime

class Agent(Base):
    """被控端表"""
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True)
    computer_name = Column(String(255))
    username = Column(String(255))
    guid = Column(String(255))
    integrity = Column(String(255))
    ip = Column(String(255))
    session_key = Column(String(255))
    sleep_time = Column(Integer)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    @property
    def serialized(self):
        return {
            'id': self.id,
            'computer_name': self.computer_name,
            "guid": self.guid,
            "username": self.username,
            "intergity": self.integrity,
            "session_key": self.session_key,
            "sleep_time": self.sleep_time,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "ip": self.ip,
            "sleep_time": self.sleep_time
        }
    @staticmethod
    def add(computer_name,username,guid,intergrity,ip,session_key): 
        with db.auto_commit():
            agent = Agent()
            agent.computer_name = computer_name
            agent.username = username
            agent.guid = guid
            agent.integrity = intergrity
            agent.ip = ip 
            agent.session_key = session_key 
            agent.first_seen = datetime.utcnow()
            agent.last_seen = datetime.utcnow()
            db.session.add(agent)
            return agent.id 
    @staticmethod 
    def is_exist(agent_id): 
        with db.auto_commit():
            agent = Agent.query.filter_by(guid=agent_id).first()
            if agent:
                return True
            else:
                return False
    @staticmethod
    def update(computer_name,username,guid,intergrity,ip,session_key): 
        with db.auto_commit():
            agent = Agent.query.filter_by(guid=guid).first()
            agent.computer_name = computer_name
            agent.username = username
            agent.integrity = intergrity
            agent.ip = ip 
            agent.session_key = session_key 
            agent.last_seen = datetime.utcnow()
            return agent.id
    @staticmethod
    def get_all():
        with db.auto_commit():
            agents = Agent.query.all()
            if len(agents)== 0:
                return None
            return [agents. serialized for agents in agents]
    @staticmethod
    def get_guid_by_id(id): 
        agent = Agent.query.filter_by(id=id).first()
        if agent:
            return agent.guid
        else:
            return None