import math

from pygame.rect import Rect
from pygame.sprite import Sprite
import pygame

from vector import Vector


class Car(Sprite):

    default_weight = 1800  # kg
    default_top_speed = 230  # km/h
    sprite_dim = (32, 15)
    default_acceleration = 3
    default_deceleration = 1
    default_rotation = 15

    def __init__(self, x, y):
        Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('resources/car.png'), Car.sprite_dim)
        self.rect = self.image.get_rect()

        self.rect = Rect(x, y, self.image.get_rect().width, self.image.get_rect().height)

        self._velocity = 0.0
        self._rotation = 0.0
        self.weight = Car.default_weight
        self.acceleration = Car.default_acceleration
        self.deceleration = Car.default_deceleration
        self.rotation_speed = Car.default_rotation
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

    def rotate_left(self, dt):
        self._rotation -= self.rotation_speed * dt

    def rotate_right(self, dt):
        self._rotation += self.rotation_speed * dt

    def move(self, dt):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.width
        h = self.rect.height
        f = self.forces
        dx = f.x * dt
        dy = f.y * dt
        self.rect = Rect(x+dx, y+dy, w, h)

    def update(self, dt):
        self.decelerate(dt)
        self.move(dt)
