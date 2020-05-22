import time

import pygame

from car import Car


def main():

    exit_keys = (pygame.K_q, pygame.K_ESCAPE)

    background_colour = (255, 255, 255)
    width, height = (1600, 900)
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('CarSim')
    screen.fill(background_colour)
    pygame.display.flip()
    running = True

    car = Car(width/2, height/2)

    dt = 0
    last = time.time_ns()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in exit_keys):
                running = False
                break

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            car.accelerate(dt)
        if pressed[pygame.K_a]:
            car.rotate_left(dt)
        if pressed[pygame.K_d]:
            car.rotate_right(dt)

        car.update(dt)

        screen.blit(car.image, car.rect)
        pygame.display.flip()

        current = time.time_ns()
        dt = (current - last) / 10 ** 9
        last = current


if __name__ == '__main__':
    main()
