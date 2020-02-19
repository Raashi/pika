def get_countries(tmdb_client):
    countries = tmdb_client.get('countries')
    return [{'id': obj['iso_3166_1'], 'name': obj['english_name']} for obj in countries]


def send_countries(pika_client, tmdb_client):
    countries = get_countries(tmdb_client)
    # TODO: log
    pika_client.post('countries', {'items': countries})


def get_languages(tmdb_client):
    languages = tmdb_client.get('languages')
    return [{'id': obj['iso_639_1'], 'name': obj['english_name']} for obj in languages]


def send_languages(pika_client, tmdb_client):
    languages = get_languages(tmdb_client)
    # TODO: log
    pika_client.post('languages', {'items': languages})


def get_jobs(tmdb_client):
    jobs = tmdb_client.get('jobs')
    jobs = [{'department': dep['department', 'name': job]} for dep in jobs for job in dep['jobs']]
    return jobs


def send_jobs(pika_client, tmdb_client):
    jobs = get_jobs(tmdb_client)
    # TODO: log
    pika_client.post('jobs', {'items': jobs})
