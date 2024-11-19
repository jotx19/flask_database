# models/review.py
from .base import BaseModel
from datetime import datetime
from pymongo import ASCENDING, DESCENDING

class ReviewModel(BaseModel):
    def get_collection(self):
        return self.db.reviews

    def create_review(self, movie_id, movie_title, movie_poster, user_id, username, rating, comment):
        review_data = {
            'movie_id': movie_id,
            'movie_title': movie_title,
            'movie_poster': movie_poster,
            'user_id': user_id,
            'username': username,
            'rating': rating,
            'comment': comment,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'likes': 0,
            'dislikes': 0
        }
        return self.create(review_data)
    

    def update_review(self, review_id, rating, comment):
        update_data = {
            'rating': rating,
            'comment': comment,
            'updated_at': datetime.utcnow()
        }
        return self.update(review_id, update_data)

    def find_by_movie(self, movie_id, skip=0, limit=10, sort_by='created_at'):
        # Uses the compound index (movie_id, created_at, rating)
        return list(self.collection.find(
            {'movie_id': movie_id}
        ).sort(sort_by, DESCENDING).skip(skip).limit(limit))

    def find_by_user(self, user_id, skip=0, limit=10):
        # Uses the compound index (user_id, created_at)
        return list(self.collection.find(
            {'user_id': user_id}
        ).sort('created_at', DESCENDING).skip(skip).limit(limit))

    def get_movie_ratings(self, movie_id):
        # Uses the movie_ratings_summary view
        return self.db.movie_ratings_summary.find_one({'_id': movie_id})

    def search_reviews(self, search_text, skip=0, limit=10):
        # Uses the text index on comments
        return list(self.collection.find(
            {'$text': {'$search': search_text}}
        ).skip(skip).limit(limit))

    def get_latest_reviews(self, limit=10):
        # Uses the created_at index
        return list(self.collection.find().sort('created_at', DESCENDING).limit(limit))

    def get_top_rated_movies(self, limit=10):
        # Uses the compound index (movie_title, rating)
        pipeline = [
            {'$group': {
                '_id': '$movie_id',
                'movie_title': {'$first': '$movie_title'},
                'average_rating': {'$avg': '$rating'},
                'review_count': {'$sum': 1}
            }},
            {'$sort': {'average_rating': -1}},
            {'$limit': limit}
        ]
        return list(self.collection.aggregate(pipeline))
