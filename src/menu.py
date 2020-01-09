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

    def render(self, screen):
        mouse = pygame.mouse.get_pos()
        if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (
                self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
            pygame.draw.rect(screen, self.color_hover, self.rect, 5)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, 1, (0, 0, 0))
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


def menu(screen, resolution):
    mainmenu = True
    rect = (resolution[0] // 5 * 2, resolution[1] // 13 * 5, resolution[0] // 5, resolution[1] // 11)
    nick_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "NICK")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 7, resolution[0] // 7, resolution[1] // 11)
    create_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CREATE GAME")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CONNECT")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 11, resolution[0] // 7, resolution[1] // 11)
    settings_btn = Button(rect, (125, 125, 125), (200, 200, 200), "SETTINGS")
    host = False
    setting = False
    while mainmenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                terminate()
            nick_box.event_handle(event)
            host = create_btn.event_handle(event)
            mainmenu = not host and not connect_btn.event_handle(event)
            setting = settings_btn.event_handle(event)
        screen.blit(textures['Logo'].image, ((resolution[0] - 644) // 2, resolution[1] // 11 * 2))
        nick_box.render(screen)
        create_btn.render(screen)
        connect_btn.render(screen)
        settings_btn.render(screen)
        pygame.display.flip()
        if setting:
            settings(screen, resolution)
            setting = False
    if host:
        screen.fill((0, 0, 0))
        rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 3, resolution[0] // 5, resolution[1] // 11)
        players_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "NUMBER OF PLAYERS")
        rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 5, resolution[0] // 5, resolution[1] // 11)
        connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CREATE")
        mainmenu = True
        while mainmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                players_box.event_handle(event)
                mainmenu = not connect_btn.event_handle(event)
            players_box.render(screen)
            connect_btn.render(screen)
            pygame.display.flip()
        return host, nick_box.text, players_box.text
    screen.fill((0, 0, 0))
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 3, resolution[0] // 5, resolution[1] // 11)
    ip_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "IP")
    rect = (resolution[0] // 5 * 2, resolution[1] // 11 * 5, resolution[0] // 5, resolution[1] // 11)
    connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CONNECT")
    mainmenu = True
    while mainmenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            ip_box.event_handle(event)
            mainmenu = not connect_btn.event_handle(event)
        ip_box.render(screen)
        connect_btn.render(screen)
        pygame.display.flip()
    print(ip_box.text)
    print(nick_box.text)
    screen.fill((0, 0, 0))
    return host, nick_box.text, ip_box.text
