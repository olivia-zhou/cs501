package api

import (
	"controllerEnd/vars"
	"encoding/base64"
	"fmt"
)

func GenToken() string {
	input := fmt.Sprintf("%s:", vars.Token)
	encodeString := base64.StdEncoding.EncodeToString([]byte(input))
	return fmt.Sprintf("Basic %s", encodeString)
}
