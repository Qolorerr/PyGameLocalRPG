import pygame
from general import camera


# Base class of all units and characters
class Essence:
    def __init__(self, health: int,
                 damage: int,
                 location: tuple,
                 texture: pygame.image,
                 exp: int,
                 gold: int,
                 essence_code: int = 1,  # unicode
                 attack_range: int = 1,
                 move_distance: int = 1):
        self.health = health
        self.damage = damage
        self.location = location
        self.texture = texture
        self.exp = exp
        self.gold = gold
        self.init_constant()
        self.live = self.ESSENSE_ALIVE
        self.essence_code = essence_code
        self.attack_range = attack_range
        self.move_distance = move_distance
        self.who_killed_me = None

    # Initialize constants for better code readability
    def init_constant(self):
        self.ESSENSE_ALIVE = 1
        self.ESSENSE_DIE = 2
        self.MAIN_ATTACK = 3
        self.RESPONSE_TO_ATTACK = 4

    # launches the consequences of an attack and returns a state essence: ALIVE or DIE
    def attack(self, other_essence, type_of_attack=3):  # 3 it is MAIN_ATTACK
        if (abs(other_essence.location[0] - self.location[0]) + abs(other_essence.location[1] - self.location[1])) <= \
                self.attack_range and self.live == self.ESSENSE_ALIVE and self is not other_essence:
            other_essence.received_damage(self, type_of_attack)
            self.alive()
        res = other_essence.alive()
        if res == self.ESSENSE_DIE:
            return res

    # Handling what we do when we take damage
    def received_damage(self, other_essence, type_of_attack):
        self.health -= other_essence.damage
        if type_of_attack == self.MAIN_ATTACK and self.alive() == self.ESSENSE_ALIVE:
            self.response_to_damage(other_essence)
            return self.ESSENSE_ALIVE
        if self.alive() == self.ESSENSE_DIE:
            self.who_killed_me = other_essence
            return self.ESSENSE_DIE

    # Damage action
    def response_to_damage(self, other_essence):
        self.attack(other_essence, self.RESPONSE_TO_ATTACK)

    def give_reward(self, other_essence):
        if self.live == self.ESSENSE_DIE:
            # Hero get exp and gold when being die
            pass

    def alive(self):
        if self.health > 0:
            self.live = self.ESSENSE_ALIVE
            return self.ESSENSE_ALIVE
        self.live = self.ESSENSE_DIE
        return self.ESSENSE_DIE

    # Change location essence
    def move(self, new_location, map):
        if map.width > new_location[0] >= 0 and map.height > new_location[1] >= 0:
            self.location = new_location
            return True
        return False

    # Draw essence in location
    def render(self, screen, map):
        x = map.left + self.location[0] * map.cell_size
        y = map.top + self.location[1] * map.cell_size
        screen.blit(self.texture, (x + map.indent + camera[0], y + map.indent + camera[1]))

    def __delete__(self, instance):
        self.health = 0
        self.damage = 0
        self.live = self.ESSENSE_DIE
        self.location = [None, None]
