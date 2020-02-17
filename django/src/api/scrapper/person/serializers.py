from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields
from pika.person.models import PersonTMDBImage, Person


class PersonImageUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = PersonTMDBImage
        fields = ['person'] + TMDB_image_fields
        lookup_fields = ['path']


class PersonUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Person
        fields = ['id', 'imdb_id', 'name', 'rus_name', 'gender', 'birthday', 'deathday', 'known_for_department',
                  'biography', 'rus_biography', 'popularity', 'profile', 'adult', 'homepage']
