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

    def handle_error(self, response):
        raise Exception(response.status_code)

    def process_request(self, method, url, body):
        # include here additional authentication headers
        return method(url, json=body)

    def send(self, method, url_name, body=None, return_json=True, *url_args):
        # create full url
        url = posixpath.join(self.base_url, self.urls[url_name].format(*url_args))
        # get, post, patch, delete...
        method = getattr(requests, method)

        response = self.process_request(method, url, body)

        # if request is successful - return response
        if response.status_code in [200, 204]:
            return response.json() if return_json else response

        # handle errors
        return self.handle_error(response)

    def get(self, url_name, body=None, return_json=True, *url_args):
        return self.send('get', url_name, body, return_json, *url_args)

    def post(self, url_name, body=None, return_json=True, *url_args):
        return self.send('post', url_name, body, return_json, *url_args)
