import gpxpy
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .constants import WindCourse
from .forms import TripForm
from .models import Trip, Boat
from sailors_log_app.analytics.trip_statistics import distance_travelled, duration_travelled, course_histogram, speed_graph, calculate_bearing, \
    normalize_histogram


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
    trip: Trip = get_object_or_404(Trip, pk=pk)

    weather = trip.weather

    wind_course_histogram = {}
    foo = []
    for p0, p1 in trip.gpx_lines:
        bearing = calculate_bearing(p0, p1)
        wind_direction = weather.wind_direction_at(p0.time)
        wind_course = WindCourse.for_angle(abs(wind_direction - bearing))
        foo.append(
            dict(
                time=p0.time,
                bearing=bearing,
                wind_direction=wind_direction,
                wind_angle=abs(wind_direction - bearing),
                course=WindCourse.for_angle(abs(wind_direction - bearing)).german_name
            ))

        if not wind_course in wind_course_histogram:
            wind_course_histogram[wind_course] = 0
        wind_course_histogram[wind_course] += (p0.time - p1.time).seconds

    wind_course_histogram = normalize_histogram(wind_course_histogram)
    stats = dict(
        weather=weather.to_dict(),
        wind_course_histogram={k.name: v for k, v in wind_course_histogram.items()},
        foo=foo
    )
    return JsonResponse(stats)
