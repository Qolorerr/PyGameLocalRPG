import pygame

from general import textures, essences, camera
from essence import Essence


class Hero(Essence):
    def __init__(self, health: int,
                 damage: int,
                 location: tuple,
                 texture: int,
                 essence_code: int = 1,
                 attack_range: int = 1,
                 move_distance: int = 1,
                 mainHero: bool = False):
        super().__init__(health, damage, location, texture, 0, 0, essence_code, attack_range, move_distance)
        self.maxHealth = health
        self.mainHero = mainHero
        self.shield = 0
        self.maxShield = 1
        self.invisible = 0
        self.maxExp = 100
        self.maxGold = 100
        self.level = 1
        self.attack_mode = False
        self.steps = move_distance
        self.move_points = move_distance

    def do_step(self):
        if self.steps == 0:
            return False
        self.steps -= 1
        return True

    def attack(self, other_essence, type_of_attack=3):
        if self.steps > 0:
            res = super().attack(other_essence, type_of_attack)
            self.do_step()
            return res

    def received_damage(self, other_essence, type_of_attack):
        if self.shield > 0:
            self.shield = max(0, self.shield - other_essence.damage)
        else:
            self.health -= other_essence.damage
        return super().received_damage(other_essence, type_of_attack)

    def give_reward(self, other_essence):
        if type(other_essence) != Hero:
            return
        other_essence.exp += self.exp
        if other_essence.exp >= other_essence.maxExp:
            other_essence.exp -= other_essence.maxExp
            other_essence.level += 1
            other_essence.maxExp = int(other_essence.maxExp * 1.1)
        other_essence.gold = min(other_essence.gold + self.gold, other_essence.maxGold)

    def move(self, new_location, map):
        if self.steps > 0:
            res = super().move(new_location, map)
            self.do_step()
            return res

    def use_ability(self, ability):
        if ability is None or ability.cd_time > 0:
            return False
        if ability.at_time > 0:
            return True
        if 'invisibility' in ability.qualities:
            self.invisible = 1
        if 'splashDamage' in ability.qualities:
            dmg, rad = ability.qualities['splashDamage']
            for i in essences:
                if i == self:
                    continue
                if abs(i.location[0] - self.location[0]) + abs(i.location[1] - self.location[1]) <= rad:
                    i.health -= dmg
        if 'healing' in ability.qualities:
            self.health += ability.qualities['healing']
            self.health = min(self.health, self.maxHealth)
        if 'shield' in ability.qualities:
            self.shield = min(ability.qualities['shield'], self.maxHealth)
            self.maxShield = self.shield

    def get_event(self, keydown_unicode, gameMap, screen):
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

    def render_move_zone(self, screen, map):
        x = map.left + self.location[0] * map.cell_size
        y = map.top + self.location[1] * map.cell_size
        if self.mainHero:
            pygame.draw.rect(screen, pygame.Color("red"), (x + camera[0], y + camera[1], map.cell_size, map.cell_size), 2)
            for i in range(-self.steps, self.steps + 1):
                for j in range(-self.steps, self.steps + 1):
                    if abs(i) + abs(j) > self.steps:
                        continue
                    x = map.left + (self.location[0] + i) * map.cell_size - map.indent
                    y = map.top + (self.location[1] + j) * map.cell_size - map.indent
                    if -1 <= x < map.left + (map.width - 1) * map.cell_size and -1 <= y < map.top + (map.height - 1) * map.cell_size:
                        screen.blit(textures[5].image, (x + camera[0], y + camera[1]))

    def render_can_attack(self, screen, map):
        for i in essences:
            if i == self:
                continue
            x, y = i.location
            if abs(x - self.location[0]) + abs(y - self.location[1]) <= self.attack_range:
                x = map.left + x * map.cell_size - map.indent
                y = map.top + y * map.cell_size - map.indent
                screen.blit(textures[4].image, (x + camera[0], y + camera[1]))

    def render(self, screen, map):
        if self.mainHero:
            self.render_move_zone(screen, map)
        elif self.invisible > 0:
            print(1)
            return
        super().render(screen, map)
        if self.steps > 0:
            self.render_can_attack(screen, map)