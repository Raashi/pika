import os
import posixpath
import requests


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
        return method(url, data=data, **kwargs)

    def create_url(self, url_name, url_args=None):
        sub_url = self.urls[url_name]
        if url_args is not None:
            sub_url = sub_url.format(*url_args)
        return posixpath.join(self.base_url, sub_url)

    def send(self, method, url_name, data=None, return_json=True, process_request=True, url_args=None, **kwargs):
        # create full url
        url = self.create_url(url_name, url_args)
        # get, post, patch, delete...
        method = getattr(requests, method)
        # set default 'json' format
        kwargs.setdefault('format', 'json')

        # recursion avoid
        if process_request:
            response = self.process_request(method, url, url_name, data, url_args, kwargs)
        else:
            response = method(url, data=data, **kwargs)

        # if request is successful - return response
        if response.status_code in [200, 204]:
            return response.json() if return_json and response.status_code == 200 else response

        # handle errors
        return self.handle_error(response, url_name, url_args, kwargs)

    def get(self, url_name, data=None, return_json=True, process_request=True, *url_args, **request_kwargs):
        return self.send('get', url_name, data, return_json, process_request, *url_args, **request_kwargs)

    def post(self, url_name, data=None, return_json=True, process_request=True, *url_args, **request_kwargs):
        return self.send('post', url_name, data, return_json, process_request, *url_args, **request_kwargs)
