import datetime

from .movie import send_movies
from .person import send_persons


def get_changes_from_response(response):
    return [obj['id'] for obj in response['results']][:10]


def get_changes(tmdb_client, start_date, end_date, url_name):
    end_date = end_date + datetime.timedelta(days=1)
    params = {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), 'page': '1'}

    response = tmdb_client.get(url_name, params=params)
    changes = get_changes_from_response(response)
    total_pages = response['total_pages']

    for page in range(2, total_pages):
        params.update(page=page)
        response = tmdb_client.get(url_name, params=params)
        changes.append(get_changes_from_response(response))

    return changes


def get_changed_movies(tmdb_client, start_date, end_date):
    return get_changes(tmdb_client, start_date, end_date, 'movie-changes')


def get_changed_persons(tmdb_client, start_date, end_date):
    return get_changes(tmdb_client, start_date, end_date, 'person-changes')


def send_changes(pika_client, tmdb_client, start_date, end_date):
    movie_ids = get_changed_movies(tmdb_client, start_date, end_date)
    person_ids = get_changed_persons(tmdb_client, start_date, end_date)

    # TODO: move it somewhere
    block_size = 100
    for idx in range(len(movie_ids) // block_size + 1):
        send_movies(pika_client, tmdb_client, movie_ids[idx * block_size:(idx + 1) * block_size])
    for idx in range(len(person_ids) // block_size + 1):
        send_persons(pika_client, tmdb_client, person_ids[idx * block_size:(idx + 1) * block_size])
