from rest_framework.serializers import ListSerializer

from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields
from pika.person.models import PersonTMDBImage, Person


class PersonImageUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = PersonTMDBImage
        fields = ['person'] + TMDB_image_fields
        lookup_field = 'path'
        extra_kwargs = {'person': {'required': False}}


class PersonUploadSerializer(BaseUploadSerializer):
    images = ListSerializer(child=PersonImageUploadSerializer, required=True)

    class Meta:
        model = Person
        fields = ['id', 'imdb_id', 'name', 'rus_name', 'gender', 'birthday', 'deathday', 'known_for_department',
                  'biography', 'rus_biography', 'popularity', 'profile', 'adult', 'homepage', 'images']

    def save(self, **kwargs):
        images = self.validated_data.pop('images')

        person = super().save(**kwargs)

        for image_serializer in images:
            image_serializer.validated_data['person'] = person
            image_serializer.save()

        return person
