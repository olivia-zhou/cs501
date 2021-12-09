package rabbitmq

import (
	"controllerEnd/models"
	"controllerEnd/vars"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/gen2brain/beeep"
	"github.com/sirupsen/logrus"
)

func getClientID() (int, error) {
	part2 := strings.Split(vars.Token, ".")[1]
	part2Text, err := base64.RawURLEncoding.DecodeString(part2)
	if err != nil {
		fmt.Printf("Error decoding string: %s ", err.Error())
		return 0, err
	}
	var temp struct {
		ID int `json:"id"`
	}
	if err := json.Unmarshal(part2Text, &temp); err != nil {
		return 0, err
	}
	return temp.ID, nil

}

func NotifyResult() error {
	//从token中获取自己的id
	clientID, err := getClientID()
	if err != nil {
		return err
	}
	//1.创建channel
	ch, err := conn.Channel()
	if err != nil {
		logrus.Error("conn.Channel failed,err:", err)
		return err
	}
	//2.声明队列
	q, err := ch.QueueDeclare(
		fmt.Sprintf("result_queue::client_id::%d", clientID), // name
		false, // durable
		false, // delete when usused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	if err != nil {
		logrus.Error("ch.QueueDeclare failed,err:", err)
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
		for d := range msgs {
			var msg models.CmdResult
			if err := json.Unmarshal(d.Body, &msg); err != nil {
				logrus.Error("json.Unmarshal failed,err:", err)
				continue
			}
			fmt.Println()
			fmt.Println("==========================")
			fmt.Println("agent_id:", msg.AgentID)
			fmt.Println("client_id:", msg.ClientID)
			fmt.Println("cmd:", msg.Cmd)
			fmt.Println("result:", msg.Result)
			fmt.Println("==========================")
		}
	}()
	return nil
}

func NotifyMessage() error {
	//从token中获取自己的id
	clientID, err := getClientID()
	if err != nil {
		return err
	}
	//1.创建channel
	ch, err := conn.Channel()
	if err != nil {
		logrus.Error("conn.Channel failed,err:", err)
		return err
	}
	// defer ch.Close()

	//2.声明队列
	q, err := ch.QueueDeclare(
		fmt.Sprintf("message_queue::%d", clientID), // name
		false, // durable
		false, // delete when usused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	if err != nil {
		logrus.Error("ch.QueueDeclare failed,err:", err)
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
		for d := range msgs {
			var msg models.Message
			if err := json.Unmarshal(d.Body, &msg); err != nil {
				logrus.Error("json.Unmarshal failed,err:", err)
				continue
			}
			err := beeep.Notify(msg.Title, msg.Body, "")
			if err != nil {
				logrus.Error("beeep.Notify failed,err:", err)
			}
		}
	}()
	return nil
}
