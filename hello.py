from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://ramhacks:ramhackspassword@ramhacks19-shg2d.mongodb.net/test?retryWrites=true&w=majority"
@app.route('/')
def hello():
    return "Hello World!"
