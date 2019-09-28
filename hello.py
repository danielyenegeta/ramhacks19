from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder="templates")
app.config["MONGO_URI"] = "mongodb+srv://ramhacks:ramhackspassword@ramhacks19-shg2d.mongodb.net/test?retryWrites=true&w=majority"
@app.route('/')
def home():
    return render_template("base.html")

@app.route('/howitworks')
def howitworks():
    return render_template("howitworks.html")

@app.route('/whomadethis')
def whomadethis():
    return render_template("whomadethis.html")
