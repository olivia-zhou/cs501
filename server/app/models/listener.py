##from lecture slides, refrenced 0xRick c2 code

import sqlite3
from flask import Flask, request, jsonify
import threading
import os, sys, random, string
import agents
import multiprocessing as mp
from multiprocessing import Process
import requests 



class FlaskListener():
    """控制端表"""
    
    c2_server = "http://127.0.0.1:5000"
    lock = mp.Lock()
    implant_lock = mp.Lock()
    TASKS = []
    AGENTS = []
    path = "data/listeners/{__name__}/"

    app = Flask(__name__)
    encryptionkey = None
    
    
    def __init__(self, name, port, ip):
        #identifying itself
        self.tablename = 'clients'
        self.name = name
        self.port = port
        self.ipaddress = ip
        self.createfolders()
        self.encryptionkey()


    @app.route("/tasks", methods=["GET"])
    def download_tasks():
        global TASKS
        lock.acquire()
        try:
            batch = "\n".join(TASKS[:5])
            TASKS = TASKS[5:]
        finally:
            lock.release()
        return batch 

    @app.route("/response", methods=["POST"])
    def print_response():
        print(request.data.decode())
        return ""

    @app.route("/queue")
    def print_queue():
        return jsonify(TASKS)

    @app.route("/secret", methods=["POST"])
    def add_request():
        r = request.json
        lock.acquire()
        try:
            for cmd in r:
                TASKS.append(cmd)
        finally:
            lock.release()
        print("Queued up ", r)
        return "True"

    @app.route("/register", methods=['POST'])
    def addAgent(self, client_id):
        #get agent object from pipe
        agent = agents(self.encryptionkey)
        #addtodatabase(agent)
        return

    def encryptionkey(self):
        if self.encryptionkey == None:
            self.encryptionkey = getencryptionkey()
        return self.encryptionkey
            
    
    def run(self):
        self.app.run(port=self.port, host=self.ipaddress)
        return
        
    def startprocess(self):
        ###from 0xRick
        self.server = Process(self.run)
    
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None
    
        self.thread = threading.Thread(name = self.name,
                                           target = self.server.start,
                                           args = ())
        self.thread.thread = True
        self.thread.start()
    
        self.isRunning = True
    
    def stopprocess(self):
        self.server.terminate()
        self.server = None
        self.thread = None
        self.isRunning = False
        
        
        
        
        
        
        
        
        
        
        
        
    