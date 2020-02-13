from api.scrapper.views import BaseScrapperUploadView

from .serializers import MovieUploadSerializer


class MovieUploadView(BaseScrapperUploadView):
    serializer_class = MovieUploadSerializer
