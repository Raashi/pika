from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from pika.tokens.models import ScrapperAccessToken

UserModel = get_user_model()


class ScrapperAuthentication(BaseAuthentication):
    # TODO: move to django.settings
    authorization_prefix = 'Bearer'
    error_message = 'Authentication failed. No tokens provided or tokens contains restricted characters'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.authorization_prefix.lower().encode():
            return None

        try:
            token = auth[1].decode()
        except (UnicodeError, IndexError):
            raise AuthenticationFailed(self.error_message)

        return self.authenticate_token(token)

    @classmethod
    def authenticate_token(cls, token):
        scrapper_account_id = ScrapperAccessToken.get_account_id(token)

        if scrapper_account_id is None:
            raise AuthenticationFailed('Invalid Token')

        try:
            user = UserModel.admins().get(id=scrapper_account_id)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed('Invalid Token')  # account was deleted

        ScrapperAccessToken.get_or_create(scrapper_account_id, update_ttl=True)

        return user, token
