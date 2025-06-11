import math

from sailors_log_app.analytics.trip_statistics import create_histogram, normalize_histogram


def test_create_histogram():
    result = normalize_histogram(create_histogram([(i % 10, abs(math.sin(i / 10  * math.pi))) for i in range(100)]))
    assert math.isclose(sum(result.values()), 1.0, rel_tol=1e-9), f"Sum is {sum(result.values())}, expected ~1.0"

