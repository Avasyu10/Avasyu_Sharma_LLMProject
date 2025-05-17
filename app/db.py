from pymongo import MongoClient
from flask import current_app, g 

def get_db():
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client[current_app.config['MONGO_DB_NAME']]
    return g.db

@current_app.teardown_appcontext
def teardown_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        client = db.client
        client.close()