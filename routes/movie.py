from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import requests

movie_bp = Blueprint('movie', __name__)

MOVIE_API_URL = 'http://www.omdbapi.com/?apikey=b24150c3'

class Movie:
    @staticmethod
    def fetch_movies(query='', genres=None):
        genre_filter = ''
        if genres:
            genre_filter = '&'.join([f'genre={genre}' for genre in genres])
        url = f'{MOVIE_API_URL}&s={query}&{genre_filter}'
        response = requests.get(url)
        return response.json().get('Search', []) if response.status_code == 200 else []

    @staticmethod
    def fetch_movie_details(movie_id):
        response = requests.get(f'{MOVIE_API_URL}&i={movie_id}')
        return response.json() if response.status_code == 200 else {}

@movie_bp.route('/', methods=['GET', 'POST'])
def index():
    selected_genres = request.form.getlist('genres')  
    search_query = 'batman' 
    if selected_genres:
        movies = Movie.fetch_movies(query=search_query, genres=selected_genres)
    else:
        movies = Movie.fetch_movies(query=search_query)
    return render_template('index.html', movies=movies)

@movie_bp.route('/search', methods=['POST'])
def search_movie():
    search_query = request.form.get('query', '').strip()
    if not search_query:
        flash('Please enter a movie name to search!', 'error')
        return redirect(url_for('movie.index'))
    return redirect(url_for('movie.search_results', query=search_query))

@movie_bp.route('/search_results', methods=['GET'])
def search_results():
    search_query = request.args.get('query', '')
    selected_genres = request.args.getlist('genres')
    movies = Movie.fetch_movies(query=search_query, genres=selected_genres)
    return render_template('search_results.html', movies=movies, query=search_query)

@movie_bp.route('/movie/<movie_id>')
def movie_details(movie_id):
    movie_data = Movie.fetch_movie_details(movie_id)
    return render_template('movie_details.html', movie=movie_data)
