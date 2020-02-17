from api.scrapper.views import BaseScrapperUploadView

from .serializers import PersonUploadSerializer, PersonImageUploadSerializer


class PersonsUploadView(BaseScrapperUploadView):
    serializer_class = PersonUploadSerializer


class PersonsImagesUploadView(BaseScrapperUploadView):
    serializer_class = PersonImageUploadSerializer
