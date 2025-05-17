from flask import Flask
from pymongo import MongoClient
from .config import Config
import os

app = Flask(__name__)  
app.config.from_object(Config)


UPLOAD_FOLDER = 'uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


try:
    mongo_client = MongoClient(app.config['MONGO_URI'])
    db = mongo_client[app.config['MONGO_DB_NAME']]
    app.db = db  
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    app.db = None

from app import routes  
