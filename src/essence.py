from general import camera, essences, textures


# Base class of all units and characters
class Essence:
    def __init__(self, name: str,
                 health: int,
                 damage: int,
                 location: list,
                 texture: int,
                 gold: int,
                 attack_range: int = 1,
                 move_distance: int = 1):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.damage = damage
        self.shield = 0
        self.maxShield = 1
        self.location = location
        self.texture_name = texture
        self.texture = textures[texture]
        self.gold = gold
        self.init_constant()
        self.live = self.ESSENSE_ALIVE
        self.attack_range = attack_range
        self.move_distance = move_distance
        self.essence_code = None

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
        if type_of_attack == self.MAIN_ATTACK and self.alive() == self.ESSENSE_ALIVE:
            self.response_to_damage(other_essence)
            return self.ESSENSE_ALIVE
        if self.alive() == self.ESSENSE_DIE:
            self.give_reward(other_essence)
            return self.ESSENSE_DIE

    def give_reward(self, other_essence):
        pass

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
    def move(self, new_location, map):
        loc_other_essences = [i.location for i in essences]
        if map.width > new_location[0] >= 0 and map.height > new_location[1] >= 0 and \
                new_location not in loc_other_essences:
            self.location = new_location
            return True
        return False

    # Draw essence in location
    def render(self, screen, map):
        x = map.left + self.location[0] * map.cell_size + map.indent + camera[0]
        y = map.top + self.location[1] * map.cell_size + map.indent + camera[1]
        w, h = self.texture.image.get_rect()[-2:]
        y -= h - w
        screen.blit(self.texture.image, (x, y))

    def __bytes__(self):
        info = {"name": self.name,
                "health": self.health,
                "damage": self.damage,
                "location": self.location,
                "texture": self.texture_name,
                "gold": self.gold,
                "code": self.essence_code,
                "live": self.live,
                "maxHealth": self.maxHealth,
                "shield": self.shield,
                "maxShield": self.maxShield,
                "type": 'essence'}
        info = bytes(str(info), encoding='utf-8')
        return info

    def __delete__(self, instance):
        self.health = 0
        self.damage = 0
        self.live = self.ESSENSE_DIE
        self.location = [None, None]
