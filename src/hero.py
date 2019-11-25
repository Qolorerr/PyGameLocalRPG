import pygame

from general import textures, essences
from essence import Essence


class Hero(Essence):
    def __init__(self, health: int,
                 damage: int,
                 location: tuple,
                 texture: pygame.image,
                 essence_code: int = 1,
                 attack_range: int = 1,
                 move_distance: int = 1,
                 mainHero: bool = False):
        super().__init__(health, damage, location, texture, essence_code, attack_range, move_distance)
        self.mainHero = mainHero
        self.ablities = dict()
        self.attack_mode = False

    def get_event(self, keydown_unicode, gameMap, screen):
        if keydown_unicode == 'w':
            new_location = (self.location[0], self.location[1] - 1)
            self.move(new_location, gameMap)
        elif keydown_unicode == 's':
            new_location = (self.location[0], self.location[1] + 1)
            self.move(new_location, gameMap)
        elif keydown_unicode == 'a':
            new_location = (self.location[0] - 1, self.location[1])
            self.move(new_location, gameMap)
        elif keydown_unicode == 'd':
            new_location = (self.location[0] + 1, self.location[1])
            self.move(new_location, gameMap)
        elif keydown_unicode == 'q':
            self.attack_mode = not self.attack_mode

    def render_move_zone(self, screen, map):
        x = map.left + self.location[0] * map.cell_size
        y = map.top + self.location[1] * map.cell_size
        if self.mainHero:
            pygame.draw.rect(screen, pygame.Color("red"), (x, y, map.cell_size, map.cell_size), 2)
            for i in range(-self.move_distance, self.move_distance + 1):
                for j in range(-self.move_distance, self.move_distance + 1):
                    if abs(i) + abs(j) > self.move_distance:
                        continue
                    x = map.left + (self.location[0] + i) * map.cell_size - map.indent
                    y = map.top + (self.location[1] + j) * map.cell_size - map.indent
                    screen.blit(textures[5].image, (x, y))

    def render_can_attack(self, screen, map):
        for i in essences:
            if i == self:
                continue
            x, y = i.location
            if abs(x - self.location[0]) + abs(y - self.location[1]) <= self.attack_range:
                x = map.left + x * map.cell_size - map.indent
                y = map.top + y * map.cell_size - map.indent
                screen.blit(textures[4].image, (x, y))

    def render(self, screen, map):
        self.render_move_zone(screen, map)
        super().render(screen, map)