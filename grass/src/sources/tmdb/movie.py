MOVIE_STATUS_MAPPING = {
    'Rumored': 1,
    'Planned': 2,
    'In Production': 3,
    'Post Production': 4,
    'Released': 5,
    'Cancelled': 6,
}

VIDEO_TYPE_MAPPING = {
    'Other': 0,
    'Trailer': 1,
    'Teaser': 2,
    'Clip': 3,
    'Featurette': 4,
    'Behind the Scenes': 5,
    'Bloopers': 6,
}


def get_movie(tmdb_client, movie_id):
    movie_eng = tmdb_client.get(
        'movie', url_args=[movie_id], params={'append_to_response': 'keywords,release_dates,videos'}
    )
    if movie_eng is None:
        # 404 - no movie with this id
        return
    movie_rus = tmdb_client.get(
        'movie', url_args=[movie_id], params={'language': 'ru-RU', 'append_to_response': 'videos'}
    )

    # collection
    collection = movie_eng['belongs_to_collection']
    collection_rus = movie_rus['belongs_to_collection']
    if collection is not None:
        collection = {
            'id': collection['id'],
            'name': collection['name'],
            'rus_name': collection_rus['name'],
            'poster': collection['poster_path'],
            'rus_poster': collection_rus['poster_path'],
            'backdrop': collection['backdrop_path'],
            'rus_backdrop': collection_rus['backdrop_path'],
        }

    # genres
    genres_eng = movie_eng['genres']
    genres_rus = movie_rus['genres']
    genres = [{'id': genre_eng['id'], 'name': genre_eng['name'], 'rus_name': genre_rus['name']}
              for genre_eng, genre_rus in zip(genres_eng, genres_rus)]

    # companies
    companies_eng = movie_eng['production_companies']
    companies_rus = movie_rus['production_companies']
    companies = [{'id': company_eng['id'], 'logo': company_eng['logo_path'], 'name': company_eng['name'],
                  'rus_name': company_rus['name'], 'origin_country': company_eng['origin_country']}
                 for company_eng, company_rus in zip(companies_eng, companies_rus)]

    # keywords
    keywords = [{'id': keyword['id'], 'name': keyword['name']} for keyword in movie_eng['keywords']['keywords']
                # TMDB has keyword with empty name (WTF)
                if keyword['name']]

    movie = {
        'id': movie_eng['id'],
        'imdb_id': movie_eng['imdb_id'],

        'title': movie_eng['title'],
        'rus_title': movie_rus['title'],

        'overview': movie_eng['overview'],
        'rus_overview': movie_rus['overview'],

        'tagline': movie_eng['tagline'],
        'rus_tagline': movie_rus['tagline'],

        'homepage': movie_eng['homepage'],
        'rus_homepage': movie_rus['homepage'],

        'adult': movie_eng['adult'],
        'budget': movie_eng['budget'],
        'popularity': movie_eng['popularity'],
        'runtime': movie_eng['runtime'],
        'revenue': movie_eng['revenue'],

        'vote_average': movie_eng['vote_average'],
        'vote_count': movie_eng['vote_count'],

        'genres': [genre['id'] for genre in genres],
        'original_language': movie_eng['original_language'],
        'production_companies': [company['id'] for company in companies],
        'production_countries': [country['iso_3166_1'] for country in movie_eng['production_countries']],
        'spoken_languages': [language['iso_639_1'] for language in movie_eng['spoken_languages']],
        'keywords': [keyword['id'] for keyword in keywords],
        'collection': None if collection is None else collection['id'],

        'release_date': movie_eng['release_date'],
        'status': MOVIE_STATUS_MAPPING[movie_eng['status']],

        'poster': movie_eng['poster_path'],
        'rus_poster': movie_rus['poster_path'],

        'backdrop': movie_eng['backdrop_path'],
        'rus_backdrop': movie_rus['backdrop_path']
    }

    releases = movie_eng['release_dates']['results']
    releases = [
        {'movie': movie['id'], 'type': release['type'], 'date': release['release_date'],
         'country': country['iso_3166_1'], 'note': release.get('note', '')}
        for country in releases if country['iso_3166_1'] in ['RU', 'US'] for release in country['release_dates']
    ]

    videos = [{'tmdb_id': video['id'], 'language': video['iso_639_1'], 'country': video['iso_3166_1'],
               'key': video['key'], 'name': video['name'], 'size': video['size'],
               'type': VIDEO_TYPE_MAPPING[video['type']]}
              for video in movie_eng['videos']['results'] + movie_rus['videos']['results']
              if video['site'] == 'YouTube']

    return {
        'collection': collection,
        'genres': genres,
        'companies': companies,
        'keywords': keywords,
        'movie': movie,
        'releases': releases,
        'videos': videos,
    }


def send_movies(pika_client, tmdb_client, movie_ids):
    movies = [get_movie(tmdb_client, movie_id) for movie_id in movie_ids]
    movies = list(filter(lambda obj: obj is not None, movies))
    if not len(movies):
        return

    genre_ids = set()
    genres = []
    keyword_ids = set()
    keywords = []
    company_ids = set()
    companies = []
    collection_ids = set()
    collections = []
    for movie in movies:
        for genre in movie['genres']:
            if genre['id'] not in genre_ids:
                genre_ids.add(genre['id'])
                genres.append(genre)

        for keyword in movie['keywords']:
            if keyword['id'] not in keyword_ids:
                keyword_ids.add(keyword['id'])
                keywords.append(keyword)

        for company in movie['companies']:
            if company['id'] not in company_ids:
                company_ids.add(company['id'])
                companies.append(company)

        collection = movie['collection']
        if collection is not None and collection['id'] not in collection_ids:
            collection_ids.add(collection['id'])
            collections.append(collection)

    # bases
    bases = {
        'genres': genres,
        'keywords': keywords,
        'companies': companies,
        'collections': collections,
    }
    pika_client.post('bases', bases)

    # movie
    pika_client.post('movies', {'items': [movie['movie'] for movie in movies]})

    # relations
    relations = {
        'releases': list([release for movie in movies for release in movie['releases']]),
        'videos': list([video for movie in movies for video in movie['videos']]),
        'participants': [],
        'reviews': []
    }
    pika_client.post('movies-relations', relations)
