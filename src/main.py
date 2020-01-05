import pygame

from general import essences, camera, font_name_B
from map import Map
from hero import Hero
from being import Being
from abilityInterface import Ability
from abilityInterface import AbilityInterface
from userInterface import UserInterface
from menu import menu, terminate
from death import death
import ctypes
from client import Client


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
    font = pygame.font.Font(font_name_B, 20, bold=True)
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
    font = pygame.font.Font(font_name_B, 40, bold=True)
    maxHealth = essences[essence].maxHealth
    filling_bar(screen, (219, 77, 66),
                (x + indent, y + barheight + 2 * indent, barwidth, barheight), health, maxHealth)
    shield = essences[essence].shield
    maxShield = essences[essence].maxShield
    filling_bar(screen, (81, 119, 179),
                (x + indent, y + 3 * barheight + 4 * indent, barwidth, barheight), shield, maxShield)
    if type(essences[essence]) == Hero:
        text = essences[essence].name + ' [' + str(essences[essence].level.get()) + ']'
    else:
        text = essences[essence].name
    text = font.render(text, 1, (255, 255, 255))
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
        elif list(essences[i].location) == list(coords):
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
    client = Client()
    step = None
    while step is None:
        step = client.get_info()
    if client.you_main_client:
        client.first_client(int(input()))
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    nick = menu(screen, resolution)
    running = True
    gameMap = Map(100, 100)
    abilities = []
    abilities.append(Ability('0', 'SplashDamage', 1, 1, True, 5, 5, splashDamage=(40, 5)))
    abilities.append(Ability('1', 'Healing', 1, 1, True, 5, 5, healing=10))
    abilities.append(Ability('2', 'Shield', 1, 1, True, 5, 5, shield=20))
    abilities.append(Ability('3', 'Invisibility', 1, 1, True, 5, 5, invisibility=1))
    abilityInterface = AbilityInterface(abilities, resolution[0], resolution[1], (255, 255, 255))
    infoObj = pygame.display.Info()
    mainHeroID = get_mainHeroID()
    essences[mainHeroID].name = nick
    cameraX = -gameMap.left - essences[mainHeroID].location[0] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_w - (gameMap.cell_size + gameMap.indent)) // 2
    cameraY = -gameMap.top - essences[mainHeroID].location[1] * (gameMap.cell_size + gameMap.indent) + \
              (infoObj.current_h - (gameMap.cell_size + gameMap.indent)) // 2
    camera.append(cameraX)
    camera.append(cameraY)
    userinterface = UserInterface(infoObj.current_w, infoObj.current_h, mainHeroID)
    timer = 0
    clock = pygame.time.Clock()
    if step is True:
        timer = 1.5 * 60 * 1000
    else:
        essences[get_mainHeroID()].steps = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            if client.your_hero_id == get_mainHeroID():
                mainHeroID = get_mainHeroID()
                if event.type == pygame.KEYDOWN:
                    essences[mainHeroID].get_event(event.unicode, gameMap, screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    get_click(gameMap, pygame.mouse.get_pos())
                    essences[mainHeroID].use_ability(abilityInterface.get_ability_on_click(pygame.mouse.get_pos()), gameMap)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    timer = 0
                    essences[mainHeroID].step = 0
        timer = max(0, timer - clock.tick())
        gameMap.render(screen)
        i = 0
        while i < len(essences):
            if essences[i].alive() == essences[i].ESSENSE_DIE:
                del(essences[i])
            else:
                i += 1
        mainHeroID = get_mainHeroID()
        if mainHeroID == -1:
            death(screen, resolution)
        for i in range(len(essences)):
            if i == mainHeroID:
                continue
            essences[i].render(screen, gameMap)
        essences[mainHeroID].render(screen, gameMap)
        if essences[mainHeroID].attack_mode:
            essences[mainHeroID].render_can_attack(screen, gameMap)
        abilityInterface.render(screen)
        userinterface.render(screen, timer)
        show_essence_info(screen)
        pygame.display.flip()
        info = client.get_info()
        if info is not None:
            if info is True:
                print('----info')
                step = True
                timer = 1.5 * 60 * 1000
                essences[client.your_hero_id].steps = essences[client.your_hero_id].move_distance
        if step is True and (essences[get_mainHeroID()].steps == 0 or timer == 0):
            essences[client.your_hero_id].steps = 0
            timer = 0
            client.send_msg(str(list(map(bytes, essences))))
            step = False
    pygame.quit()
    client.disconnect()


main()