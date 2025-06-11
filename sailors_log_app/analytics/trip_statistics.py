import itertools
import logging
import math

from typing import Iterable, TypeVar, Dict, Hashable, Protocol, runtime_checkable, Any

from django.utils.http import escape_leading_slashes
from gpxpy.gpx import GPX, GPXTrackPoint
from geopy.distance import geodesic
from datetime import timedelta, datetime, timezone

from sailors_log_app.constants import WindCourse
from sailors_log_app.models import Trip

logger = logging.getLogger(__name__)


@runtime_checkable
class SupportsAdd(Protocol):
    def __add__(self, other: 'SupportsAdd') -> 'SupportsAdd':
        ...


K = TypeVar('K', bound=Hashable)
V = TypeVar('V', bound=SupportsAdd)


def distance_travelled(gpx: GPX) -> float:
    return sum([
        geodesic(
            (start.latitude, start.longitude),
            (end.latitude, end.longitude)
        ).nm
        for start, end in extract_line_segments(list(extract_points(gpx)))
    ])


def duration_travelled(gpx: GPX) -> timedelta:
    points = list(extract_points(gpx))
    start_time: datetime | None = None
    end_time: datetime | None = None

    for point in extract_points(gpx):
        if not start_time or point.time < start_time:
            start_time = point.time
        if not end_time or point.time > end_time:
            end_time = point.time

    return end_time - start_time


def extract_points(gpx: GPX) -> Iterable[GPXTrackPoint]:
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                yield point


def extract_line_segments(points: list[GPXTrackPoint]) -> Iterable[tuple[GPXTrackPoint, GPXTrackPoint]]:
    return zip(points[:-1], points[1:])


def bearing_histogram(points: list[GPXTrackPoint], buckets=16) -> dict[int, SupportsAdd | Any]:
    bucket_names = ['N', 'NNO', 'NO', 'ONO', 'O', 'OSO', 'SO', 'SSO', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

    def bucket(bearing: float) -> int:
        return bucket_names[round((bearing % 360) / 360 * buckets) % buckets]

    def data(p0, p1):
        return bucket(calculate_bearing(p0, p1)), (p1.time - p0.time).seconds

    return create_normalize_histogram(
        data(*line)
        for line in extract_line_segments(points)
    )


def speed(start: GPXTrackPoint, end: GPXTrackPoint) -> float:
    time_delta = end.time - start.time
    distance = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).nm
    hours = time_delta.seconds / 60 / 60
    return distance / hours


def speed_graph(points: list[GPXTrackPoint]):
    return [
        (
            start.time + (end.time - start.time) / 2,
            speed(start, end)
        )
        for start, end in extract_line_segments(points)
    ]


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


def calculate_wind_course_histogram(trip: Trip):
    data_points = [(course, 0.0) for course in WindCourse]
    for p0, p1 in trip.gpx_lines:
        bearing = calculate_bearing(p0, p1)
        wind_direction = trip.weather.wind_direction_at(p0.time)
        if wind_direction is None:
            raise ValueError(f'Missing wind data for {trip.title}')
        wind_course = WindCourse.for_angle(abs(wind_direction - bearing))
        data_points.append((wind_course, (p0.time - p1.time).seconds))

    try:
        return normalize_histogram(create_histogram(data_points))
    except ValueError as e:
        logger.warning(e)
        return None


def create_histogram(ts: Iterable[tuple[K, V]] | list[tuple[K, V]]) -> Dict[K, V]:
    result: Dict[K, V] = {}
    for k, v in ts:
        if k not in result:
            result[k] = v - v
        result[k] += v
    return result


def normalize_histogram(hist: Dict[K, V]) -> Dict[K, V]:
    total = sum(hist.values())
    if total == 0:
        return hist
    return {k: v / total for k, v in hist.items()}


def create_normalize_histogram(ts: Iterable[tuple[K, V]]) -> Dict[K, V]:
    return normalize_histogram(create_histogram(ts))
