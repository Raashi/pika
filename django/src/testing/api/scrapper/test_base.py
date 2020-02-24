from copy import deepcopy

from rest_framework.reverse import reverse

from pika.base.models import Genre, Keyword, Company, Collection, Job
from pika.db.models import Country, Language

from . import ScrapperBaseTestCase
from .templates import get_template, genre, keyword, collection, job, company


class CountriesUploadBaseTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:countries')
    required_fields = {'id', 'name'}

    example = {
        'items': [
            {
                'id': 'RU',
                'name': 'Russia',
                'rus_name': 'Россия',
            }
        ]
    }

    def test_security(self):
        self.post(self.url, self.example, auth_token=self.NO_TOKEN, expected_status=403)

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

    def test_upload(self):
        # test correct uploading
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Country.objects.count(), 1)

        # object will be just updated
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Country.objects.count(), 1)

    def test_multiple(self):
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Country.objects.count(), 1)

        self.example['items'][0]['rus_name'] = 'changed'
        self.example['items'].append({
            'id': 'US',
            'name': 'USA',
            'rus_name': 'США'
        })

        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Country.objects.count(), 2)
        self.assertEqual(Country.objects.get(id='RU').rus_name, 'changed')

        # return self.example state back
        self.example['items'].pop(1)

    def test_unique(self):
        self.post(self.url, self.example, expected_status=204)

        # name is not unique no more
        self.example['items'][0]['id'] = 'US'
        self.post(self.url, self.example, expected_status=204)

        self.assertEqual(Country.objects.count(), 2)

        # return class variable state back
        self.example['items'][0]['id'] = 'RU'


class LanguagesUploadBaseTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:languages')
    required_fields = {'id', 'name'}

    example = {
        'items': [
            {
                'id': 'ru',
                'name': 'Russian',
                'rus_name': 'Русский',
            }
        ]
    }

    def test_security(self):
        self.post(self.url, self.example, auth_token=self.NO_TOKEN, expected_status=403)

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

    def test_upload(self):
        # test correct uploading
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Language.objects.count(), 1)

        # object will be just updated
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Language.objects.count(), 1)

    def test_multiple(self):
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Language.objects.count(), 1)

        self.example['items'][0]['rus_name'] = 'changed'
        self.example['items'].append({
            'id': 'en',
            'name': 'English',
            'rus_name': 'Английский'
        })

        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Language.objects.count(), 2)
        self.assertEqual(Language.objects.get(id='ru').rus_name, 'changed')

        # return self.example state back
        self.example['items'].pop(1)


class JobUploadTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:jobs')
    required_fields = {'name', 'department'}
    example = {'items': [get_template(job)]}

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

    def test_upload(self):
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Job.objects.count(), 1)

        # test lookup fields
        self.post(self.url, self.example, expected_status=204)
        self.assertEqual(Job.objects.count(), 1)

    def test_upload_uniqueness(self):
        data = deepcopy(self.example)
        data['items'].append(get_template(job))

        # two equals
        self.post(self.url, data, expected_status=400)

        # change name - no error - one more job (changed, Art)
        data['items'][1]['name'] = 'changed'
        self.post(self.url, data, expected_status=204)

        # now change department - one more job (changed, Visual Effects)
        data['items'][1]['department'] = 'Visual Effects'
        self.post(self.url, data, expected_status=204)

        self.assertEqual(Job.objects.count(), 3)


class TestBasesUploading(ScrapperBaseTestCase):
    url = reverse('scrapper:bases')
    required_fields = {
        'genres': {'id', 'name'},
        'keywords': {'id', 'name'},
        'companies': {'id', 'name'},
        'collections': {'id', 'name'}
    }

    example = {
        'genres': [get_template(genre)],
        'keywords': [get_template(keyword)],
        'companies': [get_template(company)],
        'collections': [get_template(collection)]
    }

    unique_error = {'non_field_errors': [
        'Multiple equal values provided for unique field id with value 1',
        'Multiple equal by lookup fields values provided'
    ]}

    @classmethod
    def setUpTestData(cls):
        cls.russia = Country.objects.create(id='RU', name='russia')
        cls.russian = Language.objects.create(id='ru', name='russian')

        super().setUpTestData()

    def test_required_fields(self):
        self._test_inner_required_fields(self.url, self.required_fields)

    def test_upload(self):
        self.post(self.url, self.example, expected_status=204)

        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Keyword.objects.count(), 1)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Collection.objects.count(), 1)

        # test lookup fields
        data = deepcopy(self.example)
        data['genres'].append(get_template(genre, id=2, name='genre 2'))
        data['keywords'].append(get_template(keyword, id=2, name='keyword 2'))
        data['companies'].append(get_template(company, id=2, name='company 2'))
        data['collections'].append(get_template(collection, id=2, name='collection 2'))
        self.post(self.url, data, expected_status=204)

        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(Keyword.objects.count(), 2)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Collection.objects.count(), 2)

    def test_upload_uniqueness(self):
        data = deepcopy(self.example)
        data['genres'].append(get_template(genre))
        data['keywords'].append(get_template(keyword))
        data['companies'].append(get_template(company))
        data['collections'].append(get_template(collection))

        response = self.post(self.url, data, expected_status=400).json()
        self.assertEqual(response['genres'], self.unique_error)
        self.assertEqual(response['keywords'], self.unique_error)
        self.assertEqual(response['companies'], self.unique_error)
        self.assertEqual(response['collections'], self.unique_error)
