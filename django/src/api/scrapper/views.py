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

    compositions = None

    def get_serializer_class(self):
        """disable assertion in superclass"""
        return self.serializer_class

    @staticmethod
    def require_fields(data, fields):
        errors = {}
        for field in fields:
            if field not in data:
                errors[field] = Field.default_error_messages['required']

        if errors:
            raise ValidationError(errors)

    def process_list(self, serializer_class, data):
        self.require_fields(data, ['items'])

        serializer = BaseListSerializer(data=data['items'], child=serializer_class())
        serializer.is_valid(True)
        return serializer.save()

    def process_compositions(self, compositions, data):
        serializers = []
        errors = {}

        self.require_fields(data, map(lambda comp: comp[0], compositions))

        for field, serializer_class in compositions:
            serializer = BaseListSerializer(data=data[field], child=serializer_class())

            # put serializers error into sub-json
            is_valid = serializer.is_valid(False)
            if not is_valid:
                errors[field] = serializer.errors

            serializers.append(serializer)

        if errors:
            raise ValidationError(errors)

        for serializer in serializers:
            serializer.save()

    def process_uploading(self, request):
        data = request.data

        serializer_class = self.get_serializer_class()
        compositions = self.compositions
        assert any((serializer_class, compositions))

        if serializer_class:
            return self.process_list(self.get_serializer_class(), data)
        else:
            return self.process_compositions(self.compositions, data)

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

        # TODO: put keyword to settings
        return Response(data={'Bearer': token}, status=200)
