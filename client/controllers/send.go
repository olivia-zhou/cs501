package controllers

import (
	"controllerEnd/api"
	"controllerEnd/vars"

	"github.com/abiosoft/ishell"
	"github.com/sirupsen/logrus"
)

//SendCmdHandler 发送命令
func SendCmdHandler(c *ishell.Context) {
	if vars.TargetAgentID == 0 {
		c.Println("select an agent first")
		return
	}
	if len(c.Args) == 0 {
		c.Println("enter: send <cmd>")
		return
	}
	response, err := api.SendCmd(c.Args[0], vars.TargetAgentID)
	if err != nil {
		logrus.Error("api.SendCmd failed,err:", err)
		return
	}
	if response.Code == 666 {
		c.Printf("send cmd:%s success\n", c.Args[0])
		return
	}
	c.Println("send cmd failed", response)
}
