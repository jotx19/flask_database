from abc import ABC, abstractmethod
import requests

class MovieProvider(ABC):
    """Abstract base class for movie data providers"""
    @abstractmethod
    def search_movie(self, title):
        pass

    @abstractmethod
    def get_movie_details(self, movie_id):
        pass

class OMDBMovieProvider(MovieProvider):
    """OMDB API Implementation"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://www.omdbapi.com/'

    def search_movie(self, title):
        response = requests.get(
            self.base_url,
            params={'apikey': self.api_key, 't': title}
        )
        return response.json()

    def get_movie_details(self, movie_id):
        response = requests.get(
            self.base_url,
            params={'apikey': self.api_key, 'i': movie_id}
        )
        return response.json()

class TMDBMovieProvider(MovieProvider):
    """TMDB API Implementation"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'

    def search_movie(self, title):
        response = requests.get(
            f"{self.base_url}/search/movie",
            params={
                'api_key': self.api_key,
                'query': title
            }
        )
        data = response.json()
        
        # Convert TMDB format to match OMDB format for consistency
        if data.get('results') and len(data['results']) > 0:
            movie = data['results'][0]
            return {
                'Response': 'True',
                'Title': movie.get('title'),
                'Year': movie.get('release_date', '')[:4],
                'imdbID': str(movie.get('id')),
                'Poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
                'Plot': movie.get('overview'),
                'Response': 'True'
            }
        return {'Response': 'False', 'Error': 'Movie not found!'}

    def get_movie_details(self, movie_id):
        response = requests.get(
            f"{self.base_url}/movie/{movie_id}",
            params={
                'api_key': self.api_key,
                'append_to_response': 'credits'
            }
        )
        movie = response.json()
        
        # Convert TMDB format to match OMDB format
        return {
            'Title': movie.get('title'),
            'Year': movie.get('release_date', '')[:4],
            'imdbID': str(movie.get('id')),
            'Poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
            'Plot': movie.get('overview'),
            'Director': ', '.join(c.get('name') for c in movie.get('credits', {}).get('crew', []) if c.get('job') == 'Director'),
            'Actors': ', '.join(c.get('name') for c in movie.get('credits', {}).get('cast', [])[:4]),
            'Response': 'True'
        }

