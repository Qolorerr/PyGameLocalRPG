import pygame
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface


# Load texture image
class Texture:
    def __init__(self, name, cell_size=28):
        imageLink = "../res/textures/" + name
        self.image = pygame.image.load(imageLink)
        oldSize = self.image.get_rect().size
        k = (cell_size - 2) / oldSize[0]
        self.size = (int(oldSize[0] * k), int(oldSize[1] * k))
        self.image = pygame.transform.scale(self.image, self.size)

# Game map object
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = textures[0].image.get_rect().size[0] + 2
        self.board = [[textures[0].image for __ in range(width)] for _ in range(height)]
        self.secondColor = (71, 86, 19)
        self.choosedHero = None

    # Change map settings
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Map rendering
    def render(self, screen):
        screen.fill(self.secondColor)
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                screen.blit(self.board[i][j], (x + 1, y + 1))

    # Get cell from mouse position
    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if pos[0] < self.left or pos[1] < self.top or x >= self.width or y >= self.height:
            return None
        return (x, y)

    # Attacks and moves
    def on_click(self, coords):
        global essences
        for i in range(len(essences)):
            if essences[i].location == coords:
                if self.choosedHero is None:
                    if type(essences[i]) == Being:
                        return
                    self.choosedHero = i
                else:
                    if essences[self.choosedHero].attack(essences[i]) == essences[i].ESSENSE_DIE:
                        essences = essences[:i] + essences[(i + 1):]
                    self.choosedHero = None
                return
        if self.choosedHero is not None:
            essences[self.choosedHero].move(coords)
            self.choosedHero = None

    # Mouse click processing
    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)


def main():
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    running = True
    gameMap = Map(100, 100)
    essences.append(Hero(100, 30, (2, 3), textures[2].image, move_distance=5, attack_range=3))
    essences.append(Being(100, 10, (5, 6), textures[1].image, 10, 10))
    abilities = []
    for i in range(4):
        abilities.append(Ability(str(i), textures[3], 1, 1, True))
    abilityInterface = AbilityInterface(abilities, 250, 600, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameMap.get_click(pygame.mouse.get_pos())
                abilityInterface.get_ability_on_click(pygame.mouse.get_pos())
        gameMap.render(screen)
        for i in essences:
            i.render(screen, gameMap)
        abilityInterface.render(screen)
        pygame.display.flip()
    pygame.quit()


pygame.init()
# List of textures
textures = [Texture('grass.jpg'), Texture('being1.png'), Texture('hero1.jpg'), Texture('ability1.jpg', 75)]
essences = []
main()