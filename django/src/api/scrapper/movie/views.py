from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from api.scrapper.views import BaseScrapperUploadView
from pika.movie.models import Movie

from .serializers import *


class MoviesUploadView(BaseScrapperUploadView):
    serializer_class = MovieSerializer


class MoviesRelationsUploadView(BaseScrapperUploadView):
    compositions = [
        ('releases', MovieReleaseDateSerializer),
        ('videos', MovieVideoSerializer),
        ('participants', MovieParticipantSerializer),
        ('reviews', MovieReviewSerializer),
    ]


class MovieNotExistView(BaseScrapperUploadView):
    field = PrimaryKeyRelatedField(queryset=Movie.objects.all())

    def process_uploading(self, request):
        data = request.data
        self.require_fields(data, ['items'])
        if not isinstance(data['items'], list):
            error_msg = ListSerializer.default_error_messages['not_a_list'].format(type(data['items']))
            raise ValidationError({'items': error_msg})

        not_existing_ids = []

        for value in data['items']:
            try:
                self.field.to_internal_value(value)
            except ValidationError:
                not_existing_ids.append(value)

        return not_existing_ids

    def post(self, request):
        ids = self.process_uploading(request)
        return Response(data={'items': ids})
