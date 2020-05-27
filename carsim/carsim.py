import time

import pygame

from car import Car
from direction import Direction


def main():

    exit_keys = (pygame.K_ESCAPE, )

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if car.cruise_control_on:
                    car.disable_cruise_control()
                else:
                    car.enable_cruise_control(130)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if car.front_wheel.has_target and car.front_wheel.target_rotation < 0:
                    car.unset_steer_target()
                else:
                    car.steer_target(20, Direction.LEFT)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if car.front_wheel.has_target and car.front_wheel.target_rotation > 0:
                    car.unset_steer_target()
                else:
                    car.steer_target(20, Direction.RIGHT)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            car.accelerate()
        if pressed[pygame.K_a]:
            car.steer_left(dt)
        if pressed[pygame.K_d]:
            car.steer_right(dt)
        if pressed[pygame.K_s]:
            car.apply_brake(dt)
        if pressed[pygame.K_SPACE]:
            car.full_speed()

        car.update(dt)

        screen.fill(background_colour)
        pygame.draw.rect(screen, (255, 0, 0), car.rect)
        screen.blit(car.image, car.rect)
        pygame.draw.line(screen, car.sensor.color, car.sensor.center, car.sensor.get_end(), 2)

        speed = font.render(f'v={round(car.velocity)} kmh', True, (0, 0, 0))
        screen.blit(speed, (width-speed.get_width()-5, 5))

        cc = font.render(f'CC {("off", "on")[car.cruise_control_on]}', True, (0, 0, 0))
        screen.blit(cc, (width-cc.get_width()-5, 10 + speed.get_height()))

        wheel = font.render(f'Wheel: {round(car.front_wheel.rotation)}°', True, (0, 0, 0))
        screen.blit(wheel, (width - wheel.get_width() - 5, 15 + speed.get_height()*2))

        target = font.render(f'Target: {round(car.front_wheel.target_rotation)}°', True, (0, 0, 0))
        screen.blit(target, (width - target.get_width() - 5, 20 + speed.get_height() * 3))

        pygame.display.flip()

        current = time.time_ns()
        dt = (current - last) / 10 ** 9
        last = current


if __name__ == '__main__':
    main()
