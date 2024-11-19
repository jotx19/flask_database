#factories/movie_provider_factory.py
from services.movie_service import OMDBMovieProvider, TMDBMovieProvider


class MovieProviderFactory:
    @staticmethod
    def get_provider(provider_type, api_key):
        if provider_type.lower() == 'omdb':
            return OMDBMovieProvider(api_key)
        elif provider_type.lower() == 'tmdb':
            return TMDBMovieProvider(api_key)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
        

        