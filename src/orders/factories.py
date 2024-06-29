from datetime import timedelta

from django.utils import timezone
from factory import (
    fuzzy,
    SubFactory,
)
from factory.django import DjangoModelFactory

from bicycles.factories import BicycleFactory
from orders.models import Rent
from users.factories import UserFactory


class RentFactory(DjangoModelFactory):
    """Фабрика для создания экземпляров модели Аренда."""

    class Meta:
        model = Rent

    renter = SubFactory(UserFactory)
    bicycle = SubFactory(BicycleFactory)
    start_time = fuzzy.FuzzyDateTime(
        timezone.now() - timedelta(days=1),
        timezone.now(),
    )
