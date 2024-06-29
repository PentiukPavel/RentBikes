from celery import shared_task

from orders.models import Rent


@shared_task
def calculate_rent_cost(rent_id: int):
    rent = Rent.objects.filter(pk=rent_id).first()
    rent.cost_calculation()
