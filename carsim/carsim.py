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

    car = Car()

    while running:
        screen.blit(car.image, car.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in exit_keys):
                running = False


if __name__ == '__main__':
    main()
