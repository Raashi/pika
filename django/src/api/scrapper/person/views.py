from api.scrapper.views import BaseScrapperUploadView

from .serializers import PersonUploadSerializer


class PersonUploadView(BaseScrapperUploadView):
    serializer_class = PersonUploadSerializer
