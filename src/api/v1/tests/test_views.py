from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

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
