package models

type Message struct {
	Title string `json:"title"`
	Body  string `json:"body"`
}

type CmdResult struct {
	CmdID    int    `json:"id"`
	AgentID  int    `json:"agent_id"`
	ClientID int    `json:"client_id"`
	Cmd      string `json:"cmd"`
	Result   string `json:"result"`
}
