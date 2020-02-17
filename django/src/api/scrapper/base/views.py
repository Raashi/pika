from api.scrapper.views import BaseScrapperUploadView

from .serializers import *


class CountriesUploadView(BaseScrapperUploadView):
    serializer_class = CountryUploadSerializer


class LanguagesUploadView(BaseScrapperUploadView):
    serializer_class = LanguageUploadSerializer


class JobsUploadView(BaseScrapperUploadView):
    serializer_class = JobUploadSerializer


class BasesUploadView(BaseScrapperUploadView):
    compositions = [
        ('genres', GenreUploadSerializer),
        ('keywords', KeywordUploadSerializer),
        ('companies', CompanyUploadSerializer),
    ]
