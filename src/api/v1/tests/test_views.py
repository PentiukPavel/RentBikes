from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from bicycles.models import Bicycle, Brand
from core.fixtures import (
    TestBicyclesFixture,
    TestRentsFixture,
    TestUserFixture,
)
from orders.models import Rent
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


class BicyclesTests(TestBicyclesFixture):
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

    def test_rent_bike(self):
        response = self.user_client.post(
            reverse("bicycles-rent", kwargs={"pk": self.bicycle_1.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Rent.objects.filter(
                renter=self.user, bicycle=self.bicycle_1
            ).exists()
        )

        # проверяем, что нельзя арендовать второй велосипед
        response_2 = self.user_client.post(
            reverse("bicycles-rent", kwargs={"pk": self.bicycle_2.id})
        )
        self.assertEqual(response_2.status_code, HTTPStatus.LOCKED)

    def test_anon_client_can_not_rent_bike(self):
        response = self.anon_client.post(
            reverse("bicycles-rent", kwargs={"pk": self.bicycle_2.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class RentsTests(TestRentsFixture):
    def test_get_rents(self):
        response = self.user_client_2.get(reverse("rents-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.json()), len(Rent.objects.filter(renter=self.user_2))
        )

    def test_anon_client_can_not_complete_rent(self):
        response = self.anon_client.post(
            reverse("rents-complete", kwargs={"pk": self.rent_1.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_only_renter_can_complete_rent(self):
        response = self.user_client.post(
            reverse("rents-complete", kwargs={"pk": self.rent_1.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_complete_rent(self):
        response = self.user_client_2.post(
            reverse("rents-complete", kwargs={"pk": self.rent_1.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # проверяем, что аренду нельзя закрыть дважды
        response_2 = self.user_client_2.post(
            reverse("rents-complete", kwargs={"pk": self.rent_1.id})
        )
        self.assertEqual(response_2.status_code, HTTPStatus.LOCKED)
