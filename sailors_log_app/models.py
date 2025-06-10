from math import sqrt

import gpxpy
from django.db import models


class Boat(models.Model):
    name = models.CharField(max_length=100)
    info_url = models.URLField("Weitere Informationen", blank=True)

    year_built = models.PositiveIntegerField("Baujahr", null=True, blank=True)
    length_m = models.FloatField("Länge (m)", null=True, blank=True)
    beam_m = models.FloatField("Breite (m)", null=True, blank=True)
    draft_m = models.FloatField("Tiefgang (m)", null=True, blank=True)
    displacement_kg = models.PositiveIntegerField("Verdrängung (kg)", null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def hull_speed_kn(self):
        if self.length_m:
            return round(2.43 * sqrt(self.length_m), 2)
        return None


class Trip(models.Model):
    title = models.CharField(max_length=200, blank=True)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    date = models.DateField()
    gpx_file = models.FileField(upload_to='tracks/')
    description = models.TextField(blank=True)

    # automatisch befüllt beim Upload
    distance_nm = models.FloatField("Distanz (Seemeilen)", null=True, blank=True)
    duration = models.DurationField("Dauer", null=True, blank=True)

    def __str__(self):
        return f"{self.date} – {self.title}"

    def save(self, *args, **kwargs):
        if self.gpx_file:
            self._parse_gpx()

        if not self.title or len(self.title) == 0:
            self.title = f'{self.date}_{self.boat.name}'
        super().save(*args, **kwargs)

    def _parse_gpx(self):
        self.gpx_file.seek(0)  # Datei-Zeiger auf Anfang setzen

        gpx = gpxpy.parse(self.gpx_file.read().decode("utf-8"))

        total_length_m = 0
        start_time = None
        end_time = None

        for track in gpx.tracks:
            for segment in track.segments:
                total_length_m += segment.length_3d()
                for point in segment.points:
                    if point.time:
                        if not self.date:
                            self.date = point.time.date()
                        if not start_time or point.time < start_time:
                            start_time = point.time
                        if not end_time or point.time > end_time:
                            end_time = point.time

        self.distance_nm = round(total_length_m / 1852, 2)  # Meter → Seemeilen
        if start_time and end_time:
            self.duration = end_time - start_time
