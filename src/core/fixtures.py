from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from bicycles.factories import BicycleFactory, BrandFactory
from orders.factories import RentFactory
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
        cls.user_2 = UserFactory()

        cls.anon_client = APIClient()
        cls.user_client = APIClient()
        cls.user_client_2 = APIClient()
        cls.user_client.force_authenticate(cls.user)
        cls.user_client_2.force_authenticate(cls.user_2)


class TestBicyclesFixture(TestUserFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand_1 = BrandFactory()
        cls.brand_2 = BrandFactory()
        cls.bicycle_1 = BicycleFactory(brand=cls.brand_1)
        cls.bicycle_2 = BicycleFactory(brand=cls.brand_2)
        cls.bicycle_3 = BicycleFactory(brand=cls.brand_2, available=False)


class TestRentsFixture(TestBicyclesFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rent_1 = RentFactory(
            renter=cls.user_2,
            bicycle=cls.bicycle_2,
        )
