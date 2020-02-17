from copy import deepcopy

from rest_framework.reverse import reverse

from pika.person.models import Person, PersonTMDBImage

from testing.api.scrapper import ScrapperBaseTestCase
from testing.api.scrapper.templates import get_person_template, get_image_template


class PersonUploadTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:persons')
    required_fields = {'id', 'name'}

    example = {'items': [get_person_template()]}

    def test_security(self):
        self.post(self.url, self.example, auth_token=self.NO_TOKEN, expected_status=403)

    def test_upload(self):
        # test required fields
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

        self.post(self.url, self.example, expected_status=204)

        # upload again - it should be just update
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Person.objects.count(), 1)

    def test_upload_multiple(self):
        data = deepcopy(self.example)
        data['items'].append(get_person_template())

        # these persons equal by id and imdb_id
        self.post(self.url, data, expected_status=400)

        # change id of second person
        data['items'][1]['id'] = 2
        # still error - imdb_id are equal
        self.post(self.url, data, expected_status=400)

        # change imdb_id of second_person (Nones are ok)
        data['items'][1]['imdb_id'] = None
        self.post(self.url, data, expected_status=204)

        # for sure add another None value and make some changes
        data['items'].append(get_person_template(id=3, imdb_id=None))
        data['items'][0]['biography'] = 'changed'

        self.post(self.url, data, expected_status=204)

        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(Person.objects.get(id=1).biography, 'changed')


class PersonImageTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:persons-images')
    example = {'items': [get_image_template(person=1)]}

    required_fields = {'person', 'path'}

    @classmethod
    def setUpTestData(cls):
        cls.person = Person.objects.create(**get_person_template(id=1))
        super().setUpTestData()

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

    def test_upload_image(self):
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(PersonTMDBImage.objects.count(), 1)
        self.assertEqual(self.person.images.count(), 1)

    def test_upload_multiple_images(self):
        another_person = Person.objects.create(**get_person_template(id=2, imdb_id=None))

        data = deepcopy(self.example)
        data['items'].append(get_image_template(person=1, path='1'))
        data['items'].append(get_image_template(person=2, path='2'))

        self.post(self.url, data, expected_status=204)

        self.assertEqual(self.person.images.count(), 2)
        self.assertEqual(another_person.images.count(), 1)

        # change person
        data['items'][0]['person'] = 2
        self.post(self.url, data, expected_status=204)

        self.assertEqual(self.person.images.count(), 1)
        self.assertEqual(another_person.images.count(), 2)

    def test_uniqueness(self):
        data = deepcopy(self.example)
        data['items'].append(get_image_template(person=1))

        self.post(self.url, data, expected_status=400)

        # changing person doesn't affect
        Person.objects.create(**get_person_template(id=2, imdb_id=None))
        data['items'][1]['person'] = 2
        self.post(self.url, data, expected_status=400)
