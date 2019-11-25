import pygame

from general import textures, camera
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface


# Game map object
class Map:
    def __init__(self, width, height, choosedHero):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.indent = 1
        self.cell_size = textures[0].image.get_rect().size[0] + 2 * self.indent
        self.board = [[textures[0].image for __ in range(width)] for _ in range(height)]
        self.secondColor = (71, 86, 19)
        self.choosedHero = choosedHero

    # Change map settings
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Map rendering
    def render(self, screen):
        screen.fill(self.secondColor)
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                screen.blit(self.board[i][j], (x + self.indent + camera[0], y + self.indent + camera[1]))

    # Get cell from mouse position
    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if pos[0] < self.left or pos[1] < self.top or x >= self.width or y >= self.height:
            return None
        return (x, y)

