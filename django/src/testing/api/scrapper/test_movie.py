from copy import deepcopy

from rest_framework.reverse import reverse

from pika.db.models import Country, Language

from testing.api.scrapper import ScrapperBaseTestCase
from testing.api.scrapper.templates import movie


class MovieUploadTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:movie')
    example = deepcopy(movie)

    @classmethod
    def setUpTestData(cls):
        cls.russia = Country.objects.create(id='RU', name='russia')
        cls.usa = Country.objects.create(id='US', name='usa')
        cls.russian = Language.objects.create(id='ru', name='russian')
        cls.english = Language.objects.create(id='en', name='english')

        super().setUpTestData()

    def test_required_fields(self):
        response = self.post(self.url, self.example, expected_status=400).json()
        print(response)
        self.assertEqual(set(response[0]), set())
