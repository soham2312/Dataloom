from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_PORT = int(os.getenv("PORT"))  # Assuming the port is an integer

try:
    client = MongoClient(DB_URL, DB_PORT)
    db = client['users']
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

user_collection = db['users']
file_collection = db['files']

def get_user(username: str):
    user = db.users.find_one({"username": username})
    return user

def create_user(user_data):
    user_collection.insert_one({
        "username": user_data.username,
        "password": user_data.password
    })

def upload_file_to_database(username: str, filename: str, file_data: bytes):
    file_collection.insert_one({
        "username": username,
        "filename": filename,
        "data": file_data
    })

def get_files_by_username(username: str):
    files = file_collection.find({"username": username})
    return list(files)