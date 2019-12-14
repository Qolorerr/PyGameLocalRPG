import pygame

from general import textures, essences, camera
from map import Map
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface
from userInterface import UserInterface


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
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    running = True
    mainHeroID = 0
    gameMap = Map(10, 10, mainHeroID)
    abilities = []
    abilities.append(Ability('0', 9, 1, 1, True, 5, 5, splashDamage=(40, 5)))
    abilities.append(Ability('1', 10, 1, 1, True, 5, 5, healing=10))
    abilities.append(Ability('2', 11, 1, 1, True, 5, 5, shield=20))
    abilities.append(Ability('3', 8, 1, 1, True, 5, 5, invisibility=1))
    abilityInterface = AbilityInterface(abilities, resolution[0], resolution[1], (255, 255, 255))
    essences.append(Hero(100, 30, (2, 3), 2, 1, 5, 10, True))
    essences.append(Being(100, 50, (5, 6), 1, 10, 10))
    infoObj = pygame.display.Info()
    cameraX = -gameMap.left - essences[mainHeroID].location[0] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_w - (gameMap.cell_size + gameMap.indent)) // 2
    cameraY = -gameMap.top - essences[mainHeroID].location[1] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_h - (gameMap.cell_size + gameMap.indent)) // 2
    camera.append(cameraX)
    camera.append(cameraY)
    userinterface = UserInterface(infoObj.current_w, infoObj.current_h, mainHeroID)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                essences[gameMap.choosedHero].get_event(event.unicode, gameMap, screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_click(gameMap, pygame.mouse.get_pos())
                essences[mainHeroID].use_ability(abilityInterface.get_ability_on_click(pygame.mouse.get_pos()))
        gameMap.render(screen)
        i = 0
        while i < len(essences):
            if essences[i].alive() == essences[i].ESSENSE_DIE:
                del(essences[i])
            else:
                i += 1
        for i in range(len(essences)):
            if i == mainHeroID:
                continue
            essences[i].render(screen, gameMap)
        essences[mainHeroID].render(screen, gameMap)
        if essences[mainHeroID].attack_mode:
            essences[mainHeroID].render_can_attack(screen, gameMap)
        abilityInterface.render(screen)
        userinterface.render(screen)
        pygame.display.flip()
    pygame.quit()


pygame.init()
main()