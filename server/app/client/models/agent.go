package models

type Agent struct {
	AgentID      int    `json:"id"`
	ComputerName string `json:"computer_name"`
	GUID         string `json:"guid"`
	Username     string `json:"username"`
	IP           string `json:"ip"`
	SleepTime    string `json:"sleep_time"`
	SessionKey   string `json:"session_key"`
	FirstSeen    string `json:"first_seen"`
	LastSeen     string `json:"last_seen"`
	Intergity    string `json:"intergity"`
}
