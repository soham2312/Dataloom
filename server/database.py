from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_PORT = int(os.getenv("PORT"))  # Assuming the port is an integer




# MongoDB connection
try:
    client = MongoClient(DB_URL, DB_PORT)
    db = client['users']
    db=client['files']
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

user_collection = db['users']
files_collection = db['files']

def get_user(username: str):
    user = user_collection.find_one({"username": username})
    return user

def create_user(user_data):
    user_collection.insert_one({
        "username": user_data.username,
        "password": user_data.password
    })

def add_file(file_data):
    # print(file_data['username'])
    files_collection.insert_one({
        "username": file_data['username'],
        "filename": file_data['filename'],
        "file_path": file_data['file_path']
    })


def get_files(username: str):
    files = files_collection.find({"username": username})
    files_list = list(files)
    return files_list