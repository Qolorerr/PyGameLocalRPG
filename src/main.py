import pygame
import ctypes
import socket
import os
import time
from random import shuffle
from subprocess import Popen

from general import essences, camera, font_name_B
from map import Map
from hero import Hero
from abilityInterface import Ability
from abilityInterface import AbilityInterface
from userInterface import UserInterface
from menu import menu, terminate
from death import death
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
        try:
            if essences[i].location == coords and essences[mainHeroID].attack_mode:
                if essences[mainHeroID].attack(essences[i]) == essences[i].ESSENSE_DIE:
                    print('essence die kak bbI')
                    essences[i].give_reward(essences[mainHeroID])
                    del(essences[i])
                elif essences[mainHeroID].alive() == essences[mainHeroID].ESSENSE_DIE:
                    del(essences[mainHeroID])
            elif list(essences[i].location) == list(coords):
                showing_essence = essences[i].essence_code
        except:
            pass


# Mouse click processing
def get_click(gameMap: Map, pos):
    global showing_essence
    if 500 <= pos[0] <= 525 and 200 <= pos[1] <= 225:
        showing_essence = None
        return
    cell = gameMap.get_cell((pos[0] - camera[0], pos[1] - camera[1]))
    if cell is not None:
        on_click(cell)


def get_mainHeroID():
    mainHeroID = -1
    for i in range(len(essences)):
        if type(essences[i]) == Hero and essences[i].mainHero:
            mainHeroID = i
    return mainHeroID


def main():
    pygame.init()
    your_turn = pygame.mixer.Sound('../res/sounds/YourTurn.wav')
    ctypes.windll.user32.SetProcessDPIAware()
    u32 = ctypes.windll.user32
    resolution = (u32.GetSystemMetrics(0), u32.GetSystemMetrics(1))
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    data = menu(screen, resolution)
    players = 1
    if data[0]:
        host, nick, players = data
        ip = socket.gethostbyname(socket.gethostname())
        print(data, ip)
        os.getcwd()
        Popen('python new_server.py')
        print('Server started')
        time.sleep(1)
    else:
        host, nick, ip = data
    try:
        players = int(players)
    except ValueError:
        players = 2
    print("My IP:", socket.gethostbyname(socket.gethostname()))
    client = Client(ip)
    client.nick = nick
    step = None
    while step is None:
        step = client.get_info()
    if client.you_main_client:
        client.first_client(players)
    print('Client started')
    running = True
    gameMap = Map(100, 100)
    abilities = []
    abilities.append(Ability('0', 'SplashDamage', 1, 8, False, 2, 1, splashDamage=[40, 5]))
    abilities.append(Ability('1', 'Healing', 2, 8, False, 3, 1, healing=20))
    abilities.append(Ability('2', 'Shield', 3, 8, False, 12, 3, shield=20))
    abilities.append(Ability('3', 'Invisibility', 4, 8, False, 20, 2, invisibility=1))
    abilityInterface = AbilityInterface(abilities, resolution[0], resolution[1], (0, 0, 0))
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
    playlist = ['Ancient_Stones.wav', 'Awake.wav', 'Dragonsearch.wav', 'Secunda.wav', 'The_City_Gates.wav']
    shuffle(playlist)
    playlist = list(map(lambda x: '../res/sounds/' + x, playlist))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.load(playlist[-1])
    playlist = [playlist[-1]] + playlist[:-1]
    pygame.mixer.music.queue(playlist[-1])
    playlist = [playlist[-1]] + playlist[:-1]
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    if step is True:
        timer = 1.5 * 60 * 1000
    else:
        essences[get_mainHeroID()].steps = 0
    while running:
        i = 0
        while i < len(essences):
            if essences[i].alive() == essences[i].ESSENSE_DIE:
                del (essences[i])
            else:
                i += 1
        mainHeroID = get_mainHeroID()
        if mainHeroID == -1:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                mainHeroID = get_mainHeroID()
                if mainHeroID != -1:
                    del(essences[mainHeroID])
            if event.type == pygame.USEREVENT:
                pygame.mixer.music.queue(playlist[-1])
                playlist = [playlist[-1]] + playlist[:-1]
            if get_mainHeroID() != -1:
                mainHeroID = get_mainHeroID()
                if event.type == pygame.KEYDOWN:
                    essences[mainHeroID].get_event(event.unicode, gameMap)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        userinterface.show_info(event.pos)
                        abilityInterface.show_info(event.pos, essences[mainHeroID])
                    elif event.button == 1:
                        if essences[mainHeroID].upgrade_mode:
                            ability = abilityInterface.get_ability_on_click(event.pos)
                            component = userinterface.get_user_interface_cell(event.pos)
                            if ability is not None:
                                point = ability.lvl_up(mainHeroID)
                                if point > 0:
                                    essences[mainHeroID].level.lvl_points -= 1
                                    essences[mainHeroID].gold -= ability.cost
                                    ability.cost = int(ability.cost * ability.coeff)
                                essences[mainHeroID].upgrade_mode = False
                            elif component is not None:
                                point = userinterface.upgrade_component(component)
                                essences[mainHeroID].level.lvl_points -= int(point is True)
                                essences[mainHeroID].upgrade_mode = False
                        else:
                            get_click(gameMap, pygame.mouse.get_pos())
                            mainHeroID = get_mainHeroID()
                            essences[mainHeroID].use_ability(abilityInterface.get_ability_on_click(pygame.mouse.get_pos()), gameMap)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    timer = 0
                    essences[mainHeroID].step = 0
        mainHeroID = get_mainHeroID()
        if mainHeroID != -1:
            timer = max(0, timer - clock.tick())
            gameMap.render(screen)
            for i in range(len(essences)):
                if i == mainHeroID:
                    continue
                essences[i].render(screen, gameMap)
            essences[mainHeroID].render(screen, gameMap)
            if essences[mainHeroID].attack_mode:
                essences[mainHeroID].render_can_attack(screen, gameMap)
            abilityInterface.render(screen)
            userinterface.essence = essences[mainHeroID]
            userinterface.render(screen, timer)
            show_essence_info(screen)
            pygame.display.flip()
        info = client.get_info()
        if info is not None:
            if info is True:
                step = True
                timer = 1.5 * 60 * 1000
                if get_mainHeroID() == -1:
                    break
                client.alive = False
                essences[get_mainHeroID()].step_update(abilityInterface)
                your_turn.play()
        if step is True and (get_mainHeroID() == -1 or essences[get_mainHeroID()].steps == 0 or timer == 0):
            mainHeroID = get_mainHeroID()
            if mainHeroID != -1:
                essences[mainHeroID].steps = 0
                timer = 0
                client.send_msg(str(list(map(bytes, essences))))
                step = False
            else:
                break
    client.send_msg(str(list(map(bytes, essences))))
    death(screen, resolution)
    pygame.quit()
    client.disconnect()


main()