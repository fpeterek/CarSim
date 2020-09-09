from typing import Tuple


class Waypoint:

    color = (255, 0, 0)
    sec_color = (255, 138, 138)

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 10
        self.tolerance = 30

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y
