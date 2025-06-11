from enum import Enum
from typing import Optional


class WindCourse(Enum):
    """
    WindCourse represents the sailing course relative to wind direction.
    Each entry includes the angle range (in degrees) and whether the wind
    comes from port (Backbord) or starboard (Steuerbord).
    """

    NO_GO_ZONE = (330, 30)

    CLOSE_HAULED_PORT = (315, 330)
    CLOSE_HAULED_STARBOARD = (30, 45)

    HAULED_PORT = (280, 315)
    HAULED_STARBOARD = (45, 80)

    BEAM_REACH_PORT = (260, 280)
    BEAM_REACH_STARBOARD = (80, 100)

    BROAD_REACH_PORT = (200, 260)
    BROAD_REACH_STARBOARD = (100, 160)

    RUNNING = (160, 200)

    def __init__(self, min_angle: float, max_angle: float):
        super().__init__()
        self.min_angle = min_angle  # Degrees, 0–360
        self.max_angle = max_angle

    @classmethod
    def for_angle(cls, angle: float) -> Optional["WindCourse"]:
        """
        Classifies a wind angle (0–360°) relative to the bow into a specific WindCourse.

        Args:
            angle (float): The wind angle in degrees relative to the bow (0° = head to wind).

        Returns:
            WindCourse or None: The matching course including wind side, or None if undefined.
        """

        def course_between(begin, angle, end):
            angle = angle % 360
            if begin < end:
                return begin <= angle <= end
            else:
                return begin <= angle <= end + 360 or begin - 360 <= angle <= end

        for course in cls:
            if course_between(course.min_angle, angle, course.max_angle):
                return course

        raise ValueError(f'Could not find WindCourse for {angle}')
