from typing import Tuple
import math

from util import calc_angle


class PositionTracker:

    hist_len = 10

    def __init__(self):
        self.position_history = []
        self.rotation = None

    @property
    def current_position(self):
        return None if not self.position_history else self.position_history[0]

    def trim_hist(self):
        if len(self.position_history) > PositionTracker.hist_len:
            self.position_history = self.position_history[0:-1]

    def calc_rotation(self):
        if len(self.position_history) < 2:
            return

        self.rotation = calc_angle(begin=self.position_history[-1], end=self.position_history[-2])

    def add(self, pos: Tuple[float, float]):
        self.position_history.insert(0, pos)
        self.trim_hist()
        self.calc_rotation()













