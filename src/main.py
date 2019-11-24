import pygame

from map import Map, Texture
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface


def on_click(gameMap: Map, coords):
    global essences
    for i in range(len(essences)):
        if essences[i].location == coords:
            if gameMap.choosedHero is None:
                if type(essences[i]) == Being:
                    return
                gameMap.choosedHero = i
            else:
                if essences[gameMap.choosedHero].attack(essences[i]) == essences[i].ESSENSE_DIE:
                    essences = essences[:i] + essences[(i + 1):]
                elif essences[gameMap.choosedHero].alive() == essences[gameMap.choosedHero].ESSENSE_DIE:
                    essences = essences[:gameMap.choosedHero] + essences[(gameMap.choosedHero + 1):]
                gameMap.choosedHero = None
            return
    if gameMap.choosedHero is not None:
        essences[gameMap.choosedHero].move(coords)
        gameMap.choosedHero = None

    # Mouse click processing
def get_click(gameMap: Map, pos):
    cell = gameMap.get_cell(pos)
    on_click(gameMap, cell)


def main():
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    running = True
    gameMap = Map(100, 100, textures)
    essences.append(Hero(100, 30, (2, 3), textures[2].image, move_distance=5, attack_range=3))
    essences.append(Being(100, 50, (5, 6), textures[1].image, 10, 10))
    abilities = []
    for i in range(4):
        abilities.append(Ability(str(i), textures[3], 1, 1, True))
    abilityInterface = AbilityInterface(abilities, 250, 600, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_click(gameMap, pygame.mouse.get_pos())
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