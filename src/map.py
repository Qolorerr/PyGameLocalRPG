import pygame
from essence import Essence
from hero import Hero
from being import Being


# Load texture image
class Texture:
    def __init__(self, name):
        imageLink = "../res/textures/" + name
        self.image = pygame.image.load(imageLink)


# Cell object
class Cell:
    def __init__(self, size, type):
        self.type = type
        self.image = pygame.transform.scale(textures[type].image, (size, size))
        self.essence = None

    def change_type(self, type):
        self.type = type

    def add_essence(self, essence: Being or Hero):
        self.essence = essence

    def delete_essence(self):
        self.essence = None


# Game map object
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.board = [[Cell(self.cell_size - 2, 0) for __ in range(width)] for _ in range(height)]
        self.secondColor = (71, 86, 19)
        self.choosedCell = None

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
                screen.blit(self.board[i][j].image, (x + 1, y + 1))
                essence = self.board[i][j].essence
                if essence is None:
                    continue
                if essence.alive() == essence.ESSENSE_DIE:
                    continue
                texture = essence.texture
                size = texture.get_rect().size
                screen.blit(texture, (x + 1, y + 1 + self.cell_size - size[1]))

    # Get cell from mouse position
    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if pos[0] < self.left or pos[1] < self.top or x >= self.width or y >= self.height:
            return None
        return (x, y)

    # Nothing
    def on_click(self, coords):
        if coords is None:
            return
        essence = self.board[coords[1]][coords[0]].essence
        if essence is None:
            if self.choosedCell is None:
                return
            if not self.board[self.choosedCell[1]][self.choosedCell[0]].essence.can_move(coords):
                return
            hero = self.board[self.choosedCell[1]][self.choosedCell[0]].essence
            self.board[self.choosedCell[1]][self.choosedCell[0]].delete_essence()
            hero.location = [*coords]
            self.board[coords[1]][coords[0]].add_essence(hero)
            self.choosedCell = None
            return
        if self.choosedCell is None:
            if type(essence) == Being:
                return
            self.choosedCell = coords
            return
        self.board[coords[1]][coords[0]].essence.attack(self.board[self.choosedCell[1]][self.choosedCell[0]].essence)
        self.choosedCell = None

    # Mouse click processing
    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)

    # Adding new hero
    def add_hero(self, health: int, damage: int, location: list, moveRad: int, type=2):
        oldSize = textures[type].image.get_rect().size
        k = (self.cell_size - 2) / oldSize[0]
        newSize = (int(oldSize[0] * k), int(oldSize[1] * k))
        texture = pygame.transform.scale(textures[type].image, newSize)
        hero = Hero(health, damage, location, moveRad, texture)
        self.board[location[1]][location[0]].add_essence(hero)

    def add_being(self, health: int, damage: int, location: list, exp: int, cost: int, type=1):
        oldSize = textures[type].image.get_rect().size
        k = (self.cell_size - 2) / oldSize[0]
        newSize = (int(oldSize[0] * k), int(oldSize[1] * k))
        texture = pygame.transform.scale(textures[type].image, newSize)
        being = Being(health, damage, location, texture, exp, cost)
        self.board[location[1]][location[0]].add_essence(being)


def main():
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    running = True
    gameMap = Map(100, 100)
    essence = Essence(100, 10, [2, 3], 1, gameMap.cell_size, 1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameMap.get_click(pygame.mouse.get_pos())
                essence.move(gameMap.get_cell(pygame.mouse.get_pos()))
        gameMap.render(screen)
        essence.render(screen, gameMap)
        pygame.display.flip()
    pygame.quit()


pygame.init()
# List of textures
textures = [Texture('grass.jpg'), Texture('being1.png'), Texture('hero1.jpg')]
main()