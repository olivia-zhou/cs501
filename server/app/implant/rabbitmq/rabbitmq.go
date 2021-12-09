package rabbitmq

import (
	"controllerEnd/settings"
	"fmt"

	"github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
)

var conn *amqp.Connection

func Init() (err error) {
	addr := fmt.Sprintf("amqp://%s:%s@%s:%d/",
		settings.CurrentConf.RabbitMq.Username,
		settings.CurrentConf.RabbitMq.Password,
		settings.CurrentConf.RabbitMq.Host,
		settings.CurrentConf.RabbitMq.Port)
	conn, err = amqp.Dial(addr)
	if err != nil {
		logrus.Error("amqp.Dial failed,err:", err)
		return err
	}
	return nil
}

func Close() {
	conn.Close()
}
