import os
APP_NAME  = os.environ.get("APP_NAME", "")
APP_HOST  = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT  = int(os.environ.get("APP_PORT", 80))
DEBUG  = [True, False][int(os.environ.get("DEBUG", 0))]

try:
    from local_settings import *
except:
    pass

from flask import Flask, request, abort, render_template,redirect, url_for 

app = Flask(__name__)

# Variables about mongodb 
import os
MONGODB_HOST = os.environ.get("MONGODB_HOST", "54.236.77.163") 
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017)) 
MONGODB_USER = os.environ.get("MONGODB_USER", "root") 
MONGODB_PWD = os.environ.get("MONGODB_PWD", "example") 
DB = os.environ.get("DB", "admin") 


try: 
    from local_settings import * 
except: 
    pass 

from pymongo import MongoClient 

mcli = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT) 
db = mcli[DB] 

  
if MONGODB_USER!="": 
    db.authenticate(MONGODB_USER,MONGODB_PWD) 
    try:
        db.create_collection("guestbook") 
    except Exception as e:
        print("error = ",e)

  

db = mcli["guestbook"] 

sample_data = [
    {"text":"message1"},
    {"text":"message2"},
    {"text":"message3"},
    {"text":"message4"},
]

if db.messages.find().count() == 0:
    db.messages.insert(sample_data)



@app.route('/')
def index():
    return render_template("home.html",
        title = 'Home',
        app_name = APP_NAME,
        data = list(db.messages.find()))

@app.route('/submit', methods=['POST'])
def submit():
    raw = {"text":request.form['message'],"author":request.form['name']}
    db.messages.insert(raw)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = DEBUG
    app.run(host=APP_HOST, port=APP_PORT)