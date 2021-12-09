from flask import Flask


class testclass:
    
    app = Flask(__name__)
    
    def getapp(self):
        return self.app
    
    @app.route("/response", methods=["POST", "GET"])
    def print_response():
        print("hello world")
        return "testing :D"