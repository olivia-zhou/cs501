SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/c2server"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY="secret"

#RabbitMQ 配置
FLASK_PIKA_PARAMS = {
    'host': 'localhost',  # amqp.server.com
    'username': 'admin',  # convenience param for username
    'password': 'admin',  # convenience param for password
    'port': 5672,  # amqp server port
    #'virtual_host': 'vhost'  # amqp vhost
}
