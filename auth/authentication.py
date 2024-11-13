from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask import session

class UserAuth:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    def register_user(self, username, email, password):
        if self.users_collection.find_one({"email": email}):
            return False 
        hashed_password = generate_password_hash(password)
        self.users_collection.insert_one({"username": username, "email": email, "password": hashed_password})
        return True

    def login_user(self, email, password):
        user = self.users_collection.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            session["user"] = user["email"]
            return True
        return False
