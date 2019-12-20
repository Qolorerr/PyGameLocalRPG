import pygame

from general import textures, essences, camera
from map import Map
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface
from userInterface import UserInterface
from menu import menu, terminate


showing_essence = None


def filling_bar(screen, color, rect: tuple, value, maxValue):
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    k = value / maxValue
    indent = 1
    rect2 = [*rect]
    rect2[0] += indent
    rect2[1] += indent
    rect2[2] = int((rect2[2] - 2 * indent) * k)
    rect2[3] -= 2 * indent
    rect2 = tuple(rect2)
    pygame.draw.rect(screen, color, rect2)
    font = pygame.font.SysFont('Agency FB', 20, bold=True)
    text = font.render(str(value), 1, (255, 255, 255))
    screen.blit(text, (rect[0] + rect[2] // 2 - text.get_width() // 2, rect[1] + rect[3] // 2 - text.get_height() // 2))


def show_essence_info(screen):
    global showing_essence
    if showing_essence is None:
        return
    essence = None
    for i in range(len(essences)):
        if essences[i].essence_code == showing_essence:
            essence = i
    if essence is None:
        showing_essence = None
        return
    x, y, width, height, indent = 75, 200, 450, 625, 25
    background = pygame.Surface((width, height), pygame.SRCALPHA)
    background.fill((50, 50, 50, 100))
    screen.blit(background, (x, y))
    health = essences[essence].health
    damage = essences[essence].damage
    barwidth = width - indent * 2
    barheight = (height - 5 * indent) // 4
    filling_bar(screen, (219, 77, 66),
                (x + indent, y + 2 * barheight + 3 * indent, barwidth, barheight), damage, damage)
    font = pygame.font.SysFont('Agency FB', 40, bold=True)
    if type(essences[essence]) == Hero:
        maxHealth = essences[essence].maxHealth
        filling_bar(screen, (219, 77, 66),
                    (x + indent, y + barheight + 2 * indent, barwidth, barheight), health, maxHealth)
        shield = essences[essence].shield
        maxShield = essences[essence].maxShield
        filling_bar(screen, (81, 119, 179),
                    (x + indent, y + 3 * barheight + 4 * indent, barwidth, barheight), shield, maxShield)
        text = font.render(essences[essence].name + ' [' + str(essences[essence].level) + ']', 1, (255, 255, 255))
        screen.blit(text,
                    (x + width // 2 - text.get_width() // 2, y + indent + barheight // 2 - text.get_height() // 2))
    else:
        filling_bar(screen, (219, 77, 66),
                    (x + indent, y + barheight + 2 * indent, barwidth, barheight), health, health)
        filling_bar(screen, (81, 119, 179), (x + indent, y + 3 * barheight + 4 * indent, barwidth, barheight), 0, 1)
        text = font.render(essences[essence].name, 1, (255, 255, 255))
        screen.blit(text,
                    (x + width // 2 - text.get_width() // 2, y + indent + barheight // 2 - text.get_height() // 2))
    pygame.draw.rect(screen, (200, 0, 0), (x + width - indent, y, indent, indent))
    pygame.draw.line(screen, (255, 255, 255), (x + width - indent, y), (x + width, y + indent))
    pygame.draw.line(screen, (255, 255, 255), (x + width - indent, y + indent), (x + width, y))


def on_click(coords):
    global showing_essence
    mainHeroID = get_mainHeroID()
    for i in range(len(essences)):
        if essences[i].location == coords and essences[mainHeroID].attack_mode:
            if essences[mainHeroID].attack(essences[i]) == essences[i].ESSENSE_DIE:
                del(essences[i])
            elif essences[mainHeroID].alive() == essences[mainHeroID].ESSENSE_DIE:
                del(essences[mainHeroID])
        elif essences[i].location == coords:
            showing_essence = essences[i].essence_code


# Mouse click processing
def get_click(gameMap: Map, pos):
    global showing_essence
    if 500 <= pos[0] <= 525 and 200 <= pos[1] <= 225:
        showing_essence = None
        return
    cell = gameMap.get_cell((pos[0] - camera[0], pos[1] - camera[1]))
    on_click(cell)


def get_mainHeroID():
    mainHeroID = -1
    for i in range(len(essences)):
        if type(essences[i]) == Hero and essences[i].mainHero:
            mainHeroID = i
    return mainHeroID


def main():
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    nick = menu(screen, resolution)
    running = True
    gameMap = Map(10, 10)
    abilities = []
    abilities.append(Ability('0', 8, 1, 1, True, 5, 5, splashDamage=(40, 5)))
    abilities.append(Ability('1', 9, 1, 1, True, 5, 5, healing=10))
    abilities.append(Ability('2', 10, 1, 1, True, 5, 5, shield=20))
    abilities.append(Ability('3', 7, 1, 1, True, 5, 5, invisibility=1))
    abilityInterface = AbilityInterface(abilities, resolution[0], resolution[1], (255, 255, 255))
    essences.append(Hero(nick, 100, 30, (2, 3), 2, 1, 5, 10, True))
    essences.append(Being('BOT', 100, 50, (5, 6), 1, 10, 10, 2))
    infoObj = pygame.display.Info()
    mainHeroID = get_mainHeroID()
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
                terminate()
            if event.type == pygame.KEYDOWN:
                essences[mainHeroID].get_event(event.unicode, gameMap, screen)
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
        show_essence_info(screen)
        pygame.display.flip()


pygame.init()
main()