package api

import (
	"bytes"
	"controllerEnd/models"
	"controllerEnd/settings"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

func SendCmd(cmd string, agentID int) (*models.Response, error) {
	targetURL := settings.CurrentConf.BaseURL + settings.CurrentConf.SendCmd
	contentType := "application/json"
	//1.构造传参
	params := map[string]interface{}{
		"agent_id": agentID,
		"cmd":      cmd,
	}
	//2.参数序列化
	paramStr, err := json.Marshal(params)
	if err != nil {
		return nil, err
	}
	//3.将序列化的参数抽象为一个Reader
	paramReader := bytes.NewReader(paramStr)
	//4.发送请求
	request, err := http.NewRequest(http.MethodPost, targetURL, paramReader)
	if err != nil {
		return nil, err
	}
	request.Header.Set("Authorization", GenToken())
	request.Header.Set("Content-Type", contentType)
	resp, err := http.DefaultClient.Do(request)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	//5.读取响应
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	var response models.Response
	err = json.Unmarshal(body, &response)
	if err != nil {
		return nil, err
	}
	return &response, nil
}
