from rest_framework.exceptions import ValidationError
from rest_framework.fields import DictField, CharField

from api.scrapper.serializers import BaseUploadSerializer
from pika.base.models import Keyword, Job, Company, Genre, Collection
from pika.db.models import Language, Country

__all__ = ['LanguageUploadSerializer', 'CountryUploadSerializer', 'KeywordUploadSerializer', 'JobUploadSerializer',
           'CompanyUploadSerializer', 'GenreUploadSerializer', 'CollectionSerializer', 'JobField']


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
        lookup_fields = ['name', 'department']


class JobField(DictField):
    child = CharField(allow_blank=False)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return Job.objects.get(name=data['name'], department=data['department'])

    @classmethod
    def validate(cls, data):
        errors = []
        if 'name' not in data:
            errors.append('name sub-field is required')
        if 'department' not in data:
            errors.append('department sub-field is required')
        if errors:
            raise ValidationError(errors)
        return data


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
        fields = ['id', 'name', 'rus_name', 'poster', 'backdrop']
