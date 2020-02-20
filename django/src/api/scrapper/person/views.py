from api.scrapper.views import BaseScrapperUploadView

from .serializers import PersonUploadSerializer


class PersonsUploadView(BaseScrapperUploadView):
    serializer_class = PersonUploadSerializer
