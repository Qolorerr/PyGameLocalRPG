import pygame

from general import textures, essences, camera
from map import Map
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface
from userInterface import UserInterface
from client import Client


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
    client = Client()
    client.send_info(b'[]')
    client.get_info()
    client.change_essences()
    pygame.init()
    resolution = (1000, 700)
    screen = pygame.display.set_mode(resolution)
    running = True
    mainHeroID = 0
    gameMap = Map(10, 10, mainHeroID)
    abilities = []
    for i in range(4):
        abilities.append(Ability(str(i), textures[3], 1, 1, True, 5, 5, damage=10, healing=10, shield=10))
    abilityInterface = AbilityInterface(abilities, resolution[0], resolution[1], (255, 255, 255))
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                client.send_info(bytes(str(list(map(bytes, essences))), encoding='utf-8'))
                client.get_info()
                client.change_essences()
                print("essences", essences)
        gameMap.render(screen)
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

main()