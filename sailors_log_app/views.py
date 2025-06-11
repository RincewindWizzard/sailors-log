import datetime

import gpxpy
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import TripForm
from .models import Trip, Boat, WeatherSnapshot
from .trip_statistics import distance_travelled, duration_travelled, course_histogram, speed_graph
from .weather import reduce_points_to_hourly, fetch_weather, generate_weather_data_matrix


def trip_list(request):
    trips = Trip.objects.all().order_by('-date')
    return render(request, 'trip_list.html', {'trips': trips})


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    with trip.gpx_file.open('r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    trip.distance_nm = distance_travelled(gpx)
    trip.duration = duration_travelled(gpx)

    context = dict(
        trip=trip,
        course_histogram=course_histogram(gpx),
        speed_graph=[dict(x=t[0], y=t[1]) for t in speed_graph(gpx)],
        hull_speed=trip.boat.hull_speed_kn
    )

    return render(request, 'trip_detail.html', context)


def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trip_list')  # or wherever you want to go
    else:
        form = TripForm()
    return render(request, 'trip_create.html', {'form': form})


@require_POST
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    trip.delete()
    return redirect('trip_list')


def boat_statistics(request):
    stats = (
        Boat.objects.annotate(
            total_nm=Sum('trip__distance_nm'),
            total_duration=Sum('trip__duration')
        ).order_by('-total_nm')
    )
    return render(request, 'boat_statistics.html', {'stats': stats})


def trip_weather_statistics(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    hourly_weather = generate_weather_data_matrix(trip.gpx_points)

    for instant, lat, lon, weather in hourly_weather:
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

    stats = dict(
        weather=hourly_weather
    )
    return JsonResponse(stats)
