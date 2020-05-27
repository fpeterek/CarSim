import math


class Sensor:

    default_range = 350.0
    default_color = (28, 255, 43)
    default_velocity = 120.0  # Default angle velocity in degrees per second

    def __init__(self, center: tuple):
        self.range = Sensor.default_range
        self.color = Sensor.default_color
        self.angle_velocity = Sensor.default_velocity

        self.center = center
        self.rotation = 0.0

    def get_end(self):
        x = math.cos(math.radians(self.rotation)) * self.range
        y = math.sin(math.radians(self.rotation)) * self.range
        return self.center[0] + x, self.center[1] + y

    def update(self, dt):
        self.rotation += self.angle_velocity * dt
        if self.rotation > 360.0:
            self.rotation -= 360.0
