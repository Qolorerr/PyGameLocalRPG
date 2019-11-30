import pygame

from general import textures, essences, camera
from map import Map
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface


def on_click(gameMap: Map, coords):
    for i in range(len(essences)):
        if essences[i].location == coords and essences[gameMap.choosedHero].attack_mode:
            if essences[gameMap.choosedHero].attack(essences[i]) == essences[i].ESSENSE_DIE:
                del(essences[i])
            elif essences[gameMap.choosedHero].alive() == essences[gameMap.choosedHero].ESSENSE_DIE:
                del(essences[gameMap.choosedHero])


# Mouse click processing
def get_click(gameMap: Map, pos):
    cell = gameMap.get_cell((pos[0] - camera[0], pos[1] - camera[1]))
    on_click(gameMap, cell)


def main():
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    running = True
    mainHeroID = 0
    gameMap = Map(10, 10, mainHeroID)
    essences.append(Hero(100, 30, (2, 3), textures[2].image, 1, 5, 5, True))
    essences.append(Being(100, 50, (5, 6), textures[1].image, 10, 10))
    infoObj = pygame.display.Info()
    cameraX = -gameMap.left - essences[mainHeroID].location[0] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_w - (gameMap.cell_size + gameMap.indent)) // 2
    cameraY = -gameMap.top - essences[mainHeroID].location[1] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_h - (gameMap.cell_size + gameMap.indent)) // 2
    camera.append(cameraX)
    camera.append(cameraY)
    abilities = []
    for i in range(4):
        abilities.append(Ability(str(i), textures[3], 1, 1, True))
    abilityInterface = AbilityInterface(abilities, 250, 600, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                essences[gameMap.choosedHero].get_event(event.unicode, gameMap, screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_click(gameMap, pygame.mouse.get_pos())
                abilityInterface.get_ability_on_click(pygame.mouse.get_pos())
        gameMap.render(screen)
        for i in range(len(essences)):
            if i == mainHeroID:
                continue
            essences[i].render(screen, gameMap)
        essences[mainHeroID].render(screen, gameMap)
        if essences[mainHeroID].attack_mode:
            essences[mainHeroID].render_can_attack(screen, gameMap)
        abilityInterface.render(screen)
        pygame.display.flip()
    pygame.quit()


pygame.init()
main()