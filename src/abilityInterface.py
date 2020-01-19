import pygame
from general import textures, essences
from infoBar import InfoBar


# Class hero's ability
class Ability:
    def __init__(self, name: str,
                 texture: str,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int):
        self.name = name
        self.texture = textures[texture]
        self.ability_code = ability_code
        self.ability_lvl = 1
        self.max_lvl = max_lvl
        self.active = active
        self.cool_down = cool_down
        self.cd_time = 0
        self.action_time = action_time
        self.at_time = 0
        self.init_constant()
        self.coeff = 1.2
        self.cost = 100

    def init_constant(self):
        self.NOW_MAX_LVL = -1
        self.NOT_HAVE_POINTS = -2
        self.ENOUGH_GOLD = -3

    # Increase lvl ability
    def lvl_up(self, essence):
        if essences[essence].level.lvl_points <= 0:
            return self.NOT_HAVE_POINTS
        if self.ability_lvl == self.max_lvl:
            return self.NOW_MAX_LVL
        if essences[essence].gold < self.cost:
            return self.ENOUGH_GOLD
        self.ability_lvl += 1
        self.improve_ability()
        return self.ability_lvl

    # Increase in parameters of ability
    def improve_ability(self):
        pass

    def update_ability(self):
        if self.cd_time > 0:
            self.cd_time -= 1
        if self.active:
            self.at_time += 1
        if self.at_time >= self.action_time:
            self.at_time = 0
            return False
        else:
            return True

    def get_infobar(self, essence):
        pass


class SplashDamage(Ability):
    def __init__(self, name: str,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int,
                 damage: int = 40,
                 radius: int = 5):
        super().__init__(name, 'SplashDamage', ability_code, max_lvl, active, cool_down, action_time)
        self.damage = damage
        self.radius = radius

    def improve_ability(self):
        self.damage = self.damage * self.coeff

    def get_infobar(self, essence):
        return InfoBar("Ability level = " + str(self.ability_lvl) +
                       " Deals damage = " + str(self.damage) + ", range = " + str(self.radius) +
                       ", cool down = " + str(self.cool_down) + ", make " + str(self.cd_time) + " moves to reapply" +
                       " and can be improved" * int(essence.level.lvl_points > 0) * int(essence.gold >= self.cost))


class Healing(Ability):
    def __init__(self, name: str,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int,
                 heal: int = 20):
        super().__init__(name, 'Healing', ability_code, max_lvl, active, cool_down, action_time)
        self.heal = heal

    def improve_ability(self):
        self.heal = self.heal * self.coeff

    def get_infobar(self, essence):
        return InfoBar("Ability level = " + str(self.ability_lvl) + " Heals you " + str(self.heal) + " health"
                       ", cool down = " + str(self.cool_down) + ", make " + str(self.cd_time) +
                       " moves to reapply" + " and can be improved" * int(essence.level.lvl_points > 0) *
                       int(essence.gold >= self.cost))


class Shield(Ability):
    def __init__(self, name: str,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int,
                 shield: int = 20):
        super().__init__(name, 'Shield', ability_code, max_lvl, active, cool_down, action_time)
        self.shield = shield

    def improve_ability(self):
        self.shield = self.shield * self.coeff

    def get_infobar(self, essence):
        return InfoBar("Ability level = " + str(self.ability_lvl) +
                       " Gives you a shield that blocks damage = " + str(self.shield) +
                       ", cool down = " + str(self.cool_down) + ", make " + str(self.cd_time) + " moves to reapply" +
                       " and can be improved" * int(essence.level.lvl_points > 0) * int(essence.gold >= self.cost))


class Invisibility(Ability):
    def __init__(self, name: str,
                 ability_code: int,
                 max_lvl: int,
                 active: bool,
                 cool_down: int,
                 action_time: int,
                 invisible: int = 1):
        super().__init__(name, 'Invisibility', ability_code, max_lvl, active, cool_down, action_time)
        self.invisible = invisible

    def improve_ability(self):
        self.cool_down -= 1

    def get_infobar(self, essence):
        return InfoBar("Ability level = " + str(self.ability_lvl) +
                       " Gives you complete invisibility for " + str(self.invisible) +
                       " turns, cool down = " + str(self.cool_down)
                       + ", make " + str(self.cd_time) + " moves to reapply" +
                       " and can be improved" * int(essence.level.lvl_points > 0) * int(essence.gold >= self.cost))


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
        w = self.ability_size * 4 + 5 * self.indent
        h = self.ability_size + 2 * self.indent
        background = pygame.Surface((w, h), pygame.SRCALPHA)
        background.fill((*self.color, 100))
        screen.blit(background, (x, y))
        pygame.draw.rect(screen, self.color, [x, y, w, h], self.indent)
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

    def get_infobar(self, pos, essence):
        ability = self.get_ability_on_click(pos)
        if ability is not None:
            infoBar = ability.get_infobar(essence)
            infoBar.pos = pos
            return infoBar
        return None
