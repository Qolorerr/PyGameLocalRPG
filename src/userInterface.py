import pygame
from math import pi
from general import essences, textures, font_name_B, font_name_R
from hero import Hero
from being import Being


class UserInterface:
    def __init__(self, width: int,
                 height: int,
                 essence: int):
        self.width = width
        self.height = height
        self.essence = essences[essence]
        self.upTexture = textures['Timer']
        self.upIndent = 5
        self.timeFont = pygame.font.Font(font_name_R, 20)
        self.scoreFont = pygame.font.Font(font_name_B, 20, bold=True)
        self.coords = {"healing": (100, self.height - 100),
                       "shield": (225, self.height - 100),
                       "steps": (self.width - 350, self.height - 100),
                       "level": (self.width - 100, self.height - 100),
                       "gold": (self.width - 225, self.height - 100)}

    def circle_show(self, screen, centreCoords, color, midVal, currentVal, maxVal, arcCoords):
        pygame.draw.circle(screen, color, centreCoords, 50, 1)
        text = self.scoreFont.render(str(midVal), 1, (255, 255, 255))
        screen.blit(text, (centreCoords[0] - text.get_width() // 2, centreCoords[1] - text.get_height() // 2))
        coeff = (currentVal / maxVal) * 2 * pi - pi / 2
        pygame.draw.arc(screen, color, arcCoords, -coeff, pi / 2, 5)

    def render(self, screen, timer):
        # Show upper part of GUI
        upSize = self.upTexture.size
        coords = ((self.width - upSize[0]) // 2, 0)
        screen.blit(self.upTexture.image, coords)
        minutes = str(int(timer // (60 * 1000))).rjust(2, '0')
        seconds = str(int((timer // 1000) % 60)).rjust(2, '0')
        text = self.timeFont.render(minutes + ':' + seconds, 1, (255, 255, 255))
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.upIndent))
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
        self.circle_show(screen, (100, self.height - 100), (219, 77, 66), self.essence.health, self.essence.health,
                         self.essence.maxHealth, (50, self.height - 150, 100, 100))
        # Show shield
        self.circle_show(screen, (225, self.height - 100), (81, 119, 179), self.essence.shield, self.essence.shield,
                         self.essence.maxShield, (175, self.height - 150, 100, 100))
        # Show count of move points
        self.circle_show(screen, (self.width - 350, self.height - 100), (53, 146, 196), self.essence.steps,
                         self.essence.steps, self.essence.move_points, (self.width - 400, self.height - 150, 100, 100))
        # Show exp and level
        self.circle_show(screen, (self.width - 100, self.height - 100), (255, 255, 255), self.essence.level.get(),
                         self.essence.level.exp, self.essence.level.max_exp,
                         (self.width - 150, self.height - 150, 100, 100))
        # Show gold
        self.circle_show(screen, (self.width - 225, self.height - 100), (255, 215, 0), self.essence.gold,
                         self.essence.gold, self.essence.maxGold, (self.width - 275, self.height - 150, 100, 100))

    def get_user_inteface_cell(self, pos):
        for i in self.coords.keys():
            if self.coords[i][0] - 25 <= pos[0] <= self.coords[i][0] + 25:
                return i

    def show_mini_menu(self, pos):
        self.get_user_inteface_cell(pos)


    def upgrade_something(self, user_interface_cell):
        pass