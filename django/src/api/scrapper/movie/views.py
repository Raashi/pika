from api.scrapper.views import BaseScrapperUploadView

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
