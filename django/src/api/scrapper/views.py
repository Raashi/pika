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

    @staticmethod
    def required_field(data, field):
        if field not in data:
            raise ValidationError({field: Field.default_error_messages['required']})

    def process_list(self, serializer_class, data):
        self.required_field(data, 'items')
        return BaseListSerializer(data=data, child=serializer_class())

    def process_compositions(self, compositions, data):
        serializers = []

        for field, serializer_class in compositions:
            self.required_field(data, field)
            serializer = BaseListSerializer(data=data[field], child=serializer_class())
            serializer.is_valid(True)

            serializers.append(serializer)

        for serializer in serializers:
            serializer.save()

    def process_uploading(self, request):
        data = request.data

        serializer_class = self.get_serializer_class()
        compositions = self.compositions
        assert any((serializer_class, compositions))

        if serializer_class:
            return self.process_list(self.get_serializer_class(), data['items'])
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

        return Response(data={'Bearer': token}, status=200)
