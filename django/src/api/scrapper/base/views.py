from api.scrapper.views import BaseScrapperUploadView

from .serializers import CountryUploadSerializer, LanguageUploadSerializer


class CountryUploadView(BaseScrapperUploadView):
    serializer_class = CountryUploadSerializer


class LanguageUploadView(BaseScrapperUploadView):
    serializer_class = LanguageUploadSerializer
