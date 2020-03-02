import os
import datetime

from celery.task import task

from pika import PikaApiClient
from utils import write_to_storage, read_from_storage, storage_file_exists, iter_by_chunks, temp_dir

from . import download_today_file, read_file
from .configuration import send_jobs, send_countries, send_languages
from .client import TMDBApiClient
from .movie import send_movies
from .person import send_persons
from .changes import send_changes

ROUTINE_FILENAME = 'tmdb_routine.txt'
STARTUP_FILENAME = 'tmdb_startup.txt'
NO_STATE = -1
STARTUP_MOVIE_FILENAME = 'tmdb_startup_movie.txt'
STARTUP_PEOPLE_FILENAME = 'tmdb_startup_person.txt'


def get_last_startup_state():
    if not storage_file_exists(STARTUP_FILENAME):
        return -1
    return int(read_from_storage(STARTUP_FILENAME))


def get_last_movie_count():
    if not storage_file_exists(STARTUP_MOVIE_FILENAME):
        return 0
    return int(read_from_storage(STARTUP_MOVIE_FILENAME))


def get_last_people_count():
    if not storage_file_exists(STARTUP_PEOPLE_FILENAME):
        return 0
    return int(read_from_storage(STARTUP_PEOPLE_FILENAME))


def write_startup_state(state):
    write_to_storage(STARTUP_FILENAME, str(state))


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
    process_changes.delay(today, today)

    write_to_storage(ROUTINE_FILENAME, datetime.datetime.now().isoformat())


@task
def startup():
    if storage_file_exists(ROUTINE_FILENAME):
        last_routine_date = datetime.datetime.fromisoformat(read_from_storage(ROUTINE_FILENAME)).date()
        now = datetime.datetime.now().date()

        # 1 day minus for sure
        if last_routine_date + datetime.timedelta(days=13) <= now:
            process_changes.delay(last_routine_date, now)
            return

    last_startup_state = get_last_startup_state()
    write_startup_state(NO_STATE)

    tmdb_client = TMDBApiClient()
    pika_client = PikaApiClient()

    # send basic configuration
    if last_startup_state < 0:
        send_countries(pika_client, tmdb_client)
        send_languages(pika_client, tmdb_client)
        send_jobs(pika_client, tmdb_client)
    write_startup_state(0)

    # send bases
    print('sending bases')
    if last_startup_state < 1:
        print('sending collections')
        collections_filename = download_today_file(tmdb_client, 'files-collections', 'collections.json')
        collections = [obj for obj in read_file(collections_filename)]
        for chunk in iter_by_chunks(collections):
            pika_client.post('bases', {'genres': [], 'keywords': [], 'companies': [], 'collections': chunk})
        print('sent collections')
    write_startup_state(1)

    if last_startup_state < 2:
        print('sending keywords')
        keywords_filename = download_today_file(tmdb_client, 'files-keywords', 'keywords.json')
        keywords = [obj for obj in read_file(keywords_filename)
                    # TMDB has keyword with empty name (WTF)
                    if obj['name'].strip()]
        for chunk in iter_by_chunks(keywords):
            pika_client.post('bases', {'genres': [], 'keywords': chunk, 'companies': [], 'collections': []})
        print('sent keywords')
    write_startup_state(2)

    if last_startup_state < 3:
        companies_filename = download_today_file(tmdb_client, 'files-companies', 'companies.json')
        companies = [obj for obj in read_file(companies_filename)]
        for chunk in iter_by_chunks(companies):
            pika_client.post('bases', {'genres': [], 'keywords': [], 'companies': chunk, 'collections': []})
        print('sent companies')
    write_startup_state(3)

    movies = None
    if last_startup_state < 4:
        print('sending movies')
        movies_filename = download_today_file(tmdb_client, 'files-movies', 'movies.json')
        movies = [obj for obj in read_file(movies_filename)]
        for chunk in iter_by_chunks(movies):
            pika_client.post('movies', {'items': chunk})
        print('sent movies')
    write_startup_state(4)

    people = None
    if last_startup_state < 5:
        print('sending people')
        people_filename = download_today_file(tmdb_client, 'files-people', 'people.json')
        people = [obj for obj in read_file(people_filename)]
        for chunk in iter_by_chunks(people):
            pika_client.post('people', {'items': chunk})
        print('sent people')
    write_startup_state(5)

    if last_startup_state < 6:
        if movies is None:
            movies_filename = os.path.join(temp_dir, 'movies.json')
            movies = [obj for obj in read_file(movies_filename)]

        print('creating movies tasks')
        count = get_last_movie_count()
        for movie in movies[count:]:
            process_movies.delay(movie['id'])
            count += 1
            if count % 100 == 0:
                write_to_storage(STARTUP_MOVIE_FILENAME, int(count))
        print('created movies tasks')
    write_startup_state(6)

    if last_startup_state < 7:
        if people is None:
            people_filename = os.path.join(temp_dir, 'people.json')
            people = [obj for obj in read_file(people_filename)]

        print('creating people tasks')
        count = get_last_people_count()
        for person in people[count:]:
            process_persons.delay(person['id'])
            count += 1
            if count % 100 == 0:
                write_to_storage(STARTUP_PEOPLE_FILENAME, int(count))
        print('create people tasks')
    write_startup_state(7)

    write_to_storage(STARTUP_FILENAME, datetime.datetime.now().isoformat())
    print('startup done')
