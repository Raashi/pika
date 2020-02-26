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
        'movie-changes': '/movie/changes',
        'person': '/person/{}',
        'person-changes': '/person/changes'
    }

    files_base_url = 'http://files.tmdb.org/p/exports'
    files_urls = {
        'files-movies': 'movie_ids_{}.json.gz',
        'files-people': 'person_ids_{}.json.gz',
        'files-collections': 'collection_ids_{}.json.gz',
        'files-keywords': 'keyword_ids_{}.json.gz',
        'files-companies': 'production_company_ids_{}.json.gz'
    }

    api_key = get_environ_variable('TMDB_API_KEY')

    response_interval = 1
    last_response_time = None

    files_date_format = '%m_%d_%Y'

    def create_url(self, url_name, url_args=None):
        if url_name in self.files_urls:
            assert len(url_args) == 1
            return self.join_urls(self.files_base_url, self.files_urls[url_name]).format(*url_args)
        return super().create_url(url_name, url_args)

    def handle_error(self, response, url_name, url_args, kwargs):
        if response.status_code == 404 and url_name in ['movie', 'person']:
            return None
        return super().handle_error(response, url_name, url_args, kwargs)

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        # set api_key
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params'].update(api_key=self.api_key)

        # balancing requests
        if self.last_response_time is not None:
            sleep_time = (datetime.datetime.now() - self.last_response_time).microseconds
            time.sleep(max([0, 1 - sleep_time / 1000]))

        response = super().process_request(method, url, url_name, data, url_args, kwargs)
        print(response.request.url)
        TMDBApiClient.last_response_time = datetime.datetime.now()

        return response

    def format_date(self, date):
        return date.strftime(self.files_date_format)
