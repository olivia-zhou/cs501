package routers

import (
	"controllerEnd/controllers"

	"github.com/abiosoft/ishell"
)

//Init 初始化路由
func Init(shell *ishell.Shell) {
	//获取所有被控端
	shell.AddCmd(&ishell.Cmd{
		Name: "agents",
		Help: "get agents list ",
		Func: controllers.GetAllAgentsHandler,
	})
	//选择被控端
	shell.AddCmd(&ishell.Cmd{
		Name: "select_agent",
		Help: "select a agent",
		Func: controllers.SelectAgentHandler,
	})
	//向被控端发布命令
	shell.AddCmd(&ishell.Cmd{
		Name: "send",
		Help: "send command to agent",
		Func: controllers.SendCmdHandler,
	})

}
