###from lecture notes

import requests 

c2_server = "http://127.0.0.1:8080"
path = "/secret"

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