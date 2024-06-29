from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from bicycles.factories import BicycleFactory, BrandFactory
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


class TestBicyclesFixture(TestUserFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand_1 = BrandFactory()
        cls.brand_2 = BrandFactory()
        cls.bicycle_1 = BicycleFactory(brand=cls.brand_1)
        cls.bicycle_2 = BicycleFactory(brand=cls.brand_2)
        cls.bicycle_3 = BicycleFactory(brand=cls.brand_2, available=False)
