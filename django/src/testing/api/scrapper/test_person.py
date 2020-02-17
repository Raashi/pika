from copy import deepcopy

from rest_framework.reverse import reverse

from pika.person.models import Person, PersonTMDBImage

from . import ScrapperBaseTestCase


class PersonUploadTestCase(ScrapperBaseTestCase):
    url = reverse('scrapper:person')

    example = {
        'items': [
            {
                'id': 1,
                'imdb_id': 'tt1234567',
                'name': 'test',
                'rus_name': 'rus_test',
                'gender': 0,
                'birthday': '2000-01-31',
                'deathday': '2000-01-31',
                'known_for_department': 'Crew',
                'biography': 'test biography',
                'rus_biography': 'rus test biography',
                'popularity': '2.34',
                'profile': '/sifdksjfsdkf.jpg',
                'adult': True,
                'homepage': 'http://google.com',
                'images': [
                    {
                        'path': '/somepath.png',
                        'aspect_ratio': '4.38',
                        'width': 20,
                        'height': 20,
                        'vote_average': 1.23,
                        'vote_count': 12
                    }
                ]
            }
        ]
    }

    def test_security(self):
        self.post(self.url, self.example, auth_token=self.NO_TOKEN, expected_status=403)

    def test_upload(self):
        # test required fields
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), {'id', 'name', 'images'})

        self.post(self.url, self.example, expected_status=204)

        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(PersonTMDBImage.objects.count(), 1)

    def test_upload_multiple(self):
        self.example['items'].append(deepcopy(self.example['items'][0]))

        # these persons equal by id and imdb_id
        self.post(self.url, self.example, expected_status=400)

        # change id of second person
        self.example['items'][1]['id'] = 2
        # still error - imdb_id are equal
        self.post(self.url, self.example, expected_status=400)

        # change imdb_id of second_person (Nones are ok), but persons still have non-unique images
        self.example['items'][1]['imdb_id'] = None
        self.post(self.url, self.example, expected_status=400)

        # now images are different
        self.example['items'][1]['images'][0]['path'] = 'another path'
        self.post(self.url, self.example, expected_status=204)

        # for sure add another None value
        self.example['items'].append(deepcopy(self.example['items'][1]))
        self.example['items'][2]['id'] = 3
        self.example['items'][2]['images'][0]['path'] = 'one more path'

        # also make some updates
        self.example['items'][0]['biography'] = 'changed'
        self.example['items'][1]['images'].append(deepcopy(self.example['items'][1]['images'][0]))
        self.example['items'][1]['images'][-1]['path'] = 'and one more'

        # two equal images
        self.post(self.url, self.example, expected_status=204)

        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(PersonTMDBImage.objects.count(), 4)
