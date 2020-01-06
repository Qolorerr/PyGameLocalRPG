import pygame
import math
from general import font_name_B


class InfoBar:
    def __init__(self, text: str):
        self.text = []
        self.cf = int(math.sqrt(len(text) / 2) * 20)
        self.line_breaker(text)
        self.font = pygame.font.Font(font_name_B, 20)
        self.size_x = self.cf * 2
        self.size_y = self.cf
        self.pos = None
        self.time = 5000

    def line_breaker(self, text):
        self.text = []
        s = ""
        for i in text.split():
            if len(s) <= int(self.cf) // 7:
                s += (i + " ")
            else:
                self.text.append(s)
                s = (i + " ")
        self.text.append(s)

    def render(self, screen):
        x = self.pos[0]
        y = self.pos[1]
        pygame.draw.rect(screen, (50, 50, 50), [x, y - self.size_y, self.size_x, self.size_y])
        for ind, s in enumerate(self.text):
            text = self.font.render(s, 1, (255, 255, 255))
            screen.blit(text, (x + 10, y - int(self.cf) + ind * 20))
