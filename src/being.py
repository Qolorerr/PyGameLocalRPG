from essence import Essence


class Being(Essence):
    def __init__(self, health: int, damage: int, location: tuple, texture, exp: int, cost: int):
        super().__init__(health, damage, location, texture, exp, cost)

    def received_damage(self, other_essence, type_of_attack):
        self.health -= other_essence.damage
        super().received_damage(other_essence, type_of_attack)