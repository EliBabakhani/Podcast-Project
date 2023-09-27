from celery import shared_task
from .models import Episode


@shared_task
def update_episodes():
    pass