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

    def handle_error(self, response, url_name, url_args, kwargs):
        if response.status_code == 404 and url_name == 'movie':
            return None
        return super().handle_error(response, url_name, url_args, kwargs)

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        # set api_key
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params'].update(api_key=self.api_key)

        return super().process_request(method, url, url_name, data, url_args, kwargs)
