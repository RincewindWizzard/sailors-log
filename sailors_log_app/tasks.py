from background_task import background


@background(schedule=0)
def fetch_weather_for_trip_task(trip_id):
    from .models import Trip
    from .weather import fetch_weather_for_trip
    try:
        trip = Trip.objects.get(id=trip_id)
        fetch_weather_for_trip(trip)
    except Trip.DoesNotExist:
        ...
