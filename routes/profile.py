# routes/profile.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from routes.auth import login_required
from bson import ObjectId
import gridfs
from werkzeug.utils import secure_filename
import os

profile_bp = Blueprint('profile', __name__)

# GridFS setup
# fs = gridfs.GridFS(current_app.db)

@profile_bp.route('/profile/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    if request.method == 'POST':
        profile_data = {
            'bio': request.form.get('bio', ''),
            'profile_picture': request.form.get('profile_picture', ''),
            'favorite_genres': request.form.getlist('favorite_genres'),
        }
        current_app.profile_model.update_profile(session['user_id'], profile_data)
        flash('Profile created successfully!', 'success')
        return redirect(url_for('profile.view_profile', user_id=session['user_id']))
    
    # Render the form for profile creation
    return render_template('profile/create_profile.html')

@profile_bp.route('/profile/<user_id>')
def view_profile(user_id):
    profile = current_app.profile_model.get_by_user_id(user_id)
    if not profile:
        flash('Profile not found!', 'error')
        return redirect(url_for('movie.index'))
    
    user_reviews = current_app.review_model.find_by_user(user_id)
    
    return render_template('profile/view_profile.html',
                         profile=profile,
                         reviews=user_reviews)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        update_data = {
            'bio': request.form.get('bio', ''),
            'favorite_genres': request.form.getlist('favorite_genres'),
        }
        
        if request.form.get('profile_picture'):
            update_data['profile_picture'] = request.form.get('profile_picture')
            
        current_app.profile_model.update_profile(session['user_id'], update_data)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile', user_id=session['user_id']))
    
    profile = current_app.profile_model.get_by_user_id(session['user_id'])
    return render_template('profile/edit_profile.html', profile=profile)

@profile_bp.route('/profile/watchlist/add/<movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    movie_data = current_app.movie_provider.get_movie_details(movie_id)
    current_app.profile_model.update_watch_list(session['user_id'], movie_data, 'add')
    flash('Movie added to your watchlist!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))

@profile_bp.route('/profile/watchlist/remove/<movie_id>', methods=['POST'])
@login_required
def remove_from_watchlist(movie_id):
    movie_data = {'imdbID': movie_id}
    current_app.profile_model.update_watch_list(session['user_id'], movie_data, 'remove')
    flash('Movie removed from your watchlist!', 'success')
    return redirect(url_for('profile.view_profile', user_id=session['user_id']))
