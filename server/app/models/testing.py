from flask import Flask

app = Flask(__name__)

@app.route("/response", methods=["POST", "GET"])
def print_response():
        print("hello world")
        returnval = "testing :D"
        return returnval