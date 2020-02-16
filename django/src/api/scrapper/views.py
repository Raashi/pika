from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.fields import Field
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from pika.tokens.models import ScrapperAccessToken

from .auth import ScrapperAuthentication
from .serializers import LoginSerializer, BaseListSerializer

UserModel = get_user_model()


class BaseScrapperUploadView(GenericAPIView):
    parser_classes = [JSONParser]
    authentication_classes = [ScrapperAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def init_list_serializer(serializer_class, data):
        return BaseListSerializer(data=data, child=serializer_class())

    @staticmethod
    def required_field(data, field):
        if field not in data:
            raise ValidationError({field: Field.default_error_messages['required']})

    def init_serializer(self, request):
        data = request.data
        self.required_field(data, 'items')
        return self.init_list_serializer(self.get_serializer_class(), data['items'])

    def process_uploading(self, request):
        serializer = self.init_serializer(request)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def post(self, request):
        self.process_uploading(request)
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
