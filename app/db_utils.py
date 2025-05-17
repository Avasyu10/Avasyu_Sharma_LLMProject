from pymongo import MongoClient
from flask import current_app

def get_vector_db():
    if 'vector_db' not in current_app.__dict__:
        try:
            mongo_client = MongoClient(current_app.config['MONGO_URI'])
            db = mongo_client[current_app.config['MONGO_DB_NAME']]
            current_app.vector_db = db  
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            current_app.vector_db = None
    return current_app.vector_db
