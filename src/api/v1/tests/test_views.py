from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from bicycles.models import Bicycle, Brand
from core.fixtures import TestUserFixture
from users.factories import PASSWORD

User = get_user_model()


class TestUser(TestUserFixture):
    def test_user_registry(self):
        body = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }
        response = self.anon_client.post(
            reverse("registry"), data=body, format="json"
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(User.objects.filter(email=self.email).exists())

    def test_user_login(self):
        data = {"username": self.user.username, "password": PASSWORD}
        response = self.anon_client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue("access" in response.json())
        self.assertTrue("refresh" in response.json())


class BicyclesTests(TestUserFixture):
    def test_get_brands(self):
        response = self.user_client.get(reverse("brands-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Brand.objects.all()))

    def test_get_bicycles(self):
        response = self.user_client.get(reverse("bicycles-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.json()), len(Bicycle.objects.filter(available=True))
        )

    def test_anon_client_has_no_access(self):
        response_1 = self.anon_client.get(reverse("brands-list"))
        self.assertEqual(response_1.status_code, HTTPStatus.UNAUTHORIZED)

        response_2 = self.anon_client.get(reverse("brands-list"))
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)
