from django.db import models


class BicycleManager(models.Manager):
    """Менеджер для модели Велосипед."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related("brand")
