from django.db import models

from core.enums import Limits


class Bicycle(models.Model):
    """Велосипед."""

    model = models.CharField(
        "Модель",
        max_length=Limits.MAX_LENGTH_BICIKLE_MODEL.value,
        db_index=True,
    )
    available = models.BooleanField(
        "Доступен",
        default=True,
    )

    class Meta:
        verbose_name = "Велосипед"
        verbose_name_plural = "Велосипеды"
        ordering = ["model"]

    def __str__(self) -> str:
        return self.model

    def make_unavailable(self) -> None:
        if self.available:
            self.available = False
            self.save()

    def make_available(self) -> None:
        if not self.available:
            self.available = True
            self.save()
