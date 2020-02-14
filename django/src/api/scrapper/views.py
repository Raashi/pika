from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.fields import Field
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from pika.tokens.models import ScrapperAccessToken
from .serializers import LoginSerializer, BaseListSerializer

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


class BaseScrapperUploadView(GenericAPIView):
    parser_classes = [JSONParser]
    authentication_classes = [ScrapperAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if 'items' not in data:
            raise ValidationError({'items': Field.default_error_messages['required']})

        # serializer = self.get_serializer_class()(data=request.data['items'], many=True)
        serializer = BaseListSerializer(data=request.data['items'], child=self.get_serializer_class()())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)


class LoginView(GenericAPIView):
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(True)

        user = serializer.validated_data['user']

        token, _ = ScrapperAccessToken.get_or_create(user.id)

        return Response(data={'Bearer': token}, status=200)
