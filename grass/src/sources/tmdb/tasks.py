import datetime

from celery.task import task

from pika import PikaApiClient
from utils import write_to_storage, read_from_storage, storage_file_exists, iter_by_chunks

from . import download_today_file, read_file
from .configuration import send_jobs, send_countries, send_languages
from .client import TMDBApiClient
from .movie import send_movies
from .person import send_persons
from .changes import send_changes

routine_filename = 'tmdb_routine.txt'


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
def routine():
    today = datetime.date.today()
    process_changes.apply_async(today, today)

    write_to_storage(routine_filename, datetime.datetime.now().isoformat())


@task
def startup():
    if storage_file_exists(routine_filename):
        last_routine_date = datetime.datetime.fromisoformat(read_from_storage(routine_filename)).date()
        now = datetime.datetime.now().date()

        # 1 day minus for sure
        if last_routine_date + datetime.timedelta(days=13) >= now:
            process_changes.apply_async(last_routine_date, now)
            return

    tmdb_client = TMDBApiClient()
    pika_client = PikaApiClient()

    # send basic configuration
    send_countries(pika_client, tmdb_client)
    send_languages(pika_client, tmdb_client)
    send_jobs(pika_client, tmdb_client)

    # send bases
    print('sending bases')
    collections_filename = download_today_file(tmdb_client, 'files-collections', 'collections.json')
    collections = [obj for obj in read_file(collections_filename)]
    for chunk in iter_by_chunks(collections):
        pika_client.post('bases', {'genres': [], 'keywords': [], 'companies': [], 'collections': chunk})
    print('sent collections')

    keywords_filename = download_today_file(tmdb_client, 'files-keywords', 'keywords.json')
    keywords = [obj for obj in read_file(keywords_filename)
                # TMDB has keyword with empty name (WTF)
                if obj['name']]
    print(keywords)
    for chunk in iter_by_chunks(keywords):
        pika_client.post('bases', {'genres': [], 'keywords': chunk, 'companies': [], 'collections': []})
    print('sent keywords')

    companies_filename = download_today_file(tmdb_client, 'files-companies', 'companies.json')
    companies = [obj for obj in read_file(companies_filename)]
    for chunk in iter_by_chunks(companies):
        pika_client.post('bases', {'genres': [], 'keywords': [], 'companies': chunk, 'collections': []})
    print('sent companies')
