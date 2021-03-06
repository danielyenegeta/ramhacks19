from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import boto3, botocore
import driver
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object('config')
db = SQLAlchemy(app)
app.config["DIRECTORY"] = '964222500494.s3-control.us-east-1.amazonaws.com'

@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/howitworks/')
def howitworks():
    return render_template('/howitworks.html')

@app.route('/whomadethis/')
def whomadethis():
    return render_template('/whomadethis.html')

@app.route('/getreport/<filename>/')
def download(filename):
    BUCKET_NAME = 'danielyenegeta.com' # replace with your bucket name
    driver.main(filename)
    KEY = filename+".pdf" # replace with your object key

    # Create an S3 client
    s3 = boto3.client('s3')
    s3.upload_file(KEY, BUCKET_NAME, KEY)
    os.remove(KEY)


    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, filename+'report.pdf')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    return render_template('/home.html')

if __name__ == '__main__':
    app.run(debug=True)
