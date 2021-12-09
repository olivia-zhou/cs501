package controllers

import (
	"controllerEnd/api"
	"controllerEnd/models"
	"controllerEnd/vars"
	"fmt"
	"os"
	"strconv"

	"github.com/abiosoft/ishell"
	"github.com/fatih/structs"
	"github.com/olekukonko/tablewriter"
	"github.com/sirupsen/logrus"
)

//GetAllAgentsHandler 获取所有被控端
func GetAllAgentsHandler(c *ishell.Context) {
	response, err := api.GetAllAgents()
	if err != nil {
		logrus.Error("api.GetAllAgents failed,err:", err)
		return
	}

	if response.Code != 666 {
		logrus.Error(response.Msg)
		return
	}
	if response.AgentList == nil {
		c.Println("no agents")
		return
	}
	for i := range response.AgentList {
		vars.UpAgentIDList = append(vars.UpAgentIDList, fmt.Sprintf("%v", response.AgentList[i].AgentID))
	}

	data := make([][]string, 0)
	for _, agent := range response.AgentList {
		values := make([]string, 0)
		for _, value := range structs.Values(agent) {
			values = append(values, fmt.Sprintf("%v", value))
		}
		data = append(data, values)
	}
	var tempAgent models.Agent
	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader(structs.Names(tempAgent))
	table.SetAlignment(tablewriter.ALIGN_CENTER)
	table.SetBorder(true)
	table.SetRowLine(true)
	table.SetAutoMergeCells(true)
	table.AppendBulk(data)
	table.SetCaption(true, "Agents UP")
	table.Render()
}

//SelectAgentHandler 选择被控端
func SelectAgentHandler(c *ishell.Context) {
	if len(vars.UpAgentIDList) == 0 {
		c.Println("请先执行 agents 获取所有被控端的信息")
		return
	}
	choice := c.MultiChoice(vars.UpAgentIDList, "请选择要控制的被控端:")
	vars.TargetAgentID, _ = strconv.Atoi(vars.UpAgentIDList[choice])
	c.Println("您选择的被控端是:", vars.TargetAgentID)
}
