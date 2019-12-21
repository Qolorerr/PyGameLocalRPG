from essence import Essence


class Being(Essence):
    def __init__(self, name: str,
                 health: int,
                 damage: int,
                 location: tuple,
                 texture: int,
                 exp: int,
                 cost: int,
                 essence_code: int = 1,
                 attack_range: int = 1,
                 move_distance: int = 1):
        super().__init__(name, health, damage, location, texture, cost, essence_code, attack_range, move_distance)
        self.exp = exp

    def received_damage(self, other_essence, type_of_attack):
        self.health -= other_essence.damage
        return super().received_damage(other_essence, type_of_attack)

    def give_reward(self, other_essence):
        other_essence.level.add_exp(self.exp)
        other_essence.gold = min(other_essence.gold + self.gold, other_essence.maxGold)