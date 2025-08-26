from django.contrib import admin
from .models import Boat, Trip, WeatherSnapshot


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ("name", "year_built", "length_m", "beam_m", "draft_m", "displacement_kg")
    search_fields = ("name",)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "boat", "date", "distance_nm", "duration")
    list_filter = ("boat", "date")
    search_fields = ("title", "description")


@admin.register(WeatherSnapshot)
class WeatherSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        'trip',
        'timestamp',
        'temperature',
        'wind_speed',
        'wind_gusts',
        'wind_direction',
        'cloud_cover',
        'rain',
        'pressure_msl',
        'surface_pressure',
        'weather_code',
    )
    list_filter = ('trip', 'timestamp')
    search_fields = ('trip__title', 'trip__boat__name')
    ordering = ('-timestamp',)