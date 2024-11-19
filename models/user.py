# models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .base import BaseModel

class UserModel(BaseModel):
    def get_collection(self):
        return self.db.users

    def create_user(self, username, email, password):
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.utcnow(),
            'profile_picture': None,
            'bio': '',
            'favorite_movies': []
        }
        return self.create(user_data)

    def find_by_username(self, username):
        # Using the username index
        return self.collection.find_one({'username': username})

    def find_by_email(self, email):
        # Using the email index
        return self.collection.find_one({'email': email})

    def update_profile(self, user_id, profile_data):
        return self.update(user_id, profile_data)

    def add_favorite_movie(self, user_id, movie_id, movie_title):
        return self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$addToSet': {'favorite_movies': {
                'movie_id': movie_id,
                'movie_title': movie_title,
                'added_at': datetime.utcnow()
            }}}
        )
    
    def verify_password(self, user, password):
        """
        Verifies the password against the stored hash.
        """
        return check_password_hash(user['password'], password)
    
    

