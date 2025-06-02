from django.contrib import admin
from .models import Boat, Trip


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ("name", "year_built", "length_m", "beam_m", "draft_m", "displacement_kg")
    search_fields = ("name",)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "boat", "date", "distance_nm", "duration")
    list_filter = ("boat", "date")
    search_fields = ("title", "description")
