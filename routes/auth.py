from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from flask import current_app

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = current_app.user_model.find_by_username(username)
        
        if existing_user is None:
            user = current_app.user_model.create_user(
                username=username,
                email=request.form['email'],
                password=request.form['password']
            )
            # Create associated profile
            current_app.profile_model.create_profile(
                user_id=str(user.inserted_id),
                username=username
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('auth.register'))

    # Handle GET request (Show registration form)
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = current_app.user_model.find_by_username(request.form['username'])
        
        if user and current_app.user_model.verify_password(user, request.form['password']):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('movie.index'))
            
        flash('Invalid username/password combination', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))

