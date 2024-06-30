from datetime import timedelta, datetime

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models, transaction

from bicycles.models import Bicycle
from orders.managers import RentManager


User = get_user_model()


class Rent(models.Model):
    """Аренда велосипеда."""

    bicycle = models.ForeignKey(
        Bicycle,
        on_delete=models.PROTECT,
        verbose_name="велоспед",
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Арендатор",
        db_index=True,
    )
    start_time = models.DateTimeField(
        "Начало аренды",
        auto_now_add=True,
        db_index=True,
    )
    end_time = models.DateTimeField(
        "Конец аренды",
        null=True,
    )
    cost = models.DecimalField(
        "Стоимость аренды",
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal(0),
                "Стоимость не может быть меньше 0.",
            ),
        ],
        null=True,
    )

    objects = models.Manager()
    cstm_mngr = RentManager()

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        default_related_name = "rents"

    def __str__(self) -> str:
        return f"Аренда от {self.start_time}"

    def complete_rent(self) -> None:
        """Завершить аренду."""

        with transaction.atomic():
            self.end_time = datetime.now()
            self.bicycle.make_available()

    def cost_calculation(self) -> None:
        """Расчет стоимости аренды."""

        if self.end_time is not None:
            delta: timedelta = self.end_time - self.start_time
            self.cost = (
                Decimal(delta.seconds / 3600 + 1)
                * self.bicycle.brand.rental_price
            )
            self.save()
