#db/db.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure

class DatabaseSetup:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.MovieTable

    def setup_indexes(self):
        try:
            # Users collection indexes
            print("Creating user indexes...")
            self.db.users.create_index([("username", ASCENDING)], unique=True)
            self.db.users.create_index([("email", ASCENDING)], unique=True)

            # Reviews collection indexes
            print("Creating review indexes...")
            # Compound index for movie reviews with nested fields
            self.db.reviews.create_index([
                ("movie_id", ASCENDING),
                ("created_at", DESCENDING),
                ("rating", ASCENDING)
            ])
            
            # Compound index for user reviews
            self.db.reviews.create_index([
                ("user_id", ASCENDING),
                ("created_at", DESCENDING)
            ])

            # Index for full-text search on comments
            self.db.reviews.create_index([("comment", "text")])

            # Nested index for movie details
            self.db.reviews.create_index([
                ("movie_title", ASCENDING),
                ("rating", DESCENDING)
            ])

            print("All indexes created successfully!")
            return True

        except OperationFailure as e:
            print(f"Index creation error: {e}")
            return False

    def create_views(self):
        try:
            # Create a view for movie ratings summary
            pipeline = [
                {
                    '$group': {
                        '_id': '$movie_id',
                        'average_rating': {'$avg': '$rating'},
                        'total_reviews': {'$sum': 1},
                        'rating_distribution': {
                            '$push': '$rating'
                        }
                    }
                }
            ]
            
            self.db.command({
                'create': 'movie_ratings_summary',
                'viewOn': 'reviews',
                'pipeline': pipeline
            })
            print("Views created successfully!")
            return True

        except OperationFailure as e:
            print(f"View creation error: {e}")
            return False

    def setup_all(self):
        index_success = self.setup_indexes()
        view_success = self.create_views()
        return index_success and view_success