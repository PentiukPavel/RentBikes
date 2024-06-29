from django.db import transaction

from bicycles.models import Bicycle
from orders.models import Rent


def rent_bike(bicycle: Bicycle, user) -> None:
    """Арендовать велосипед."""

    with transaction.atomic():
        Rent.objects.create(
            bicycle=bicycle,
            renter=user,
        )
        bicycle.make_unavailable()
