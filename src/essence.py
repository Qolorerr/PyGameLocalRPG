# Base class of all units and characters
class Essence:
    def __init__(self, health: int, damage: int, location: list, texture):
        self.health = health
        self.damage = damage
        self.location = location
        self.texture = texture
        self.init_constant()
        self.live = self.ESSENSE_ALIVE

    # Initialize constants for better code readability
    def init_constant(self):
        self.ESSENSE_ALIVE = 1
        self.ESSENSE_DIE = 2
        self.MAIN_ATTACK = 3
        self.RESPONSE_TO_ATTACK = 4

    # launches the consequences of an attack and returns a state essence: ALIVE or DIE
    def attack(self, other_essence, type_of_attack=3):
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

    def __delete__(self, instance):
        self.health = 0
        self.damage = 0
        self.live = self.ESSENSE_DIE
        self.location = [None, None]


A = Essence(100, 10, [1, 1], 0)
B = Essence(1000, 1, [1, 1], 0)
while B.live != B.ESSENSE_DIE and A.live != A.ESSENSE_DIE:
    A.attack(B)
    print(B.health, A.health)
