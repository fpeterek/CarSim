import time

import pygame

from car import Car


def main():

    exit_keys = (pygame.K_q, pygame.K_ESCAPE)

    background_colour = (255, 255, 255)
    width, height = (1400, 750)
    screen = pygame.display.set_mode((width, height))

    pygame.font.init()
    font = pygame.font.SysFont('Helvetica', 16)

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
            car.accelerate()
        if pressed[pygame.K_a]:
            car.rotate_left(dt)
        if pressed[pygame.K_d]:
            car.rotate_right(dt)
        if pressed[pygame.K_s]:
            car.apply_brake(dt)
        if pressed[pygame.K_SPACE]:
            car.full_speed()

        car.update(dt)

        screen.fill(background_colour)
        pygame.draw.rect(screen, (255, 0, 0), car.rect)
        screen.blit(car.image, car.rect)

        speed = font.render(f'v={round(car.velocity)} kmh', True, (0, 0, 0))
        screen.blit(speed, (width-speed.get_width()-5, 5))

        pygame.display.flip()

        current = time.time_ns()
        dt = (current - last) / 10 ** 9
        last = current


if __name__ == '__main__':
    main()
