import logging
from datetime import timedelta, datetime, timezone, tzinfo
from itertools import groupby
from typing import Iterable, Any

import requests
from django.utils.timezone import make_aware
from gpxpy.gpx import GPXTrackPoint

from sailors_log_app.analytics.trip_statistics import reduce_points_to_hourly
from sailors_log_app.models import Trip, WeatherSnapshot

logger = logging.getLogger(__name__)

OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(instant: datetime, latitude: float, longitude: float) -> dict:
    """
    Fetches the weather for this position on earth for the whole day where instant took place.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join([
            "temperature_2m", "rain", "weather_code", "visibility",
            "wind_direction_10m", "wind_speed_10m", "wind_gusts_10m",
            "cloud_cover", "cloud_cover_low", "cloud_cover_mid",
            "cloud_cover_high", "pressure_msl", "surface_pressure"
        ]),
        "wind_speed_unit": "kn",
        "start_date": instant.date().isoformat(),
        "end_date": (instant + timedelta(days=2)).date().isoformat(),
        "timezone": "UTC"
    }

    response = requests.get(OPEN_METEO_API, params=params)
    response.raise_for_status()
    data = response.json()
    logger.info(f'Got weather data = {data}')
    return data


def generate_weather_data_matrix(points: list[GPXTrackPoint]) -> list[tuple[datetime, float, float, dict]]:
    """
    Fetches hourly weather data for a list of GPXTrackPoints.
    :param points:
    :return:
    """
    hourly_weather = []
    hourly_positions = reduce_points_to_hourly(points)
    logger.info(f'hourly_positions = {hourly_positions}')
    for instant, lat, lon in hourly_positions:
        weather = fetch_weather(instant, lat, lon)
        data = weather['hourly']

        transposed = [dict(zip(data.keys(), values)) for values in zip(*data.values())]

        for weather_entry in transposed:
            if datetime.fromisoformat(weather_entry['time']).replace(tzinfo=timezone.utc) == instant:
                hourly_weather.append((instant, lat, lon, weather_entry))
                break
    return hourly_weather
