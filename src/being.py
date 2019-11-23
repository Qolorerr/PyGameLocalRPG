from src.essence import Essence


class Being(Essence):
    def __init__(self, health: int, damage: int, location: list, texture, exp: int, cost: int):
        super().__init__(health, damage, location, texture)
        self.given_experience = exp
        self.given_gold = cost

    def give_reward(self, hero):
        if self.live == self.ESSENSE_DIE:
            # Hero get exp and gold when being die
            pass