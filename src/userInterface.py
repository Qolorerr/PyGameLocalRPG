import pygame
from math import pi
from general import essences, textures, font_name_B, font_name_R
from hero import Hero
from being import Being
from infoBar import InfoBar


class CircleIndicator:
    def __init__(self, essence,
                 color,
                 centre_coord,
                 arc_coord):
        self.essence = essence
        self.color = color
        self.scoreFont = pygame.font.Font(font_name_B, 20, bold=True)
        self.centre_coord = centre_coord
        self.arc_coord = arc_coord
        self.middle_value = ''
        self.current_value = 0
        self.max_value = 1

    def update(self, current_value: int,
               max_value: int,
               middle_value = ''):
        if middle_value == '':
            self.middle_value = current_value
        else:
            self.middle_value = middle_value
        self.current_value = current_value
        self.max_value = max_value

    def render(self, screen, radius: int = 50):
        pygame.draw.circle(screen, self.color, self.centre_coord, radius, 1)
        text = self.scoreFont.render(str(self.middle_value), 1, (255, 255, 255))
        screen.blit(text, (self.centre_coord[0] - text.get_width() // 2, self.centre_coord[1] - text.get_height() // 2))
        coeff = (self.current_value / self.max_value) * 2 * pi - pi / 2
        pygame.draw.arc(screen, self.color, self.arc_coord, -coeff, pi / 2, 5)

    def get_infobar(self):
        pass


class Health(CircleIndicator):

    def get_infobar(self):
        return InfoBar("Name: health, MAX Health = " + str(self.essence.maxHealth) + ", now health = " +
                       str(self.essence.health) + " and can be improved" * int(self.essence.level.lvl_points > 0))


class Shield(CircleIndicator):
    def get_infobar(self):
        return InfoBar("Name: shield, MAX Shield = " + str(self.essence.maxShield) + ", now shield = " +
                       str(self.essence.shield) + " and can be improved" * int(self.essence.level.lvl_points > 0))


class Steps(CircleIndicator):
    def get_infobar(self):
        return InfoBar("Name: steps, MAX Steps = " + str(self.essence.move_distance) + ", now steps = " +
                       str(self.essence.steps) + " and can be improved" * int(self.essence.level.lvl_points > 0))


class Level(CircleIndicator):
    def get_infobar(self):
        return InfoBar("Name: level, Need experience for upgrade = " +
                       str(self.essence.level.max_exp - self.essence.level.exp))


class Gold(CircleIndicator):
    def get_infobar(self):
        return InfoBar("Name: gold, MAX Gold = " + str(self.essence.maxGold) + ", Gold = " + str(self.essence.gold) +
                       " and can be improved" * int(self.essence.level.lvl_points > 0))


class UserInterface:
    def __init__(self, width: int,
                 height: int,
                 essence: int,
                 ability_interface):
        self.width = width
        self.height = height
        self.essence = essences[essence]
        self.ability_interface = ability_interface
        self.upTexture = textures['Timer']
        self.upIndent = 5
        self.timeFont = pygame.font.Font(font_name_R, 20)
        self.scoreFont = pygame.font.Font(font_name_B, 20, bold=True)
        self.coords = {"health": (100, self.height - 100),
                       "shield": (225, self.height - 100),
                       "steps": (self.width - 350, self.height - 100),
                       "level": (self.width - 100, self.height - 100),
                       "gold": (self.width - 225, self.height - 100)}
        self.info_name = None
        self.max_gold = 100
        self.components_lvl = {"health": 1,
                               "steps": 1,
                               "gold": 1}
        self.health = Health(self.essence, (219, 77, 66), (100, self.height - 100), (50, self.height - 150, 100, 100))
        self.shield = Shield(self.essence, (81, 119, 179), (225, self.height - 100), (175, self.height - 150, 100, 100))
        self.steps = Steps(self.essence, (53, 146, 196), (self.width - 350, self.height - 100),
                           (self.width - 400, self.height - 150, 100, 100))
        self.level = Level(self.essence, (255, 255, 255), (self.width - 100, self.height - 100),
                           (self.width - 150, self.height - 150, 100, 100))
        self.gold = Gold(self.essence, (255, 215, 0), (self.width - 225, self.height - 100),
                         (self.width - 275, self.height - 150, 100, 100))

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
        self.health.update(self.essence.health, self.essence.maxHealth)
        self.health.render(screen)
        # Show shield
        self.shield.update(self.essence.shield, self.essence.maxShield)
        self.shield.render(screen)
        # Show count of move points
        self.steps.update(self.essence.steps, self.essence.move_distance)
        self.steps.render(screen)
        # Show exp and level
        self.level.update(self.essence.level.exp, self.essence.level.max_exp, self.essence.level.get())
        self.level.render(screen)
        # Show gold
        self.gold.update(self.essence.gold, self.essence.maxGold)
        self.gold.render(screen)
        # Show ability interface
        self.ability_interface.render(screen)
        if self.info_name is not None and 0 < self.info_name[0].time:
            self.info_name[0].render(screen)
            self.info_name[0].time -= self.info_name[1].tick()
        else:
            self.info_name = None

    def get_user_interface_cell(self, pos):
        for i in self.coords.keys():
            if self.coords[i][0] - 50 <= pos[0] <= self.coords[i][0] + 50 and \
                    self.coords[i][1] - 50 <= pos[1] <= self.coords[i][1] + 50:
                return i
        return False

    def show_info(self, pos):
        infoBar = self.ability_interface.get_infobar(pos, self.essence)
        if infoBar is not None:
            clock = pygame.time.Clock()
            self.info_name = [infoBar, clock]
            return
        name = self.get_user_interface_cell(pos)
        if name is not False:
            infoBar = InfoBar('')
            if name == "health":
                infoBar = self.health.get_infobar()
            elif name == "shield":
                infoBar = self.shield.get_infobar()
            elif name == "steps":
                infoBar = self.steps.get_infobar()
            elif name == "level":
                infoBar = self.level.get_infobar()
            elif name == "gold":
                infoBar = self.gold.get_infobar()
            clock = pygame.time.Clock()
            infoBar.pos = pos
            self.info_name = [infoBar, clock]

    def upgrade_component(self, component):
        if self.essence.level.lvl_points <= 0:
            return None
        if component == 'health' and self.components_lvl[component] < 5:
            self.essence.maxHealth += 10
            self.components_lvl[component] += 1
        elif component == "steps" and self.components_lvl[component] < 5:
            self.essence.move_distance += 1
            self.components_lvl[component] += 1
        elif component == "gold" and self.components_lvl[component] < 5:
            self.essence.maxGold += 100
            self.components_lvl[component] += 1
        else:
            return False
        return True
