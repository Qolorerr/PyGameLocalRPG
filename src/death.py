import pygame
from menu import terminate
from general import textures


def death(screen, resolution):
    pygame.display.flip()
    screen.fill((0, 0, 0))
    screen.blit(textures['Death'].image, ((resolution[0] - 340) // 2, resolution[1] // 11 * 4))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()