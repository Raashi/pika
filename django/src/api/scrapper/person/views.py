from api.scrapper.views import BaseScrapperUploadView

from .serializers import PersonUploadSerializer, PersonImageUploadSerializer


class PersonUploadView(BaseScrapperUploadView):
    serializer_class = PersonUploadSerializer

    def process_uploading(self, request):
        data = request.data
        self.required_field(data, 'items')

        images_data = []
        images_mapping = {}
        image_idx = 0
        for idx, person_data in enumerate(data['items']):
            self.required_field(person_data, 'images')
            persons_images_data = person_data.pop('images')
            for image_data in persons_images_data:
                images_mapping[image_idx] = idx
                image_idx += 1
                images_data.append(image_data)
        serializer_images = self.init_list_serializer(PersonImageUploadSerializer, images_data)
        serializer_persons = self.init_list_serializer(PersonUploadSerializer, data['items'])

        serializer_persons.is_valid(True)
        serializer_images.is_valid(True)

        persons = serializer_persons.save()
        for idx, image_data in enumerate(serializer_images.validated_data):
            image_data['person'] = persons[images_mapping[idx]]
        serializer_images.save()
