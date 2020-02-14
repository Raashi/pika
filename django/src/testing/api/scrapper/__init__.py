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
