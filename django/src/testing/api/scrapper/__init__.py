from django.contrib.auth import get_user_model

from pika.tokens.models import ScrapperAccessToken

from testing import LoggedBaseTestCase

UserModel = get_user_model()


class ScrapperBaseTestCase(LoggedBaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.scrapper = UserModel.objects.create_superuser(username='scrapper', password=cls.test_password)
        cls.token, _ = ScrapperAccessToken.get_or_create(cls.scrapper.id, update_ttl=True)

    def _test_inner_required_fields(self, url, required_fields):
        response = self.post(url, {}, expected_status=400).json()
        self.assertEqual(set(response), set(required_fields))

        data = {field: [{}] for field in required_fields}
        response = self.post(url, data, expected_status=400).json()
        for field in required_fields:
            self.assertEqual(set(response[field][0]), required_fields[field], field)
