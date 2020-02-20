from copy import deepcopy


def get_template(template, **kwargs):
    data = deepcopy(template)
    data.update(kwargs)
    return data


genre = {
    'id': 1,
    'name': 'genre',
    'rus_name': 'rus genre'
}

keyword = {
    'id': 1,
    'name': 'keyword'
}

job = {
    'name': 'job',
    'rus_name': 'rus job',
    'department': 'Art'
}

company = {
    'id': 1,
    'name': 'company',
    'rus_name': 'rus_company',
    'description': 'description',
    'rus_description': 'rus description',
    'headquarters': 'headquarters',
    'homepage': 'http://google.com',
    'origin_country': 'RU',
    'parent_company': None,
    'logo': '/logo.png'
}

collection = {
    'id': 1,
    'name': 'collection',
    'rus_name': 'rus collection',
    'poster': '/poster.png',
    'backdrop': '/backdrop.png',
    'overview': 'overview',
    'rus_overview': 'rus overview'
}

video = {
    'tmdb_id': 1,
    'size': 360,
    'type': 1,
}


def get_video_template(**kwargs):
    data = deepcopy(video)
    data.update(kwargs)
    return data


review = {
    'tmdb_id': 1,
    'content': 'test'
}


def get_review_template(**kwargs):
    data = deepcopy(review)
    data.update(kwargs)
    return data


person = {
    'id': 1,
    'imdb_id': 'tt1234567',
    'name': 'test',
    'rus_name': 'rus_test',
    'gender': 0,
    'birthday': '2000-01-31',
    'deathday': '2000-01-31',
    'known_for_department': 'Crew',
    'biography': 'test biography',
    'rus_biography': 'rus test biography',
    'popularity': '2.34',
    'profile': '/sifdksjfsdkf.jpg',
    'adult': True,
    'homepage': 'http://google.com',
}


def get_person_template(**kwargs):
    data = deepcopy(person)
    data.update(kwargs)
    return data


movie = {
    'id': 1,
    'imdb_id': 'tt1234567',
    'title': 'test',
    'rus_title': 'тест',
    'overview': 'test overview',
    'rus_overview': 'rus test_overview',
    'tagline': 'test tagline',
    'rus_tagline': 'rus test tagline',
    'homepage': 'http://google.com',
    'rus_homepage': 'http://google.ru',
    'adult': True,
    'budget': 2000000000,
    'popularity': '2.89',
    'runtime': 23,
    'revenue': 2000000000,
    'vote_average': '2.34',
    'vote_count': 43434,
    'release_date': '2020-01-31',
    'status': 4,
    'poster': 'poster.png',
    'backdrop': 'backdrop.png',
    'original_language': 'ru',
    'collection': None,

    # m2m - require additional entities already created
    'genres': [1],
    'production_companies': [1],
    'keywords': [1],
    'production_countries': ['RU'],
    'spoken_languages': ['ru'],
}


def get_movie_template(**kwargs):
    data = deepcopy(movie)
    data.update(kwargs)
    return data


release = {
    'movie': 1,
    'type': 1,
    'date': '2020-02-17T12:08:43.366501',
    'country': 'RU'
}

participant = {
    'movie': 1,
    'tmdb_credit_id': '12345',
    'person': 1,
    'job': 'job',
    'character': 'character',
    'rus_character': 'rus character'
}
