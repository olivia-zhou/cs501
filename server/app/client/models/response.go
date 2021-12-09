package models

type Response struct {
	Code int         `json:"code"`
	Msg  string      `json:"msg"`
	Data interface{} `json:"data"`
}

type GetAllAgentsResponse struct {
	Code      int     `json:"code"`
	AgentList []Agent `json:"data"`
	Msg       string  `json:"msg"`
}
