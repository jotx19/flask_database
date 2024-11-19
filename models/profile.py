# models/profile.py
from datetime import datetime
from bson import ObjectId
from .base import BaseModel


class ProfileModel(BaseModel):
    def get_collection(self):
        return self.db.profiles

    def create_profile(self, user_id, username):
        profile_data = {
            'user_id': user_id,
            'username': username,
            'bio': '',
            'profile_picture': None,
            'watch_list': [],
            'favorite_genres': [],
            'total_reviews': 0,
            'avg_rating': 0.0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.create(profile_data)

    def get_by_user_id(self, user_id):
        return self.collection.find_one({'user_id': user_id})

    def update_profile(self, user_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'user_id': user_id},
            {'$set': update_data}
        )

    def update_watch_list(self, user_id, movie_data, action='add'):
        if action == 'add':
            return self.collection.update_one(
                {'user_id': user_id},
                {'$addToSet': {'watch_list': {
                    'movie_id': movie_data['imdbID'],
                    'title': movie_data['Title'],
                    'poster': movie_data['Poster'],
                    'year': movie_data['Year'],
                    'added_at': datetime.utcnow()
                }}}
            )
        else:  # remove
            return self.collection.update_one(
                {'user_id': user_id},
                {'$pull': {'watch_list': {'movie_id': movie_data['imdbID']}}}
            )

    def update_review_stats(self, user_id, new_rating):
        profile = self.get_by_user_id(user_id)
        current_total = profile['total_reviews']
        current_avg = profile['avg_rating']
        
        new_total = current_total + 1
        new_avg = ((current_avg * current_total) + new_rating) / new_total
        
        return self.update_profile(user_id, {
            'total_reviews': new_total,
            'avg_rating': round(new_avg, 2)
        })
    