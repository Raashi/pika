from api.scrapper.serializers import BaseUploadSerializer
from pika.base.models import Keyword, Job, Company, Genre, Collection
from pika.db.models import Language, Country

__all__ = ['LanguageUploadSerializer', 'CountryUploadSerializer', 'KeywordUploadSerializer', 'JobUploadSerializer',
           'CompanyUploadSerializer', 'GenreUploadSerializer', 'CollectionSerializer']


class LanguageUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'rus_name']


class CountryUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'rus_name']


class KeywordUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']


class JobUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Job
        fields = ['department', 'name', 'rus_name']
        lookup_fields = ['name']


class CompanyUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'rus_name', 'description', 'rus_description', 'headquarters', 'homepage',
                  'origin_country', 'parent_company', 'logo']


class GenreUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'rus_name']


class CollectionSerializer(BaseUploadSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'rus_name', 'poster', 'backdrop', 'overview', 'rus_overview']
