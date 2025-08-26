import logging

from background_task import background

logger = logging.getLogger(__name__)


@background(schedule=0)
def fetch_weather_for_trip_task(trip_id):
    from .models import Trip
    from sailors_log_app.models import WeatherSnapshot
    from sailors_log_app.services.weather import generate_weather_data_matrix
    try:
        trip = Trip.objects.get(id=trip_id)
        logger.info(f'Fetching weather data for trip {trip.pk}')
        weather_data_matrix = generate_weather_data_matrix(trip.gpx_points)

        for instant, lat, lon, weather in weather_data_matrix:
            WeatherSnapshot(
                trip=trip,
                timestamp=instant,
                latitude=lat,
                longitude=lon,
                temperature=weather['temperature_2m'],
                rain=weather['rain'],
                wind_speed=weather['wind_speed_10m'],
                wind_gusts=weather['wind_gusts_10m'],
                wind_direction=weather['wind_direction_10m'],
                cloud_cover=weather['cloud_cover'],
                pressure_msl=weather['pressure_msl'],
                surface_pressure=weather['surface_pressure'],
                weather_code=weather['weather_code'],
            ).save()
    except Trip.DoesNotExist:
        ...
