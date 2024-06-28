from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from users.factories import UserFactory

User = get_user_model()


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = "example@exampl.com"
        cls.username = "example"
        cls.password = "example"

        cls.user = UserFactory()

        cls.anon_client = APIClient()
        cls.user_client = APIClient()
        cls.user_client.force_authenticate(cls.user)
