from pygame import image
import map

# Base class of all units and characters
class Essence:
    def __init__(self, health: int,
                 damage: int,
                 location: tuple,
                 type: int,
                 cell_size: int,
                 essence_code: int = 1,  # unicode
                 attack_range: int = 1,
                 move_distance: int = 1):
        self.health = health
        self.damage = damage
        self.location = location
        oldSize = textures[type].image.get_rect().size
        k = (cell_size - 2) / oldSize[0]
        newSize = (int(oldSize[0] * k), int(oldSize[1] * k))
        self.texture = pygame.transform.scale(textures[type].image, newSize)
        self.init_constant()
        self.live = self.ESSENSE_ALIVE
        self.essence_code = essence_code
        self.attack_range = attack_range
        self.move_distance = move_distance

    # Initialize constants for better code readability
    def init_constant(self):
        self.ESSENSE_ALIVE = 1
        self.ESSENSE_DIE = 2
        self.MAIN_ATTACK = 3
        self.RESPONSE_TO_ATTACK = 4

    # launches the consequences of an attack and returns a state essence: ALIVE or DIE
    def attack(self, other_essence, type_of_attack=3):  # 3 it is MAIN_ATTACK
        if (abs(other_essence.location[0] - self.location[0]) + abs(other_essence.location[1] - self.location[1])) <= \
                self.attack_range:
            other_essence.received_damage(self, type_of_attack)
        return self.alive()

    # Handling what we do when we take damage
    def received_damage(self, other_essence, type_of_attack):
        self.health -= other_essence.damage
        if type_of_attack == self.MAIN_ATTACK and self.alive() == self.ESSENSE_ALIVE:
            self.response_to_damage(other_essence)
            return self.ESSENSE_ALIVE
        return self.ESSENSE_DIE

    # Damage action
    def response_to_damage(self, other_essence):
        self.attack(other_essence, self.RESPONSE_TO_ATTACK)

    def alive(self):
        if self.health > 0:
            self.live = self.ESSENSE_ALIVE
            return self.ESSENSE_ALIVE
        self.live = self.ESSENSE_DIE
        return self.ESSENSE_DIE

    # Change location essence
    def move(self, new_location):
        if (abs(new_location[0] - self.location[0]) + abs(new_location[1] - self.location[1]) <= self.move_distance and
                new_location != self.location):
            self.location = new_location
            return True
        return False

    # Draw essence in location
    def render(self, screen, map):
        x = map.left + self.location[0] * map.cell_size
        y = map.top + self.location[1] * map.cell_size
        screen.blit(self.texture, (x + 1, y + 1))

    def __delete__(self, instance):
        self.health = 0
        self.damage = 0
        self.live = self.ESSENSE_DIE
        self.location = [None, None]
