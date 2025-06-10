from django.shortcuts import render, get_object_or_404
from .models import Trip


def trip_overview(request):
    trips = Trip.objects.all().order_by('-date')
    return render(request, 'overview.html', {'trips': trips})


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'trip_detail.html', {'trip': trip})
