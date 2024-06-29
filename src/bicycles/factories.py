from factory import (
    fuzzy,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory

from bicycles.models import Bicycle, Brand
from core.enums import Limits


class BrandFactory(DjangoModelFactory):
    """Фабрика для создания экземпляров модели Марка Велосипеда."""

    class Meta:
        model = Brand

    title = Sequence(lambda n: "model_{}".format(n))
    description = fuzzy.FuzzyText(
        length=Limits.MAX_LENGTH_BRAND_DESCRIPTION.value
    )
    rental_price = fuzzy.FuzzyDecimal(low=1, high=100)


class BicycleFactory(DjangoModelFactory):
    """Фабрика для создания экземпляров модели Велосипед."""

    class Meta:
        model = Bicycle

    brand = SubFactory(BrandFactory)
