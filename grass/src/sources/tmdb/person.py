from .movie import send_movies


MINIMUM_PERSON_POPULARITY = 0.1


def get_person(tmdb_client, person_id):
    person_eng = tmdb_client.get('person', url_args=[person_id], params={'append_to_response': 'movie_credits'})
    if person_eng['popularity'] < MINIMUM_PERSON_POPULARITY:
        return

    person = {
        'id': person_eng['id'],
        'imdb_id': person_eng['imdb_id'],
        'name': person_eng['name'],
        'rus_name': '',
        'gender': person_eng['gender'],
        'birthday': person_eng['birthday'],
        'deathday': person_eng['deathday'],
        'known_for_department': person_eng['known_for_department'],
        'biography': person_eng['biography'],
        # TODO: decide it is worth it to make additional request just for biography
        'rus_biography': '',
        'popularity': person_eng['popularity'],
        'profile': person_eng['profile_path'],
        'adult': person_eng['adult'],
        'homepage': person_eng['homepage'],
    }

    participants = [
        {'movie': credit['id'], 'tmdb_credit_id': credit['credit_id'], 'person': person['id'], 'job': 'Actor',
         'character': credit['character'], 'rus_character': ''}
        for credit in person_eng['movie_credits']['cast']
    ] + [
        {'movie': credit['id'], 'tmdb_credit_it': credit['credit_id'], 'person': person['id'], 'job': credit['job']}
        for credit in person_eng['movie_credits']['crew']
    ]

    return {
        'person': person,
        'participants': participants,
    }


def send_persons(pika_client, tmdb_client, person_ids):
    persons = [get_person(tmdb_client, person_id) for person_id in person_ids]
    persons = list(filter(lambda obj: obj is not None, persons))
    if not len(persons):
        return

    pika_client.post('persons', {'items': [person['person'] for person in persons]})

    participants = [participant for person in persons for participant in person['participants']]

    # populate not existing movies
    movies_ids = [obj['movie'] for obj in participants]
    movies_not_exist = pika_client.post('movies-not-exist', {'items': movies_ids})['items']
    send_movies(pika_client, tmdb_client, movies_not_exist)

    # finally send
    data = {'releases': [], 'videos': [], 'reviews': [], 'participants': participants}
    pika_client.post('movies-relations', data)
