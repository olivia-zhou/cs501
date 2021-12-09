from flask import Flask


class testclass:
    
    app = Flask(__name__)
    
    def __init__(self, value):
        print("testing")
    
    def getapp(self):
        return self.app
    
    @app.route("/response", methods=["POST", "GET"])
    def print_response(self):
        print("hello world")
        self.returnval = "testing :D"
        return self.returnval