from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    test_password = 'testpass123'

    def send(self, command, parameters=None, method=None, auth_token=None, expected_status=status.HTTP_200_OK,
             check_error_code=True, expected_response=None, **kwargs):

        parameters = parameters or {}
        if auth_token:
            prefix = settings.AUTH_HEADER_PREFIX
            self.client.credentials(HTTP_AUTHORIZATION=f'{prefix} {auth_token}')
        else:
            self.client.credentials(HTTP_AUTHORIZATION='')

        send_func = getattr(self.client, method, None)
        if send_func is None:
            raise BaseException('Incorrect method')
        if 'format' not in kwargs:
            kwargs['format'] = 'json'
        response = send_func(command, data=parameters, **kwargs)

        if check_error_code:
            if expected_response is not None:
                self.assertEqual(response.json(), expected_response)
            self.assertEqual(response.status_code, expected_status,
                             msg=response.json() if getattr(response, 'data', None) else '')

        return response

    def post(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
             check_error_code=True, expected_response=None, **kwargs):
        return self.send(command, parameters, 'post', auth_token, expected_status, check_error_code, expected_response,
                         **kwargs)

    def get(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
            check_error_code=True, expected_response=None, **kwargs):
        return self.send(command, parameters, 'get', auth_token, expected_status, check_error_code, expected_response,
                         **kwargs)

    def delete(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
               check_error_code=True, expected_response=None, **kwargs):
        return self.send(command, parameters, 'delete', auth_token, expected_status, check_error_code,
                         expected_response, **kwargs)

    def patch(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
              check_error_code=True, expected_response=None, **kwargs):
        return self.send(command, parameters, 'patch', auth_token, expected_status, check_error_code, expected_response,
                         **kwargs)

    def put(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
            check_error_code=True, expected_response=None, **kwargs):
        return self.send(command, parameters, 'put', auth_token, expected_status, check_error_code, expected_response,
                         **kwargs)

    def assertLenEqual(self, arg, length, msg=None):
        return self.assertEqual(len(arg), length, msg)


class LoggedBaseTestCase(BaseTestCase):
    token = None
    NO_TOKEN = -1
    auto_use_token = True

    def send(self, command, parameters=None, method=None, auth_token=None, expected_status=status.HTTP_200_OK,
             check_error_code=True, expected_response=None, **kwargs):

        if auth_token == self.NO_TOKEN:
            token = None
        elif self.auto_use_token:
            token = self.token if auth_token is None else auth_token
        else:
            token = auth_token

        return super().send(
            command, parameters, method, token, expected_status, check_error_code, expected_response, **kwargs
        )
