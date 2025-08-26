import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trip
from .tasks import fetch_weather_for_trip_task

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Trip)
def fetch_weather_after_save(sender, instance, created, **kwargs):
    logger.info('fetch_weather_after_save')
    if created:
        fetch_weather_for_trip_task(trip_id=instance.id)
