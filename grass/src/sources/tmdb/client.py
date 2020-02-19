import time
import datetime

from utils import get_environ_variable, BaseApiClient


class TMDBApiClient(BaseApiClient):
    base_url = 'https://api.themoviedb.org/3/'
    urls = {
        'countries': '/configuration/countries',
        'languages': '/configuration/languages',
        'jobs': '/configuration/jobs',
        'movie': '/movie/{}',
    }
    api_key = get_environ_variable('PIKA_TMDB_API_KEY')

    response_interval = 1
    last_response_time = None

    def handle_error(self, response, url_name, url_args, kwargs):
        if response.status_code == 404 and url_name == 'movie':
            return None
        return super().handle_error(response, url_name, url_args, kwargs)

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        # set api_key
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params'].update(api_key=self.api_key)

        # balancing requests
        if self.last_response_time is not None:
            sleep_time = (datetime.datetime.now() - self.last_response_time).total_seconds()
            time.sleep(sleep_time)

        response = super().process_request(method, url, url_name, data, url_args, kwargs)
        TMDBApiClient.last_response_time = datetime.datetime.now()

        return response
