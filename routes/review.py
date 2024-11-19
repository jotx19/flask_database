from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from routes.auth import login_required

review_bp = Blueprint('review', __name__)

@review_bp.route('/review/<movie_id>', methods=['POST'])
@login_required
def add_review(movie_id):
    current_app.review_model.create_review(
        movie_id=movie_id,
        movie_title = request.form.get('movie_title'),
        movie_poster = request.form.get('movie_poster'),
        user_id=session['user_id'],
        username=session['username'],
        rating=int(request.form.get('rating')),
        comment=request.form.get('comment')
    )
    flash('Review added successfully!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))

@review_bp.route('/review/edit/<review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = current_app.review_model.find_by_id(review_id)
    
    if review['user_id'] != session['user_id']:
        flash('You can only edit your own reviews!', 'error')
        return redirect(url_for('movie.movie_details', movie_id=review['movie_id']))
    
    if request.method == 'POST':
        current_app.review_model.update_review(
            review_id=review_id,
            rating=int(request.form.get('rating')),
            comment=request.form.get('comment')
        )
        flash('Review updated successfully!', 'success')
        return redirect(url_for('movie.movie_details', movie_id=review['movie_id']))
    
    return render_template('edit_review.html', review=review)

@review_bp.route('/review/delete/<review_id>')
@login_required
def delete_review(review_id):
    review = current_app.review_model.find_by_id(review_id)
    
    if review['user_id'] != session['user_id']:
        flash('You can only delete your own reviews!', 'error')
        return redirect(url_for('movie.movie_details', movie_id=review['movie_id']))
    
    current_app.review_model.delete(review_id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=review['movie_id']))

@review_bp.route('/reviews')
def view_all_reviews():
    limit = int(request.args.get('limit', 10))  # Default to 10 reviews
    page = int(request.args.get('page', 1))    # Default to page 1
    skip = (page - 1) * limit
    reviews = current_app.review_model.get_latest_reviews(limit=limit + skip)[skip:]
    return render_template('all_reviews.html', reviews=reviews)

@review_bp.route('/my_reviews')
@login_required
def my_reviews():
    user_reviews = current_app.review_model.find_by_user(session['user_id'])
    return render_template('my_reviews.html', reviews=list(user_reviews))
