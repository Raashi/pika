from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields, BaseListSerializer
from pika.person.models import PersonTMDBImage, Person


class PersonImageUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = PersonTMDBImage
        fields = ['person'] + TMDB_image_fields
        lookup_fields = ['path']
        extra_kwargs = {'person': {'required': False}}


class PersonUploadSerializer(BaseUploadSerializer):
    images = BaseListSerializer(child=PersonImageUploadSerializer())

    class Meta:
        model = Person
        fields = ['id', 'imdb_id', 'name', 'rus_name', 'gender', 'birthday', 'deathday', 'known_for_department',
                  'biography', 'rus_biography', 'popularity', 'profile', 'adult', 'homepage', 'images']
        child_fields = ['images']

    def save(self, **kwargs):
        images = self.validated_data.pop('images')

        person = super().save()

        self.save_arr_of_related(images, 'images', 'person', person)

        return person
