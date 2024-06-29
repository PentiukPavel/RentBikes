from django.db import models


class RentManager(models.Manager):
    """Пользовательсткий менеджер для модели Аренда."""

    def get_queryset(self) -> models.QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                "bicycle",
                "bicycle__brand",
            )
        )
