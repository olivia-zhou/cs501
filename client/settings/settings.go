package settings

import (
	"errors"
	"fmt"

	"github.com/spf13/viper"
)

var CurrentConf AppConfig

type AppConfig struct {
	BaseURL  string `mapstructure:"base_url"`
	API      `mapstructure:"api"`
	RabbitMq `mapstructure:"rabbitmq"`
}

type API struct {
	Login        string `mapstructure:"login"`
	SendCmd      string `mapstructure:"send_cmd"`
	GetAllAgents string `mapstructure:"get_all_agents"`
}

type RabbitMq struct {
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
}

//Init 初始化配置
func Init(filePath string) error {
	if len(filePath) == 0 {
		return errors.New("filepath is invalid")
	}
	//指定配置文件
	viper.SetConfigFile(filePath)
	//读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		fmt.Printf("viper.ReadInConfig() failed,err:%v\n", err)
		return err
	}
	//反序列化配置信息
	if err := viper.Unmarshal(&CurrentConf); err != nil {
		fmt.Printf("viper.Unmarshal(&CurrentConf) failed,err:%v\n", err)
		return err
	}
	return nil
}
