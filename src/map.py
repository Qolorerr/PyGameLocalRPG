import pygame
from essence import Essence


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


# Game map object
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.board = [[Cell(self.cell_size - 2, 0)] * width for _ in range(height)]
        self.secondColor = (71, 86, 19)

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

    # Get cell from mouse position
    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if pos[0] < self.left or pos[1] < self.top or x >= self.width or y >= self.height:
            return None
        return (x, y)

    # Nothing
    def on_click(self, coords):
        pass

    # Mouse click processing
    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)


def main():
    screen = pygame.display.set_mode((800, 600))
    running = True
    gameMap = Map(100, 100)
    essence = Essence(100, 10, [2, 3], Cell(gameMap.cell_size - 2, 1), 1)
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
textures = [Texture('0.jpg'), Texture('1.png')]
main()