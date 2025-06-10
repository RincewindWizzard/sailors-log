import gpxpy
from django.shortcuts import render, get_object_or_404
from .models import Trip
from .trip_statistics import distance_travelled, duration_travelled, course_histogram, speed_graph


def trip_overview(request):
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
        speed_graph=[dict(x=t[0], y=t[1]) for t in speed_graph(gpx)]
    )

    return render(request, 'trip_detail.html', context)
