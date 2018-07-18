import os
APP_NAME  = os.environ.get("APP_NAME", "")
APP_HOST  = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT  = int(os.environ.get("APP_PORT", 80))
DEBUG  = [True, False][int(os.environ.get("DEBUG", 0))]

try:
    from local_settings import *
except:
    pass

from flask import Flask, request, abort, render_template

app = Flask(__name__)



MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://")
DB = os.environ.get("DB", "az")

from pymongo import MongoClient

mcli = MongoClient(MONGODB_URI)
db = mcli[DB]

sample_data = [{"text":"Hello! Flask!"}, 
                    {"text":"Flask is awesome!"}, 
                    {"text":"Flask is the best!"},
                    {"text":"Hey! Flask is the best!"}]
    
if db.messages.find().count() == 0:
    for raw in sample_data:
        db.messages.insert(raw)


@app.route('/')
def index():
    return render_template("home.html",
        title = 'Home',
        app_name = APP_NAME,
        data = sample_data)


if __name__ == "__main__":
    app.debug = DEBUG
    app.run(host=APP_HOST, port=APP_PORT)