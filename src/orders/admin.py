from django.contrib import admin

from orders.models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    """Отображение модель Аренда в ажминке."""

    list_display = (
        "bicycle",
        "renter",
        "start_time",
        "end_time",
    )
    search_fields = ("renter__username", "start_time")
