from django.db import models

from bicycles.managers import BicycleManager
from core.enums import Limits


class Brand(models.Model):
    """Марка велосипеда."""

    title = models.CharField(
        "Название",
        max_length=Limits.MAX_LENGTH_BRAND_TITLE.value,
        db_index=True,
    )
    description = models.TextField(
        "Описание",
        max_length=Limits.MAX_LENGTH_BRAND_DESCRIPTION.value,
        null=True,
    )
    rental_price = models.DecimalField(
        "Стоимость аренды в час",
        max_digits=6,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "Марка велосипеда"
        verbose_name_plural = "Марки велосипедов"
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Bicycle(models.Model):
    """Велосипед."""

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        verbose_name="Марка Велосипеда",
        db_index=True,
    )
    available = models.BooleanField(
        "Доступен",
        default=True,
    )

    objects = models.Manager()
    cstm_mngr = BicycleManager()

    class Meta:
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеды"
        ordering = ["brand"]

    def __str__(self) -> str:
        return f"Велосипед марки {self.brand}"

    def make_unavailable(self) -> None:
        if self.available:
            self.available = False
            self.save()

    def make_available(self) -> None:
        if not self.available:
            self.available = True
            self.save()
