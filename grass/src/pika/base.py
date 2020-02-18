import requests
import posixpath

from utils import get_environ_variable


def get_url():
    return get_environ_variable('PIKA_URL')


def get_credentials():
    return {
        'username': get_environ_variable('PIKA_SCRAPPER_USERNAME'),
        'password': get_environ_variable('PIKA_SCRAPPER_PASSWORD')
    }


base_url = get_url()
credentials = get_credentials()
token = None


def _login():
    response = requests.post(posixpath.join(base_url, urls['login']), json=credentials)
    if response.status_code != 200:
        # TODO: change class
        raise Exception('Cannot login to pika')
    global token
    token = response.json()['Bearer']


def pika_send(_method_name, url_name, body, *url_args, **url_kwargs):
    url = posixpath.join(base_url, urls[url_name].format(*url_args, **url_kwargs))
    method = getattr(requests, _method_name)

    response = method(url, json=body)
    if response.status_code != 200:
        _login()
        response = method(url, json=body)

    if response.status_code == 400:
        # TODO: log, send email/message in vk/discord
        raise Exception(f'Invalid request to pika. Response:\n{response.json()}')
    if response.status_code != 200:
        # TODO: log, send email/message in vk/discord
        raise Exception(f'Something went wrong with pika, status_code={response.status_code}')

    return response.json()


def pika_post(_url, _body):
    return pika_send('post', _url, _body)


urls = {
    'login': '/api/scrapper/login',
    'countries': '/api/scrapper/countries/',
    'languages': '/api/scrapper/languages/',
    'jobs': '/api/scrapper/jobs/',
    'bases': '/api/scrapper/bases/',
    'persons': '/api/scrapper/persons/',
    'persons-images': '/api/scrapper/persons/images/',
    'movies': '/api/scrapper/movies/',
    'movies-relations': 'api/scrapper/movies/relations/'
}
