import pygame


from src.essence import Essence


class Hero(Essence):
    def __init__(self, health: int,
                 damage: int,
                 location: tuple,
                 texture: pygame.image,
                 essence_code: int = 1,
                 attack_range: int = 1,
                 move_distance: int = 1):
        super().__init__(health, damage, location, texture, essence_code, attack_range, move_distance)
        self.ablities = dict()