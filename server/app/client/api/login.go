package api

import (
	"bytes"
	"controllerEnd/models"
	"controllerEnd/settings"
	"controllerEnd/vars"
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"

	"github.com/sirupsen/logrus"
)

func Login(username, password string) error {
	targetURL := settings.CurrentConf.BaseURL + settings.CurrentConf.API.Login
	//1.构造参数
	params := map[string]string{
		"username": username,
		"password": password,
	}
	paramStr, err := json.Marshal(params)
	if err != nil {
		logrus.Error("json.Marshal failed,err:", err)
		return err
	}
	resp, err := http.Post(targetURL, "application/json", bytes.NewReader(paramStr))
	if err != nil {
		logrus.Error("http.Post failed,err:", err)
		return err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logrus.Error("ioutil.ReadAll faield,err:", err)
		return err
	}
	var response models.Response
	err = json.Unmarshal(body, &response)
	if err != nil {
		logrus.Error("json.Unmarshal failed,err:", err)
		return err
	}
	if response.Code != 666 {
		return errors.New(response.Msg)
	}
	vars.Token = response.Data.(string)
	return nil
}
