from flask import Flask
from flask_pymongo import PyMongo
import os
from db.db import DatabaseSetup

from routes.auth import auth_bp
from routes.movie import movie_bp
from routes.review import review_bp
from routes.profile import profile_bp

from models.user import UserModel
from models.review import ReviewModel
from factories.movie_provider_factory import MovieProviderFactory
from models.profile import ProfileModel

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.secret_key = '11dsd215e16e'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # MongoDB Configuration add your mongolink here
    app.config["MONGO_URI"] = 
    
    mongo = PyMongo(app)
    
    print("Setting up database optimizations...")
    db_setup = DatabaseSetup(app.config["MONGO_URI"])
    setup_success = db_setup.setup_all()
    
    if setup_success:
        print("Database optimization completed successfully!")
    else:
        print("Warning: Some database optimizations failed. Application will continue with reduced performance.")
    
    # Initialize models and services
    app.user_model = UserModel(mongo.db)
    app.review_model = ReviewModel(mongo.db)
    app.movie_provider = MovieProviderFactory.get_provider(
        'omdb',
        'b24150c3'
    )
    app.profile_model = ProfileModel(mongo.db)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(profile_bp)
    
    return app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

