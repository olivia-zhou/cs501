package main

import (
	"controllerEnd/api"
	"controllerEnd/rabbitmq"
	"controllerEnd/routers"
	"controllerEnd/settings"
	"flag"
	"fmt"
	"os"

	"github.com/abiosoft/ishell"
	"github.com/sirupsen/logrus"
	"golang.org/x/crypto/ssh/terminal"
)

func main() {
	var (
		username       string
		configFilePath string
	)
	//1.解析命令行参数
	flag.StringVar(&username, "u", "", "username")
	flag.StringVar(&configFilePath, "c", "./config.json", "config file path")
	flag.Parse()
	if username == "" {
		flag.Usage()
		return
	}
	//2.读取密码
	fmt.Print("password:")
	password, err := terminal.ReadPassword(int(os.Stdin.Fd()))
	if err != nil {
		logrus.Fatal(err)
	}
	//3.初始化配置文件
	if err := settings.Init(configFilePath); err != nil {
		logrus.Error("settings.Init failed,err:", err)
		return
	}
	//4.登录
	if err := api.Login(username, string(password)); err != nil {
		logrus.Error("\rlogin failed,err:", err)
		return
	}
	//5.初始化rabbitmq
	if err := rabbitmq.Init(); err != nil {
		logrus.Error("rabbitmq.Init() failed,err:", err)
		return
	}
	//6.监听通知
	if err := rabbitmq.NotifyMessage(); err != nil {
		logrus.Error("rabbitmq.NotifyMessage failed,err:", err)
		return
	}
	//7.监听结果
	if err := rabbitmq.NotifyResult(); err != nil {
		logrus.Error("rabbitmq.ResultMessage failed,err:", err)
		return
	}
	shell := ishell.New()
	shell.Println("\rhappy hacking")
	routers.Init(shell)
	shell.Run()
}
