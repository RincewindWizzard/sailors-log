from enum import Enum


class WindCourse(Enum):
    NO_GO_ZONE = (0, 30, "Toter Winkel")
    CLOSE_HAULED = (30, 45, "Hart am Wind")
    HAULED = (45, 80, "am Wind")
    BEAM_REACH = (80, 100, "Halber Wind")
    BROAD_REACH = (100, 160, "Raumschots")
    RUNNING = (160, 180, "Vorm Wind")

    def __init__(self, min_angle, max_angle, german_name):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.german_name = german_name

    @classmethod
    def for_angle(cls, angle: float) -> "WindCourse | None":
        """
        Returns the WindCourse enum member that matches the given angle in degrees,
        using the smallest angle to the wind (0°..180°).

        Parameters:
            angle (float): The angle in degrees to classify.

        Returns:
            WindCourse or None: The matching WindCourse member if found, else None.
        """
        angle = angle % 360
        if angle > 180:
            angle = 360 - angle

        for course in cls:
            if course.min_angle <= angle <= course.max_angle:
                return course
        return None
