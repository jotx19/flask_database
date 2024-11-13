from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        try:
            mongo_connection = os.getenv("MONGO_URI")
            self.client = MongoClient(mongo_connection)
            self.db = self.client.dbtest  # Ensure 'dbtest' matches your MongoDB database name
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")
        except errors.ConnectionError as ce:
            print(f"Failed to connect to MongoDB: {ce}")
    
    def get_users_collection(self):
        try:
            return self.db.users
        except Exception as e:
            print(f"Error accessing 'users' collection: {e}")
            return None
