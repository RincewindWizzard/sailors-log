import itertools
import math
from typing import Iterable

import gpxpy
import gpxpy.gpx
from gpxpy.gpx import GPX, GPXTrackPoint
from geopy.distance import geodesic
from datetime import timedelta, datetime, timezone


def distance_travelled(gpx: GPX) -> float:
    total_distance = 0.0
    for track in gpx.tracks:
        for segment in track.segments:
            points = segment.points
            for i in range(1, len(points)):
                start = (points[i - 1].latitude, points[i - 1].longitude)
                end = (points[i].latitude, points[i].longitude)
                total_distance += geodesic(start, end).nm
    return total_distance


def duration_travelled(gpx: GPX) -> timedelta:
    start_time: datetime | None = None
    end_time: datetime | None = None
    for track in gpx.tracks:
        for segment in track.segments:
            points = segment.points
            if points:
                if not start_time or points[0].time < start_time:
                    start_time = points[0].time
                if not end_time or points[-1].time > end_time:
                    end_time = points[-1].time

    return end_time - start_time


def extract_points(gpx: GPX) -> Iterable[GPXTrackPoint]:
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                yield point


def extract_line_segments(gpx: GPX) -> Iterable[tuple[GPXTrackPoint, GPXTrackPoint]]:
    points = list(extract_points(gpx))
    return zip(points[:-1], points[1:])


def course_histogram(gpx: GPX, buckets=16) -> list[float]:
    bearings = [
        calculate_bearing(*line)
        for line in extract_line_segments(gpx)
    ]

    # ['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    bearing_histogram = [0] * buckets

    for bearing in bearings:
        bearing_bucket = int(((bearing) % 360) / 360 * buckets)
        bearing_histogram[bearing_bucket] += 1

    total_count = sum(bearing_histogram)

    bearing_histogram_normalized = [float(x) / total_count for x in bearing_histogram]

    return bearing_histogram_normalized


def normalize_histogram(hist: dict) -> dict:
    total = sum(hist.values())
    if total == 0:
        return hist
    return {k: v / total for k, v in hist.items()}


def speed_graph(gpx: GPX):
    result = []
    for start, end in extract_line_segments(gpx):
        time_delta = end.time - start.time
        distance = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
        hours = time_delta.seconds / 60 / 60
        result.append((
            (start.time + (time_delta / 2)).isoformat(),
            distance / hours)
        )
    return result


def calculate_bearing(point_a: GPXTrackPoint, point_b: GPXTrackPoint) -> float:
    lat1 = math.radians(point_a.latitude)
    lat2 = math.radians(point_b.latitude)
    diff_long = math.radians(point_b.longitude - point_a.longitude)

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_long))
    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing


def reduce_points_to_hourly(points: list[GPXTrackPoint]) -> list[tuple[datetime, float, float]]:
    """
    Reduces a list of GPXTrackPoints to only one (average) position every hour using groupby.
    """
    # Stelle sicher, dass die Punkte nach Zeit sortiert sind
    points = sorted(points, key=lambda p: p.time)

    def hour_key(point):
        # Runde die Zeit auf die volle Stunde in UTC
        return datetime(
            year=point.time.year,
            month=point.time.month,
            day=point.time.day,
            hour=point.time.hour,
            tzinfo=point.time.tzinfo
        ).astimezone(timezone.utc)

    hourly_positions = []

    for hour, group in itertools.groupby(points, key=hour_key):
        group_list = list(group)
        lat_avg = sum(p.latitude for p in group_list) / len(group_list)
        lon_avg = sum(p.longitude for p in group_list) / len(group_list)
        hourly_positions.append((hour, lat_avg, lon_avg))

    last_position = hourly_positions[-1]
    hourly_positions.append((last_position[0] + timedelta(hours=1), last_position[1], last_position[2]))
    return hourly_positions
