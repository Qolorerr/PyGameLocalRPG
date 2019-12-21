# Load texture image
import pygame


class Texture:
    def __init__(self, name, cell_size=28):
        imageLink = "../res/textures/" + name
        self.image = pygame.image.load(imageLink)
        oldSize = self.image.get_rect().size
        k = (cell_size - 2) / oldSize[0]
        self.size = (int(oldSize[0] * k), int(oldSize[1] * k))
        self.image = pygame.transform.scale(self.image, self.size)


# List of textures
textures = {'Grass': Texture('grass.jpg'),
            'Being1': Texture('being1.png'),
            'Hero1': Texture('hero1.jpg'),
            'AttackZone': Texture('attack.png', 30),
            'MoveZone': Texture('moveZone.png', 30),
            'Sand': Texture('sand.jpg'),
            'Timer': Texture('upperUI.png', 550),
            'Invisibility': Texture('caveira.png', 75),
            'SplashDamage': Texture('sledge.png', 75),
            'Healing': Texture('doc.png', 75),
            'Shield': Texture('montagne.png', 75),
            'Logo': Texture('logo.png', 644),
            'Crack': Texture('cracking.png')}

essences = []

camera = []