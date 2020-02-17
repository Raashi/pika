from copy import deepcopy

image = {
    'path': 'path.png',
    'aspect_ratio': '4.38',
    'width': 20,
    'height': 20,
    'vote_average': 1.23,
    'vote_count': 12
}

video = {
    'tmdb_id': 1,
    'size': 360,
    'type': 1,
}

review = {
    'tmdb_id': 1,
    'content': 'test'
}


def get_image_template(**kwargs):
    data = deepcopy(image)
    data.update(kwargs)
    return data


def get_video_template(**kwargs):
    data = deepcopy(video)
    data.update(kwargs)
    return data


def get_review_template(**kwargs):
    data = deepcopy(review)
    data.update(kwargs)
    return data


person = {
    'id': 1,
    'name': 'test',
    'images': []
}


def get_person_template(**kwargs):
    data = deepcopy(person)
    data.update(kwargs)
    return data


movie = {
    'items': [
        {
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
            'genres': [
                {'id': 1, 'name': 'comedy'},
                {'id': 2, 'name': 'horror'},
            ],
            'production_companies': [
                {'id': 1, 'name': 'warner'},
                {'id': 2, 'name': 'brothers'},
            ],
            'keywords': [
                {'id': 1, 'name': 'so'},
                {'id': 2, 'name': 'fun'},
            ],
            'production_countries': [
                'RU', 'US'
            ],
            'spoken_languages': ['ru', 'en'],
            'releases': [
                {'type': 1, 'country': 'RU', 'date': '2020-01-31T21:00:00.121212+00:00'},
                {'type': 2, 'country': 'RU', 'date': '2020-01-31T21:00:00.121212+00:00'}
            ],
            'posters': [
                get_image_template(path='1.png'),
                get_image_template(path='2.png'),
            ],
            'backdrops': [
                get_image_template(path='1.png'),
                get_image_template(path='2.png'),
            ],
            'videos': [
                get_video_template(tmdb_id=1),
                get_video_template(tmdb_id=2),
            ],
            'reviews': [
                get_review_template(tmdb_id=1),
                get_review_template(tmdb_id=2),
            ]
        }
    ]
}
