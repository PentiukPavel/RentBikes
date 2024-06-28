from django.contrib import admin

from bicycles.models import Bicycle, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Отображение модели Марка Велосипеда в админке."""

    list_display = ("title", "rental_price")
    search_fields = ("title",)


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    """Отображение модели Велосипед в админке."""

    list_display = ("brand", "available")
    search_fields = ("brand__title",)
    list_filter = ("available",)
