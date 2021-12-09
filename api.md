## /被控端
```text
暂无描述
```
#### 公共Header参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Query参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Body参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /被控端/被控端保持心跳,汇报状态
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{baseurl}}/api/v1/agent/ping/123455-13213-3123

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "host_name":"mac",
    "ip":"192.168.1.101",
    "session_key":"unkonwn",
    "user_login_name":"rick",
    "intergrity":"root"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /被控端/被控端向服务器上报执行结果
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{baseurl}}/api/v1/agent/result

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "cmd_id":1,
    "result":"root"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /控制端
```text
暂无描述
```
#### 公共Header参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Query参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Body参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /控制端/发送命令
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{baseurl}}/api/v1/client/cmd

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "agent_id":1,
    "cmd":"ls"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /控制端/登录
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{baseurl}}/api/v1/client/login

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "username":"rick",
    "password":"sunshine1"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /控制端/获取被控端列表
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{baseurl}}/api/v1/client/agents

#### 请求方式
> GET

#### Content-Type
> form-data

#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
  "code": 666, 
  "data": [
    {
      "computer_name": "mac", 
      "first_seen": "Thu, 09 Dec 2021 09:22:52 GMT", 
      "guid": "123455-13213-3124", 
      "id": 1, 
      "intergity": "root", 
      "last_seen": "Thu, 09 Dec 2021 09:23:10 GMT", 
      "session_key": "unkonwn", 
      "sleep_time": null
    }, 
    {
      "computer_name": "mac", 
      "first_seen": "Thu, 09 Dec 2021 09:23:24 GMT", 
      "guid": "123455-13213-3123", 
      "id": 2, 
      "intergity": "root", 
      "last_seen": "Thu, 09 Dec 2021 09:23:24 GMT", 
      "session_key": "unkonwn", 
      "sleep_time": null
    }, 
    {
      "computer_name": "mac", 
      "first_seen": "Thu, 09 Dec 2021 09:23:29 GMT", 
      "guid": "123455-13213-3122", 
      "id": 3, 
      "intergity": "root", 
      "last_seen": "Thu, 09 Dec 2021 09:23:29 GMT", 
      "session_key": "unkonwn", 
      "sleep_time": null
    }
  ], 
  "msg": "get all agents success"
}

```