from rest_framework.reverse import reverse

from pika.db.models import Country

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
