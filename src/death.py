import pygame
from general import textures
from general import font_name_B


def death(screen, resolution, state):
    pygame.display.flip()
    screen.fill((0, 0, 0))
    if state == "die":
        screen.blit(textures['Death'].image, ((resolution[0] - 340) // 2, resolution[1] // 11 * 4))
    elif state == "win":
        font = pygame.font.Font(font_name_B, 20)
        text = font.render("You win!", 1, (255, 0, 0))
        screen.blit(text, (600, 400))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()