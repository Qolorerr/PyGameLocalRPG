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
textures = [Texture('grass.jpg'),
            Texture('being1.png'),
            Texture('hero1.jpg'),
            Texture('ability1.jpg', 75),
            Texture('attack.png', 30),
            Texture('moveZone.png', 30)]

essences = []
