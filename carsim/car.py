import math

from pygame.rect import Rect
from pygame.sprite import Sprite
import pygame

from vector import Vector
from wheels import Wheel


class Car(Sprite):

    default_weight = 1800  # kg
    default_top_speed = 230  # km/h
    sprite_dim = (32, 15)
    default_brake_force = 15
    default_acceleration = 30
    default_deceleration = 0.05

    def __init__(self, x, y):
        Sprite.__init__(self)

        self.orig_image = pygame.transform.scale(pygame.image.load('resources/car.png'), Car.sprite_dim)
        self.image = self.orig_image
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect = Rect(self.x, self.y, self.image.get_rect().width, self.image.get_rect().height)

        self._velocity = 0.0
        self._rotation = 0.0

        self.target_velocity = -1

        self.is_acc = False
        self.v_input_received = False

        self.front_wheel = Wheel()

        self.weight = Car.default_weight
        self.acceleration = Car.default_acceleration
        self.deceleration = Car.default_deceleration
        self.brake_force = Car.default_brake_force
        self.top_speed = Car.default_top_speed

    @property
    def rotation(self):
        return math.radians(self._rotation)

    @property
    def forces(self):
        rotation = self.rotation
        fx = self._velocity * math.cos(rotation)
        fy = self._velocity * math.sin(rotation)

        return Vector(fx, fy)

    @property
    def velocity(self):
        return self._velocity

    @property
    def cruise_control_on(self):
        return not (self.target_velocity < 0)

    @property
    def should_acc(self):
        return self.cruise_control_on and self._velocity < self.target_velocity and not self.v_input_received

    @property
    def should_brake(self):
        return self.cruise_control_on and self._velocity > self.target_velocity + 3 and not self.v_input_received

    def enable_cruise_control(self, target):
        self.target_velocity = target

    def disable_cruise_control(self):
        self.target_velocity = -1

    def full_speed(self):
        self.v_input_received = True
        self._velocity = self.top_speed

    def accelerate(self):
        self.v_input_received = True
        self.is_acc = True

    def inverse_acc(self):
        return -2.94118 * (1 - math.e**(0.0112642 * self.velocity))

    def acc_fun(self, dt):
        t = self.inverse_acc() + dt
        return 88.777 * math.log(0.34 * (t+2.94118))

    def _acc(self, dt):
        new = self.acc_fun(dt)

        if self.cruise_control_on and new > self.target_velocity and not self.v_input_received:
            self._velocity = self.target_velocity
        else:
            self._velocity = min(float(self.top_speed), new)

    def _dec(self, dt):
        delta = dt * max(self.deceleration * ((self._velocity / 10) ** 2), 1)

        if not self.v_input_received and self.cruise_control_on and self._velocity-delta < self.cruise_control_on:
            self._velocity = self.target_velocity
        else:
            self._velocity -= delta

        self._velocity = max(self._velocity, 0)

    def _brake(self, dt):
        delta = dt * self.brake_force

        if self.v_input_received or (self.cruise_control_on and self._velocity - delta > self.target_velocity):
            self._velocity -= dt * self.brake_force
        else:
            self._velocity = self.target_velocity

        self._velocity = max(self._velocity, 0)

    def calc_velocity(self, dt):
        if self.is_acc or self.should_acc:
            self._acc(dt)
        else:
            self._dec(dt)
            if self.cruise_control_on and self.should_brake:
                self._brake(dt)

    def apply_brake(self, dt):
        self.v_input_received = True
        self._brake(dt)

    def bound_rotation(self):
        if self._rotation > 360:
            self._rotation -= 360
        elif self._rotation < 0:
            self._rotation += 360

    def rotate(self, dt, v):
        self._rotation += v * dt * (self._velocity / self.top_speed * 5)
        self.bound_rotation()
        self.image = pygame.transform.rotate(self.orig_image, 360.0 - self._rotation)
        self.rect = self.image.get_rect()
        self.update_rect()

    def steer_left(self, dt):
        self.front_wheel.steer_left(dt)

    def steer_right(self, dt):
        self.front_wheel.steer_right(dt)

    def steer_target(self, deg, direction):
        self.front_wheel.set_target(deg, direction)

    def unset_steer_target(self):
        self.front_wheel.unset_target()

    def update_rect(self):
        w = self.rect.width
        h = self.rect.height
        self.rect = Rect(self.x, self.y, w, h)

    def move(self, dt):
        f = self.forces
        dx = f.x * dt
        dy = f.y * dt
        self.x += dx
        self.y += dy
        self.update_rect()

    def update(self, dt):
        self.front_wheel.update(dt)
        self.rotate(dt, self.front_wheel.rotation)
        self.calc_velocity(dt)
        self.is_acc = False
        self.v_input_received = False
        self.move(dt)
