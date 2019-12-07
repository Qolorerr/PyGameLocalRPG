import pygame
from math import pi
from general import essences, textures
from hero import Hero
from being import Being


class UserInterface:
    def __init__(self, width: int,
                 height: int,
                 essence: int):
        self.width = width
        self.height = height
        self.essence = essences[essence]
        self.upTexture = textures[7]
        self.upIndent = 5
        self.timeFont = pygame.font.SysFont('Agency FB', 20)
        self.scoreFont = pygame.font.SysFont('Agency FB', 20, bold=True)

    def render(self, screen):

        # Show upper part of GUI
        upSize = self.upTexture.size
        coords = ((self.width - upSize[0]) // 2, 0)
        screen.blit(self.upTexture.image, coords)
        text = self.timeFont.render('00:00', 1, (255, 255, 255))
        screen.blit(text, (self.width // 2 - 20, self.upIndent))
        heroes = 0
        beings = 0
        for i in essences:
            if type(i) == Hero and i.alive() == i.ESSENSE_ALIVE:
                heroes += 1
            elif type(i) == Being and i.alive() == i.ESSENSE_ALIVE:
                beings += 1
        text = self.scoreFont.render(str(heroes), 1, (255, 255, 255))
        screen.blit(text, (self.width // 2 - text.get_width() - 45, self.upIndent))
        text = self.scoreFont.render(str(beings), 1, (255, 255, 255))
        screen.blit(text, (self.width // 2 + 45, self.upIndent))

        # Show health
        coords = (100, self.height - 100)
        pygame.draw.circle(screen, (255, 255, 255), coords, 50, 1)
        text = self.scoreFont.render(str(self.essence.health), 1, (255, 255, 255))
        screen.blit(text, (100 - text.get_width() // 2, self.height - 100 - text.get_height() // 2))
        coords = (50, self.height - 150, 100, 100)
        health = (self.essence.health / self.essence.maxHealth) * 2 * pi - pi / 2
        pygame.draw.arc(screen, (255, 255, 255), coords, -health, pi / 2, 5)

        # Show shield
        coords = (225, self.height - 100)
        pygame.draw.circle(screen, (81, 119, 179), coords, 50, 1)
        text = self.scoreFont.render(str(self.essence.shield), 1, (255, 255, 255))
        screen.blit(text, (225 - text.get_width() // 2, self.height - 100 - text.get_height() // 2))
        coords = (175, self.height - 150, 100, 100)
        shield = (self.essence.shield / self.essence.maxShield) * 2 * pi - pi / 2
        pygame.draw.arc(screen, (81, 119, 179), coords, -shield, pi / 2, 5)

        # Show count of move points
        coords = (self.width - 100, self.height - 100)
        pygame.draw.circle(screen, (53, 146, 196), coords, 50, 1)
        text = self.scoreFont.render(str(self.essence.steps), 1, (255, 255, 255))
        screen.blit(text, (self.width - 100 - text.get_width() // 2, self.height - 112))
        coords = (self.width - 150, self.height - 150, 100, 100)
        steps = (self.essence.steps / self.essence.move_points) * 2 * pi - pi / 2
        pygame.draw.arc(screen, (53, 146, 196), coords, -steps, pi / 2, 5)