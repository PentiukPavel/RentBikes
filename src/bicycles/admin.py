from django.contrib import admin

from bicycles.models import Bicycle


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    """Отображение модели Велосипед в админке."""

    list_display = ("model", "available")
    search_fields = ("model",)
    list_filter = ("available",)
