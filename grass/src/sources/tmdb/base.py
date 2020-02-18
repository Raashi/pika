import posixpath
import requests

from utils import get_environ_variable


def init_base_url():
    # TODO: move somewhere else
    return 'https://api.themoviedb.org/3/'


def init_api_key():
    return get_environ_variable('PIKA_TMDB_API_KEY')


def tmdb_send(url_name, *url_format_args, **url_format_kwargs):
    url = posixpath.join(base_url, urls[url_name].format(*url_format_args, **url_format_kwargs))
    url += '?api_key=' + api_key

    response = requests.get(posixpath.join(base_url, url))

    if response.status_code not in [200, 404]:
        # TODO: change class, log error
        raise Exception('Error while requesting tmdb')

    if response.status_code == 404:
        return None

    return response.json()


base_url = init_base_url()
api_key = init_api_key()

urls = {
    'countries': '/configuration/countries',
    'languages': '/configuration/languages',
    'jobs': '/configuration/jobs'
}
