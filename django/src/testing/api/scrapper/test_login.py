from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse

from . import ScrapperBaseTestCase

UserModel = get_user_model()


class LoginTestCase(ScrapperBaseTestCase):
    auto_use_token = False

    def test(self):
        url = reverse('scrapper:login')
        correct_credentials = {
            'username': self.scrapper.username,
            'password': self.test_password
        }

        # fields are required
        self.post(url, {}, expected_status=400)

        # success login
        response = self.post(url, correct_credentials).json()
        self.assertIn('Bearer', response)
        # test that token was not recreated (it was created in LoggedBaseTestCase)
        self.assertEqual(response['Bearer'], self.token)

        # invalid credentials
        self.post(url, {'username': '***', 'password': '***'}, expected_status=400)
        # invalid password
        self.post(url, {'username': self.scrapper.username, 'password': '***'}, expected_status=400)
        # scrapper is not active
        self.scrapper.is_active = False
        self.scrapper.save()
        self.post(url, correct_credentials, expected_status=400)
        # scrapper is not admin
        self.scrapper.is_admin = False
        self.scrapper.is_active = True
        self.scrapper.save()
        self.post(url, correct_credentials, expected_status=400)
        # check ignoring authentication token if provided (also make scrapper admin again!)
        self.scrapper.is_admin = True
        self.scrapper.save()
        self.post(url, correct_credentials, auth_token=self.token)
