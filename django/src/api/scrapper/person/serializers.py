from api.scrapper.serializers import BaseUploadSerializer
from pika.person.models import Person


class PersonUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Person
        fields = ['id', 'imdb_id', 'name', 'rus_name', 'gender', 'birthday', 'deathday', 'known_for_department',
                  'biography', 'rus_biography', 'popularity', 'profile', 'adult', 'homepage']
