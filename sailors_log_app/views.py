import gpxpy
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import TripForm
from .models import Trip, Boat
from sailors_log_app.analytics.trip_statistics import distance_travelled, duration_travelled, bearing_histogram, \
    speed_graph, calculate_wind_course_histogram


def trip_list(request):
    trips = Trip.objects.all().order_by('-date')
    return render(request, 'trip_list.html', {'trips': trips})


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    with trip.gpx_file.open('r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    trip.distance_nm = distance_travelled(gpx)
    trip.duration = duration_travelled(gpx)

    wind_course_histogram = calculate_wind_course_histogram(trip)
    context = dict(
        trip=trip,
        hull_speed=trip.boat.hull_speed_kn,
        data=dict(
            gpx=trip.gpx_file.url,
            speed_graph=[dict(time=t[0].isoformat(), speed=t[1]) for t in speed_graph(trip.gpx_points)],
            weather=trip.weather.as_list(),
            wind_course_histogram={k.name: v for k, v in
                                   wind_course_histogram.items()} if wind_course_histogram else None,
            bearing_histogram=bearing_histogram(trip.gpx_points),
        )
    )

    return render(request, 'trip_detail.html', context)


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trip_list')  # or wherever you want to go
    else:
        form = TripForm()
    return render(request, 'trip_create.html', {'form': form})


@login_required
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


def trip_statistics_json(request, pk):
    trip: Trip = get_object_or_404(Trip, pk=pk)

    stats = dict(
        trip=trip.to_dict(),
        speed_graph=[dict(time=t[0], speed=t[1]) for t in speed_graph(trip.gpx_points)],
        hull_speed=trip.boat.hull_speed_kn,
        weather=trip.weather.as_list(),
        wind_course_histogram={k.name: v for k, v in calculate_wind_course_histogram(trip).items()},
        bearing_histogram=bearing_histogram(trip.gpx_points),
    )
    return JsonResponse(stats)
