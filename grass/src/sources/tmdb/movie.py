def get_movie(tmdb_client, movie_id):
    movie = tmdb_client.get('movie', url_args=[movie_id])
