from essence import Essence
from hero import Hero


class Being(Essence):
    def __init__(self, name, health: int, damage: int, location: tuple, texture, gold: int):
        super().__init__(name, health, damage, location, texture, gold)
        self.exp = 20

    def give_reward(self, other_essence):
        if type(other_essence) != Hero:
            return
        other_essence.level.add_exp(self.exp)
        other_essence.gold = min(other_essence.gold + self.gold, other_essence.maxGold)