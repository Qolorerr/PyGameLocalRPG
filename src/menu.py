import pygame
import sys
from general import textures, font_name_B


def terminate():
    pygame.quit()
    sys.exit()


class Button:
    def __init__(self, rect: tuple,
                 color: tuple,
                 color_hover: tuple = (-1, -1, -1),
                 text: str = ''):
        self.rect = rect
        self.color = color
        if color_hover[0] == -1:
            self.color_hover = color
        else:
            self.color_hover = color_hover
        self.text = text
        self.font = pygame.font.Font(font_name_B, 40, bold=True)

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (
                    self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
                return True
            return False

    def render(self, screen, text_color=(0, 0, 0)):
        mouse = pygame.mouse.get_pos()
        if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (
                self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
            pygame.draw.rect(screen, self.color_hover, self.rect, 5)
            text_color = tuple(map(lambda x: 255 - x, text_color))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, 1, text_color)
        x = self.rect[0] + self.rect[2] // 2 - text.get_width() // 2
        y = self.rect[1] + self.rect[3] // 2 - text.get_height() // 2
        screen.blit(text, (x, y))


class InputBox:
    def __init__(self, rect: tuple,
                 color: tuple,
                 color_hover: tuple = (-1, -1, -1),
                 text: str = ''):
        self.rect = rect
        self.color = color
        if color_hover[0] == -1:
            self.color_hover = color
        else:
            self.color_hover = color_hover
        self.text = text
        self.setup = True
        self.font = pygame.font.Font(font_name_B, 40, bold=True)
        self.active = False

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (
                    self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
                if self.setup:
                    self.text = ''
                    self.setup = False
                self.active = True
                return
            self.active = False
            return
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_ESCAPE:
                self.active = False
                return
            elif self.active and key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                if len(self.text) == 0:
                    return
                self.text = self.text[:-1]
            elif self.active:
                self.text += event.unicode
                self.text = self.text[:20]

    def render(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color_hover, self.rect)
            pygame.draw.rect(screen, self.color, self.rect, 2)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, 1, (0, 0, 0))
        x = self.rect[0] + 1
        y = self.rect[1] + self.rect[3] // 2 - text.get_height() // 2
        screen.blit(text, (x, y))


class CheckBox:
    def __init__(self, rect: tuple,
                 active: bool,
                 color: tuple,
                 color_checked: tuple = (-1, -1, -1),
                 text: str = ''):
        self.rect = rect
        self.color = color
        if color_checked[0] == -1:
            self.color_checked = color
        else:
            self.color_checked = color_checked
        self.text = text
        self.font = pygame.font.Font(font_name_B, 40, bold=True)
        self.active = active

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (
                    self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
                self.active = not self.active

    def render(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color_checked, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text = self.font.render(self.text, 1, self.color)
        x = self.rect[0] + self.rect[2] + 5
        y = self.rect[1] + self.rect[3] // 2 - text.get_height() // 2
        screen.blit(text, (x, y))


def get_data_from_configs():
    try:
        f = open('../res/configs.cfg', 'r')
        configs = dict()
        for line in f:
            key, value = line[:-1].split(': ')
            configs[key] = value
        f.close()
    except FileNotFoundError:
        configs = dict()
    return configs


def set_data_to_configs(configs: dict):
    f = open('../res/configs.cfg', 'w')
    for key, value in configs.items():
        f.write(str(key) + ': ' + str(value) + '\n')
    f.close()


def rules(screen, resolution):
    rule = True
    x, y = resolution[0] // 15, resolution[1] // 13
    font = pygame.font.Font(font_name_B, 40, bold=True)
    text = ["""'WASD' - MOVING                      'q' - ATTACK MODE"""]
    text += ["""'p' - END TURN                       'u' - UPGRADE MODE"""]
    text += ["""'F4' - EXIT"""]
    text += [""""""]
    text += ["""CLICK ON ENEMY TO GET INFO ABOUT HIM"""]
    text += ["""CLICK ON ENEMY IN ATTACK MODE AND ATTACK HIM (IF IT HIGHLIGHT)"""]
    text += [""""""]
    text += ["""CLICK ON ABILITY OR INDICATOR (HEALTH, SHIELD, STEPS, GOLD) IN UPGRADE MODE TO UPGRADE IT"""]
    text += ["""NEED LEVEL POINTS (YOU GET 1 LEVEL POINT PER LEVEL) AND GOLD"""]
    rect = (resolution[0] // 7 * 5, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    exit_btn = Button(rect, (125, 125, 125), (200, 200, 200), "EXIT")
    while rule:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            rule = not exit_btn.event_handle(event)
        screen.fill((0, 0, 0))
        for line in text:
            text_rend = font.render(line, 1, (200, 200, 200))
            rect = text_rend.get_rect()
            rect.left = x
            rect.top = y
            y += rect.height + 10
            screen.blit(text_rend, rect)
        y = resolution[1] // 13
        exit_btn.render(screen)
        pygame.display.flip()


def settings(screen, resolution):
    configs = get_data_from_configs()
    music = True
    if 'music' in configs:
        music = eval(configs['music'])
    sounds = True
    if 'sounds' in configs:
        sounds = eval(configs['sounds'])
    setting = True
    rect = (resolution[0] // 15 * 7, resolution[1] // 13 * 5, resolution[0] // 25, resolution[0] // 25)
    music_box = CheckBox(rect, music, (125, 125, 125), (200, 200, 200), "MUSIC")
    rect = (resolution[0] // 15 * 7, resolution[1] // 13 * 7, resolution[0] // 25, resolution[0] // 25)
    sounds_box = CheckBox(rect, sounds, (125, 125, 125), (200, 200, 200), "SOUNDS")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    save_btn = Button(rect, (125, 125, 125), (200, 200, 200), "SAVE")
    while setting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            music_box.event_handle(event)
            sounds_box.event_handle(event)
            setting = not save_btn.event_handle(event)
        screen.fill((0, 0, 0))
        music_box.render(screen)
        sounds_box.render(screen)
        save_btn.render(screen)
        pygame.display.flip()
    configs['music'] = str(music_box.active)
    configs['sounds'] = str(sounds_box.active)
    set_data_to_configs(configs)


def connecting(screen, resolution):
    connect = True
    screen.fill((0, 0, 0))
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 3, resolution[0] // 5, resolution[1] // 11)
    ip_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "IP")
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 5, resolution[0] // 5, resolution[1] // 11)
    connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CONNECT")
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 8, resolution[0] // 5, resolution[1] // 11)
    return_btn = Button(rect, (125, 125, 125), (200, 200, 200), "RETURN")
    while connect:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            ip_box.event_handle(event)
            connect = not connect_btn.event_handle(event)
            if return_btn.event_handle(event):
                return None
        ip_box.render(screen)
        connect_btn.render(screen)
        return_btn.render(screen)
        pygame.display.flip()
    return ip_box.text


def creating(screen, resolution):
    create = True
    screen.fill((0, 0, 0))
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 3, resolution[0] // 5, resolution[1] // 11)
    players_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "NUMBER OF PLAYERS")
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 5, resolution[0] // 5, resolution[1] // 11)
    create_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CREATE")
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 8, resolution[0] // 5, resolution[1] // 11)
    return_btn = Button(rect, (125, 125, 125), (200, 200, 200), "RETURN")
    while create:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            players_box.event_handle(event)
            create = not create_btn.event_handle(event)
            if return_btn.event_handle(event):
                return None
        players_box.render(screen)
        create_btn.render(screen)
        return_btn.render(screen)
        pygame.display.flip()
    return players_box.text


def menu(screen, resolution):
    mainmenu = True
    rect = (resolution[0] // 5 * 2, resolution[1] // 13 * 5, resolution[0] // 5, resolution[1] // 11)
    nick_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "NICK")
    rect = (resolution[0] // 7 * 2, resolution[1] // 13 * 7, resolution[0] // 7, resolution[1] // 11)
    create_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CREATE GAME")
    rect = (resolution[0] // 7 * 4, resolution[1] // 13 * 7, resolution[0] // 7, resolution[1] // 11)
    connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CONNECT")
    rect = (resolution[0] // 7 * 2, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    settings_btn = Button(rect, (125, 125, 125), (200, 200, 200), "SETTINGS")
    rect = (resolution[0] // 7 * 4, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    rules_btn = Button(rect, (125, 125, 125), (200, 200, 200), "RULES")
    create = False
    connect = False
    setting = False
    rule = False
    while mainmenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            nick_box.event_handle(event)
            create = create_btn.event_handle(event)
            connect = connect_btn.event_handle(event)
            setting = settings_btn.event_handle(event)
            rule = rules_btn.event_handle(event)
        screen.fill((0, 0, 0))
        screen.blit(textures['Logo'].image, ((resolution[0] - 644) // 2, resolution[1] // 11 * 2))
        nick_box.render(screen)
        create_btn.render(screen)
        connect_btn.render(screen)
        settings_btn.render(screen)
        rules_btn.render(screen)
        pygame.display.flip()
        if create:
            players = creating(screen, resolution)
            if players is not None:
                return True, nick_box.text, players
            create = False
        if connect:
            ip = connecting(screen, resolution)
            if ip is not None:
                return False, nick_box.text, ip
            connect = False
        if setting:
            settings(screen, resolution)
            setting = False
        if rule:
            rules(screen, resolution)
            rule = False
