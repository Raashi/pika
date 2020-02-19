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
        'countries': '/api/scrapper/countries/',
        'languages': '/api/scrapper/languages/',
        'jobs': '/api/scrapper/jobs/',
        'bases': '/api/scrapper/bases/',
        'persons': '/api/scrapper/persons/',
        'persons-images': '/api/scrapper/persons/images/',
        'movies': '/api/scrapper/movies/',
        'movies-relations': 'api/scrapper/movies/relations/'
    }

    def __init__(self):
        self.token = None

    def login(self):
        response = self.post('login', self.credentials, process_request=False)
        self.token = response['Bearer']

    def handle_error(self, response, url_name, url_args, kwargs):
        if response.status_code == 401:
            # if authentication failed - token expired
            self.login()
            return
        return super().handle_error(response, url_name, url_args, kwargs)

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        if self.token is None:
            # get token if no token provided
            self.login()

        kwargs.update(**{self.authorization_header: self.token})
        return super().process_request(method, url, url_name, data, url_args, kwargs)
