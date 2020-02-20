from utils import get_environ_variable, BaseApiClient


class PikaApiClient(BaseApiClient):
    base_url = get_environ_variable('PIKA_URL')
    authorization_header = 'HTTP_AUTHORIZATION'
    credentials = {
        'username': get_environ_variable('PIKA_SCRAPPER_USERNAME'),
        'password': get_environ_variable('PIKA_SCRAPPER_PASSWORD')
    }

    urls = {
        'login': '/api/scrapper/login',
        'countries': '/api/scrapper/countries',
        'languages': '/api/scrapper/languages',
        'jobs': '/api/scrapper/jobs',
        'bases': '/api/scrapper/bases',
        'persons': '/api/scrapper/persons',
        'movies': '/api/scrapper/movies',
        'movies-relations': 'api/scrapper/movies/relations',
        'movies-not-exist': 'api/scrapper/movies/not_exist',
    }

    def __init__(self):
        self.token = None

    def login(self):
        response = self.post('login', self.credentials, process_request=False)
        self.token = response['Bearer']

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        if self.token is None:
            self.login()

        if url_name != 'login':
            kwargs.update(**{self.authorization_header: self.token})

        response = super().process_request(method, url, url_name, data, url_args, kwargs)
        if response.status_code == 403:
            self.login()

        return super().process_request(method, url, url_name, data, url_args, kwargs)
