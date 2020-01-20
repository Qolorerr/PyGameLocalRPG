import pygame

from general import textures, essences, camera
from essence import Essence
from level import Level
from abilityInterface import SplashDamage, Healing, Shield, Invisibility


class Hero(Essence):
    def __init__(self, name: str,
                 health: int,
                 damage: int,
                 location: list,
                 texture: int,
                 gold: int,
                 attack_range: int = 5,
                 move_distance: int = 10,
                 mainHero: bool = False):
        super().__init__(name, health, damage, location, texture, gold, attack_range, move_distance)
        self.mainHero = mainHero
        self.invisible = 0
        self.maxGold = 100
        self.level = Level(100, 1.1)
        self.attack_mode = False
        self.steps = 0
        self.upgrade_mode = False

    def step_update(self, ability_interface):
        self.steps = self.move_distance
        self.new_step(ability_interface)

    def do_step(self):
        if self.steps == 0:
            return False
        self.steps -= 1
        return True

    def attack(self, other_essence, type_of_attack=3):
        if self == other_essence:
            print(1)
            return self.ESSENSE_ALIVE
        if self.steps > 0 or type_of_attack == self.RESPONSE_TO_ATTACK:
            res = super().attack(other_essence, type_of_attack)
            self.do_step()
            return res

    def give_reward(self, other_essence):
        if type(other_essence) != Hero:
            return
        other_essence.level.add_exp(self.level.exp + 100 * self.level.level)
        other_essence.gold = min(other_essence.gold + self.gold, other_essence.maxGold)

    def move(self, new_location, map):
        if self.steps > 0:
            res = super().move(new_location, map)
            if res:
                self.do_step()
            return res

    def use_ability(self, ability, map):
        if ability is None or ability.cd_time > 0 or self.steps == 0 or ability.ability_lvl == 0:
            return False
        else:
            ability.active = True
        if ability.at_time > 0:
            return True
        self.do_step()
        if type(ability) == Invisibility:
            ability.cd_time = ability.cool_down
            self.invisible = 1
        elif type(ability) == SplashDamage:
            ability.cd_time = ability.cool_down
            ind = 0
            while ind < len(essences):
                i = essences[ind]
                if i == self:
                    ind += 1
                    continue
                if abs(i.location[0] - self.location[0]) + abs(i.location[1] - self.location[1]) <= ability.radius:
                    i.health -= ability.damage
                    if i.alive() == i.ESSENSE_DIE:
                        i.give_reward(self)
                        del(essences[ind])
                        continue
                ind += 1
            for i in range(-ability.radius, ability.radius + 1):
                for j in range(-ability.radius, ability.radius + 1):
                    if abs(i) + abs(j) > ability.radius:
                        continue
                    x = self.location[0] + i
                    y = self.location[1] + j
                    if 0 <= x <= map.width - 1 and 0 <= y <= map.height - 1:
                        map.board[y][x][1] = True
        elif type(ability) == Healing:
            ability.cd_time = ability.cool_down
            self.health += ability.heal
            self.health = min(self.health, self.maxHealth)
        elif type(ability) == Shield:
            ability.cd_time = ability.cool_down
            self.shield = min(ability.shield, self.maxHealth)
            self.maxShield = self.shield

    def get_event(self, keydown_unicode, gameMap):
        if keydown_unicode in ['w', 'ц']:
            new_location = (self.location[0], self.location[1] - 1)
            if self.move(new_location, gameMap):
                camera.append(camera[1] + (gameMap.cell_size))
                del(camera[1])
        elif keydown_unicode in ['s', 'ы']:
            new_location = (self.location[0], self.location[1] + 1)
            if self.move(new_location, gameMap):
                camera.append(camera[1] - (gameMap.cell_size))
                del (camera[1])
        elif keydown_unicode in ['a', 'ф']:
            new_location = (self.location[0] - 1, self.location[1])
            if self.move(new_location, gameMap):
                camera.append(camera[0] + (gameMap.cell_size))
                camera.append(camera[1])
                del(camera[0])
                del(camera[0])
        elif keydown_unicode in ['d', 'в']:
            new_location = (self.location[0] + 1, self.location[1])
            if self.move(new_location, gameMap):
                camera.append(camera[0] - (gameMap.cell_size))
                camera.append(camera[1])
                del (camera[0])
                del (camera[0])
        elif keydown_unicode in ['q', 'й']:
            self.attack_mode = not self.attack_mode
        elif keydown_unicode in ['u', 'г']:
            print(self.name)
            self.upgrade_mode = True

    def render_move_zone(self, screen, map):
        x = map.left + self.location[0] * map.cell_size
        y = map.top + self.location[1] * map.cell_size
        if self.mainHero:
            rect = (x + camera[0], y + camera[1], map.cell_size - map.indent, map.cell_size - map.indent)
            pygame.draw.rect(screen, pygame.Color("red"), rect, 2)
            for i in range(-self.steps, self.steps + 1):
                for j in range(-self.steps, self.steps + 1):
                    if abs(i) + abs(j) > self.steps:
                        continue
                    x = map.left + (self.location[0] + i) * map.cell_size
                    y = map.top + (self.location[1] + j) * map.cell_size
                    if 0 <= x <= map.left + (map.width - 1) * map.cell_size and 0 <= y <= map.top + (map.height - 1) * map.cell_size:
                        screen.blit(textures['MoveZone'].image, (x + camera[0], y + camera[1]))

    def render_can_attack(self, screen, map):
        for i in essences:
            if i == self:
                continue
            x, y = i.location
            if abs(x - self.location[0]) + abs(y - self.location[1]) <= self.attack_range:
                if type(i) == Hero and i.invisible == 1:
                    continue
                x = map.left + x * map.cell_size - map.indent
                y = map.top + y * map.cell_size - map.indent
                screen.blit(textures['AttackZone'].image, (x + camera[0], y + camera[1]))

    def render(self, screen, map):
        if self.mainHero:
            self.render_move_zone(screen, map)
        elif self.invisible > 0:
            return
        super().render(screen, map)
        if self.steps > 0:
            self.render_can_attack(screen, map)

    def new_step(self, ability_interface):
        for i in ability_interface.abilities:
            cont = not(i.update_ability())
            if cont:
                if i.name == "3":
                    self.invisible = 0
                elif i.name == "2":
                    self.shield = 0

    def __bytes__(self):
        info = eval(super().__bytes__().decode('utf-8'))
        info["type"] = "hero"
        info["invise"] = self.invisible
        info["maxGold"] = self.maxGold
        info["move"] = self.move_distance
        info["lvl_points"] = self.level.lvl_points
        info["level"] = (self.level.level, self.level.exp, self.level.max_exp)
        info = bytes(str(info), encoding='utf-8')
        return info
