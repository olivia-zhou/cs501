package api

import (
	"controllerEnd/models"
	"controllerEnd/settings"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

func GetAllAgents() (*models.GetAllAgentsResponse, error) {
	targetURL := settings.CurrentConf.BaseURL + settings.CurrentConf.GetAllAgents
	//1.发送请求
	request, err := http.NewRequest(http.MethodGet, targetURL, nil)
	if err != nil {
		return nil, err
	}
	request.Header.Set("Authorization", GenToken())
	resp, err := http.DefaultClient.Do(request)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	//2.解析响应
	var response models.GetAllAgentsResponse
	err = json.Unmarshal(b, &response)
	return &response, err
}
