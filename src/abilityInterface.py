import pygame


# Class hero's ability
class Ability:
    def __init__(self, name: str,
                 texture,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int,
                 **kwargs: dict):  # Qualities of ability, for example: damage 10, healing 100 or others
        self.name = name
        self.texture = texture
        self.ability_code = ability_code
        self.ability_lvl = 1
        self.max_lvl = max_lvl
        self.active = active
        self.cool_down = cool_down
        self.cd_time = 0
        self.action_time = action_time
        self.at_time = 0
        self.qualities = kwargs
        self.init_constant()

    def init_constant(self):
        self.NOW_MAX_LVL = 0

    # Increase lvl ability
    def lvl_up(self):
        if self.ability_lvl == self.max_lvl:
            return self.NOW_MAX_LVL
        self.ability_lvl += 1
        self.improve_ability()
        return self.ability_lvl

    # Increase in parameters of ability
    def improve_ability(self):
        pass


# Interface all abilities of hero
class AbilityInterface:
    def __init__(self, abilities: list,  # len tuple needs = 4
                 window_width: int,
                 window_height: int,
                 color):
        self.abilities = abilities
        self.ability_size = abilities[0].texture.size[0]
        self.color = color
        self.indent = 3
        self.left = (window_width - len(abilities) * self.ability_size - (len(abilities) + 1) * self.indent) // 2
        self.window_height = window_height
        self.width = 4
        self.height = 1

    def render(self, screen):
        x = self.left
        y = self.window_height - self.ability_size - 2 * self.indent
        pygame.draw.rect(screen, self.color,
                         [x, y, self.ability_size * 4 + 5 * self.indent, self.ability_size + 2 * self.indent])
        x += self.indent
        y += self.indent
        for abl in self.abilities:
            screen.blit(abl.texture.image, (x, y))
            x += self.indent + abl.texture.size[0]

    # Return ability when user clicked on ability
    def get_ability_on_click(self, pos):
        x = (pos[0] - self.left) // self.ability_size
        y = (pos[1] - self.window_height - self.ability_size - 2 * self.indent) // self.ability_size
        if (pos[0] < self.left or pos[1] < self.window_height - self.ability_size - 2 * self.indent or
                x >= self.width or y >= self.height):
            return None
        return self.abilities[x]
