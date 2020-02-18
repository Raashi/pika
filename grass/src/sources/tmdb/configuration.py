from pika import pika_post

from .base import tmdb_send


def get_countries():
    countries = tmdb_send('countries')
    return [{'id': obj['iso_3166_1'], 'name': obj['english_name']} for obj in countries]


def send_countries():
    countries = get_countries()
    # TODO: log
    pika_post('countries', {'items': countries})


def get_languages():
    languages = tmdb_send('languages')
    return [{'id': obj['iso_639_1'], 'name': obj['english_name']} for obj in languages]


def send_languages():
    languages = get_languages()
    # TODO: log
    pika_post('languages', {'items': languages})
