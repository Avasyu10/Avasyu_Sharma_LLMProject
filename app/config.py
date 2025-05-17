import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') 
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')  
    HUGGING_FACE_API_KEY = os.environ.get('HUGGING_FACE_API_KEY') 
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  