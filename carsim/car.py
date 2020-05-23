import math

from pygame.rect import Rect
from pygame.sprite import Sprite
import pygame

from vector import Vector


class Car(Sprite):

    default_weight = 1800  # kg
    default_top_speed = 230  # km/h
    sprite_dim = (32, 15)
    default_brake_force = 50
    default_acceleration = 30
    default_deceleration = 10
    default_rotation = 15

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
        self.weight = Car.default_weight
        self.acceleration = Car.default_acceleration
        self.deceleration = Car.default_deceleration
        self.rotation_speed = Car.default_rotation
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

    def accelerate(self, dt):
        self._velocity += dt * self.acceleration
        self._velocity = min(self._velocity, self.top_speed)

    def decelerate(self, dt):
        self._velocity -= dt * self.deceleration
        self._velocity = max(self._velocity, 0)

    def apply_brake(self, dt):
        self._velocity -= dt * self.brake_force
        self._velocity = max(self._velocity, 0)

    def bound_rotation(self):
        if self._rotation > 360:
            self._rotation -= 360
        elif self._rotation < 0:
            self._rotation += 360

    def rotate(self, dt, v):
        self._rotation += v * dt
        self.bound_rotation()
        self.image = pygame.transform.rotate(self.orig_image, 360.0 - self._rotation)

    def rotate_left(self, dt):
        self.rotate(dt, -self.rotation_speed)

    def rotate_right(self, dt):
        self.rotate(dt, self.rotation_speed)

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
        self.decelerate(dt)
        self.move(dt)
