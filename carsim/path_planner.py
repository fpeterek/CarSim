from typing import List

from direction import Direction
from position_tracker import PositionTracker
from util import calc_angle
from waypoint import Waypoint


class PathPlanner:

    def __init__(self, car, pt: PositionTracker):
        self.car = car
        self.desired_heading = 0.0
        self.pt = pt

    @staticmethod
    def calc_angle(cur: float, des: float) -> float:
        cur += 360 if cur == 0 else 0
        des += 360 if des == 0 else 0
        dist = des - cur
        return (360 - abs(dist)) * [-1, 1][dist > 0] if abs(dist) > 180 else dist

    def adjust_steering(self):

        if self.pt.rotation is None:
            return

        angle = PathPlanner.calc_angle(cur=self.pt.rotation, des=self.desired_heading)
        direction = [Direction.LEFT, Direction.RIGHT][angle > 0]

        if abs(angle) <= 1.0:
            self.car.unset_steer_target()
        elif abs(angle) <= 5.0:
            self.car.steer_target(deg=2.0, direction=direction)
        elif abs(angle) <= 10.0:
            self.car.steer_target(deg=5.0, direction=direction)
        else:
            self.car.steer_target(deg=20.0, direction=direction)

    def adjust_speed(self, waypoints: List[Waypoint]):
        if not waypoints:
            self.car.enable_cruise_control(0)

        w0 = waypoints[0]
        dist = ((w0.x - self.car.x) ** 2 + (w0.y - self.car.y) ** 2) ** 0.5

        if dist < w0.tolerance:
            waypoints.pop(0)

        if waypoints:
            self.car.enable_cruise_control(50)

    def plan(self, waypoints: List[Waypoint]):
        if not waypoints:
            self.car.enable_cruise_control(0)
            self.car.unset_steer_target()
            return

        self.desired_heading = calc_angle(self.car.position, waypoints[0].position)

        self.adjust_steering()
        self.adjust_speed(waypoints)

