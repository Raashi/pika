from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.fields import Field


class BaseScrapperUploadView(GenericAPIView):
    parser_classes = ['rest_framework.parsers.JSONParser']
    # TODO: change auth and permission classes in order to provide security between scrapper and django services
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    def post(self, request):
        data = request.data
        if 'items' not in data:
            raise ValidationError({'items': Field.default_error_messages['required']})

        serializer = self.get_serializer_class()(data=request.data['items'], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)
