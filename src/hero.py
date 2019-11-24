from src.essence import Essence


class Hero(Essence):
    def __init__(self, health: int, damage: int, location: list, moveRad: int, texture):
        super().__init__(health, damage, location, texture)
        self.moveRad = moveRad
        self.ablities = dict()

    def can_move(self, coords):
        if abs(coords[0] - self.location[0]) + abs(coords[1] - self.location[1]) > self.moveRad:
            return False
        return True