import datetime
from datetime import timezone
from math import sqrt

import gpxpy
from django.db import models
from gpxpy.gpx import GPXTrackPoint


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

    def to_dict(self):
        return {
            "title": self.title,
            "boat": self.boat.name,
            "date": self.date.isoformat(),
            "description": self.description,
            "distance_nm": self.distance_nm,
            "duration": str(self.duration) if self.duration else None,
            "gpx": [dict(
                time=p.time.isoformat(),
                latitude=p.latitude,
                longitude=p.longitude
            ) for p in self.gpx_points]
        }

    def save(self, *args, **kwargs):
        if self.gpx_file:
            self._parse_gpx()

        if not self.title or len(self.title) == 0:
            self.title = f'{self.date}_{self.boat.name}'
        super().save(*args, **kwargs)

    @property
    def weather(self):
        if not hasattr(self, '_weather') or self._weather is None:
            self._weather = WeatherTrip(self)
        return self._weather

    @property
    def gpx_points(self) -> list[GPXTrackPoint]:
        if not hasattr(self, '_gpx_points'):
            self._gpx_points = []
            with self.gpx_file.open("rb") as f:
                gpx = gpxpy.parse(f.read().decode("utf-8"))
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        self._gpx_points.append(point)
        return self._gpx_points

    @property
    def gpx_lines(self):
        return zip(self.gpx_points[:-1], self.gpx_points[1:])

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


class WeatherSnapshot(models.Model):
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name="weather_snapshots")
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    temperature = models.FloatField(null=True, blank=True)
    rain = models.FloatField(null=True, blank=True)
    weather_code = models.IntegerField(null=True, blank=True)
    visibility = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_gusts = models.FloatField(null=True, blank=True)
    cloud_cover = models.FloatField(null=True, blank=True)
    cloud_cover_low = models.FloatField(null=True, blank=True)
    cloud_cover_mid = models.FloatField(null=True, blank=True)
    cloud_cover_high = models.FloatField(null=True, blank=True)
    pressure_msl = models.FloatField(null=True, blank=True)
    surface_pressure = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.trip} – {self.timestamp}"

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature": self.temperature,
            "rain": self.rain,
            "weather_code": self.weather_code,
            "visibility": self.visibility,
            "wind_direction": self.wind_direction,
            "wind_speed": self.wind_speed,
            "wind_gusts": self.wind_gusts,
            "cloud_cover": self.cloud_cover,
            "cloud_cover_low": self.cloud_cover_low,
            "cloud_cover_mid": self.cloud_cover_mid,
            "cloud_cover_high": self.cloud_cover_high,
            "pressure_msl": self.pressure_msl,
            "surface_pressure": self.surface_pressure,
        }


class WeatherTrip(object):
    """
    This is a container object for multiple WeatherSnapshots following a route given by a Trip.
    It can be used to interpolate data
    """

    def __init__(self, trip: Trip):
        super().__init__()
        self._hourly_weather = {
            ws.timestamp.astimezone(timezone.utc): ws
            for ws in trip.weather_snapshots.all()
        }

    @staticmethod
    def _shortest_angle_delta(a: float, b: float):
        """
        Gibt die kleinstmögliche (signierte) Winkeländerung von a nach b zurück,
        im Bereich (-180, +180].
        """
        delta = (b - a + 180) % 360 - 180
        return delta

    def wind_direction_at(self, instant: datetime.datetime):
        previous_hour = datetime.datetime(
            year=instant.year,
            month=instant.month,
            day=instant.day,
            hour=instant.hour,
            tzinfo=instant.tzinfo
        ).astimezone(datetime.timezone.utc)
        next_hour = previous_hour + datetime.timedelta(hours=1)

        if previous_hour in self._hourly_weather and next_hour in self._hourly_weather:
            wd_prev = self._hourly_weather[previous_hour].wind_direction
            wd_next = self._hourly_weather[next_hour].wind_direction

            total = (next_hour - previous_hour).total_seconds()
            elapsed = (instant - previous_hour).total_seconds()
            factor = elapsed / total

            delta = WeatherTrip._shortest_angle_delta(wd_prev, wd_next)

            interpolated = (wd_prev + delta * factor) % 360
            return interpolated
        else:
            return None

    def to_dict(self):
        return {
            ts.isoformat(): ws.to_dict()
            for ts, ws in self._hourly_weather.items()
        }

    def as_list(self):
        return [v.to_dict() for k, v in sorted(self._hourly_weather.items())]
