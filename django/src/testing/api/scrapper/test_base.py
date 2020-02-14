from rest_framework.reverse import reverse

from pika.db.models import Country, Language

from . import ScrapperBaseTestCase


class CountriesUploadBaseTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:country')

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

    def test_upload(self):
        # test required fields
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), {'id', 'name'})

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

        self.example['items'][0]['id'] = 'US'
        self.post(self.url, self.example, expected_status=400)

        self.assertEqual(Country.objects.count(), 1)

        # return class variable state back
        self.example['items'][0]['id'] = 'RU'


class LanguagesUploadBaseTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:language')

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

    def test_upload(self):
        # test required fields
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), {'id', 'name'})

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
