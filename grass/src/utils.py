import os
import requests
import shutil

STORAGE_DIR_NAME = 'storage'
TEMP_DIR_NAME = 'temp'

source_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.dirname(source_dir)
storage_dir = os.path.join(project_dir, STORAGE_DIR_NAME)
temp_dir = os.path.join(storage_dir, TEMP_DIR_NAME)

if not os.path.exists(storage_dir):
    os.mkdir(storage_dir)
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)


def get_environ_variable(name, required=True):
    value = os.environ.get(name, None)

    if value is None and required:
        # TODO: change class
        raise Exception(f'Required environment variable {name} not provided')

    return value


class BaseApiClient:
    base_url = None
    urls = {}

    # shortcut
    @staticmethod
    def get_environ_variable(name, required=True):
        return get_environ_variable(name, required)

    def handle_error(self, response, url_name, url_args, kwargs):
        raise Exception(response.status_code)

    def process_request(self, method, url, url_name, data, url_args, kwargs):
        return method(url, json=data, **kwargs)

    @staticmethod
    def join_urls(base, *args):
        for arg in args:
            if base[-1] == '/' and arg[0] == '/':
                base += arg[1:]
            elif base[-1] != '/' and arg[0] != '/':
                base += '/' + arg
            else:
                base += arg
        return base

    def create_url(self, url_name, url_args=None):
        sub_url = self.urls[url_name]
        if url_args is not None:
            sub_url = sub_url.format(*url_args)
        return self.join_urls(self.base_url, sub_url)

    def send(self, method, url_name, data=None, return_json=True, process_request=True, url_args=None, **kwargs):
        # create full url
        url = self.create_url(url_name, url_args)
        # get, post, patch, delete...
        method = getattr(requests, method)
        # set content type
        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/json'

        # recursion avoid
        if process_request:
            response = self.process_request(method, url, url_name, data, url_args, kwargs)
        else:
            response = method(url, json=data, **kwargs)

        # if request is successful - return response
        if response.status_code in [200, 204]:
            return response.json() if return_json and response.status_code == 200 else response

        # handle errors
        return self.handle_error(response, url_name, url_args, kwargs)

    @classmethod
    def clear_send(cls, method, url, data=None, **kwargs):
        return getattr(requests, method)(url, json=data, **kwargs)

    def get(self, url_name, data=None, return_json=True, process_request=True, *url_args, **request_kwargs):
        return self.send('get', url_name, data, return_json, process_request, *url_args, **request_kwargs)

    def post(self, url_name, data=None, return_json=True, process_request=True, *url_args, **request_kwargs):
        return self.send('post', url_name, data, return_json, process_request, *url_args, **request_kwargs)


def clean_temp_dir():
    shutil.rmtree(temp_dir)
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)


def storage_file_exists(filename):
    return os.path.exists(os.path.join(storage_dir, filename))


def read_from_storage(filename):
    with open(os.path.join(storage_dir, filename)) as f:
        data = f.read()
    return data


def write_to_storage(filename, data):
    with open(os.path.join(storage_dir, filename), 'w') as f:
        f.write(data)


def iter_by_chunks(data, size=1000):
    for idx in range(len(data) // size + 1):
        yield data[idx * size:(idx + 1) * size]
