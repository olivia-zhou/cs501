from sqlalchemy import Column, Integer, String
from app.models.base import Base, db
from app.libs.error_code import NotFound

class Client(Base):
    """控制端表"""
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))

    @staticmethod 
    def add(computer_name, username):
        """添加一条记录"""
        with db.auto_commit():
            client = Client()
            client.computer_name = computer_name
            client.username = username
            db.session.add(client)
            return client.id
    @staticmethod 
    def verify(username, password):
        """验证用户名和密码"""
        client = Client.query.filter_by(username=username, password=password).first()
        if not client:
            raise NotFound(msg='wrong username or password')
        return client.id
    @staticmethod
    def get_all():
        """获取所有记录"""
        return Client.query.all()