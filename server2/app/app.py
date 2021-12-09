from flask import Flask 
import pymysql


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/api/v1')

def register_plugin(app):
    #初始化mysql
    from app.models.base import db
    pymysql.install_as_MySQLdb()
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
    #初始化rabbitmq
    from app.libs.pika import fpika
    fpika.init_app(app)

def create_app():
    app = Flask(__name__)
    # 读取配置项
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    # 注册路由
    register_blueprints(app)
    # 注册插件
    register_plugin(app)
    return app