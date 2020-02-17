from copy import deepcopy

from rest_framework.reverse import reverse

from pika.db.models import Country, Language
from pika.base.models import Genre, Keyword, Company

from testing.api.scrapper import ScrapperBaseTestCase
from testing.api.scrapper.templates import movie


class MovieUploadTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:movies')
    example = {'items': deepcopy(movie)}
    required_fields = {'id', 'title'}

    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(id=1, name='genre')
        cls.keyword = Keyword.objects.create(id=1, name='keyword')
        cls.company = Company.objects.create(id=1, name='company')
        cls.russia = Country.objects.create(id='RU', name='russia')
        cls.russian = Language.objects.create(id='ru', name='russian')

        super().setUpTestData()

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)
