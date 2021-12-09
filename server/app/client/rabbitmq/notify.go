package rabbitmq

import (
	"fmt"

	"github.com/gen2brain/beeep"
	"github.com/sirupsen/logrus"
)

func NotifyMessage() error {
	//1.创建channel
	ch, err := conn.Channel()
	if err != nil {
		logrus.Error("conn.Channel failed,err:", err)
		return err
	}
	defer ch.Close()
	//2.声明交换机
	err = ch.ExchangeDeclare(
		"message_exchange", // name
		"fanout",           // type
		false,              // durable
		false,              // auto-deleted
		false,              // internal
		false,              // no-wait
		nil,                // arguments
	)
	if err != nil {
		logrus.Error("ch.ExchangeDeclare failed,err:", err)
		return err
	}

	q, err := ch.QueueDeclare(
		"message_queue::1", // name
		false,              // durable
		false,              // delete when usused
		true,               // exclusive
		false,              // no-wait
		nil,                // arguments
	)
	if err != nil {
		logrus.Error("ch.QueueDeclare failed,err:", err)
		return err
	}
	err = ch.QueueBind(
		q.Name,             // queue name
		"",                 // routing key
		"message_exchange", // exchange
		false,
		nil,
	)
	if err != nil {
		logrus.Error("ch.QueueBind failed,err:", err)
		return err
	}
	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	if err != nil {
		return err
	}

	go func() {
		fmt.Println("开始监听队列：", q.Name)
		for d := range msgs {
			fmt.Prin
			err := beeep.Notify("Title", string(d.Body), "")
			if err != nil {
				logrus.Error("beeep.Notify failed,err:", err)
			}
		}
	}()
	return nil
}
