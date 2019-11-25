from essence import Essence


class Being(Essence):
    def __init__(self, health: int, damage: int, location: tuple, texture, exp: int, cost: int):
        super().__init__(health, damage, location, texture, exp, cost)