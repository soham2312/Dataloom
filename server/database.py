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
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

user_collection = db['users']

def get_user(username: str):
    user = db.users.find_one({"username": username})
    return user

def create_user(user_data):
    user_collection.insert_one({
        "username": user_data.username,
        "password": user_data.password
    })