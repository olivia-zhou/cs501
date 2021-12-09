from flask import Flask 

class createFlaskApp:
    def register_blueprints(self, app):
        from app.api.v1 import create_blueprint_v1
        app.register_blueprint(create_blueprint_v1(), url_prefix='/api/v1')
    
    def register_plugin(self, app):
        from app.models.base import db
        db.init_app(app)
        with app.app_context():
            db.create_all()
    
    def create_app(self):
        app = Flask(__name__)
        # 读取配置项
        #app.config.from_object('app.config.setting')
        #app.config.from_object('app.config.secure')
        # 注册路由
        #self.register_blueprints(app)
        # 注册插件
        #self.register_plugin(app)
        return app