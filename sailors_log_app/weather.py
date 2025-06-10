import logging
from datetime import timedelta, datetime
from typing import Iterable

import requests
from django.utils.timezone import make_aware

from sailors_log_app.models import Trip, WeatherSnapshot

logger = logging.getLogger(__name__)

OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


def fetch_weather_for_trip(trip: Trip):
    logger.info(f"Fetching weather info for Trip {trip.id} on {trip.date}")

    gpx_point = trip.gpx_points[0]

    start_date = trip.date.isoformat()
    end_date = (trip.date + timedelta(days=1)).isoformat()

    params = {
        "latitude": gpx_point.latitude,
        "longitude": gpx_point.longitude,
        "hourly": ",".join([
            "temperature_2m", "rain", "weather_code", "visibility",
            "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m",
            "cloud_cover", "cloud_cover_low", "cloud_cover_mid",
            "cloud_cover_high", "pressure_msl", "surface_pressure"
        ]),
        "wind_speed_unit": "kn",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "UTC"
    }

    try:
        response = requests.get(OPEN_METEO_API, params=params)
        response.raise_for_status()
        data = response.json()

        logger.info(data)

        for weather_snapshot in parse_weather(data):
            WeatherSnapshot(
                trip=trip,
                **weather_snapshot
            ).save()


    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Wetterdaten: {e}")


def parse_weather(data: dict) -> Iterable[dict]:
    hours = data['hourly']['time']

    for i, ts in enumerate(hours):
        weather = dict(
            latitude=data['latitude'],
            longitude=data['longitude'],
            timestamp=make_aware(datetime.fromisoformat(ts)),
            temperature=data['hourly']['temperature_2m'][i],
            rain=data['hourly']['rain'][i],
            wind_speed=data['hourly']['wind_speed_10m'][i],
            wind_gusts=data['hourly']['wind_gusts_10m'][i],
            wind_direction=data['hourly']['wind_direction_10m'][i],
            cloud_cover=data['hourly']['cloud_cover'][i],
            pressure_msl=data['hourly']['pressure_msl'][i],
            surface_pressure=data['hourly']['surface_pressure'][i],
            weather_code=data['hourly']['weather_code'][i],
        )
        yield weather
