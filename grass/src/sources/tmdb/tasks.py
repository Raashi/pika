from celery.task import task

from pika import PikaApiClient

from .client import TMDBApiClient
from .movie import send_movies
from .person import send_persons
from .changes import send_changes


@task
def process_movies(movie_ids):
    pika_client = PikaApiClient()
    tmdb_client = TMDBApiClient()
    send_movies(pika_client, tmdb_client, movie_ids)


@task
def process_persons(person_ids):
    pika_client = PikaApiClient()
    tmdb_client = TMDBApiClient()
    send_persons(pika_client, tmdb_client, person_ids)


@task
def process_changes(start_date, end_date):
    pika_client = PikaApiClient()
    tmdb_client = TMDBApiClient()
    send_changes(pika_client, tmdb_client, start_date, end_date)


@task
def startup():
    # 1. load files
    # 2. for each file: scan it - and tasks to ids
    # 3.
    pass
