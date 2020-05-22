from pygame.sprite import Sprite
import pygame


class Car(Sprite):

    default_weight = 1800  # kg
    default_top_speed = 230  # km/h
    sprite_dim = (32, 15)

    def __init__(self):
        Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('resources/car.png'), Car.sprite_dim)
        self.rect = self.image.get_rect()

        self.velocity = 0.0
        self.rotation = 0.0
        self.weight = Car.default_weight
