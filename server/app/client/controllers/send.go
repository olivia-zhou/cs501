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
		c.Println("请先选择被控端:select_agent")
		return
	}
	if len(c.Args) == 0 {
		c.Println("请输入要发送的命令:send 命令")
		return
	}
	response, err := api.SendCmd(c.Args[0], vars.TargetAgentID)
	if err != nil {
		logrus.Error("api.SendCmd failed,err:", err)
		return
	}
	if response.Code == 666 {
		c.Printf("发送命令:%s 成功\n", c.Args[0])
		c.Println(response.Data)
		return
	}
	c.Println("发送命令失败", response)
}
