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

    def check_clicked(self):
        mouse = pygame.mouse.get_pos()
        if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
            return True
        return False

    def render(self, screen):
        mouse = pygame.mouse.get_pos()
        if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
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
        self.font = pygame.font.Font(font_name_B, 40, bold=True)
        self.active = False

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (self.rect[0] <= mouse[0] <= self.rect[0] + self.rect[2]) and (self.rect[1] <= mouse[1] <= self.rect[1] + self.rect[3]):
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


def menu(screen, resolution):
    mainmenu = True
    rect = (resolution[0] // 5 * 2, resolution[1] // 13 * 5, resolution[0] // 5, resolution[1] // 11)
    nick_box = InputBox(rect, (125, 125, 125), (200, 200, 200), "NICK")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 7, resolution[0] // 7, resolution[1] // 11)
    create_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CREATE GAME")
    rect = (resolution[0] // 7 * 3, resolution[1] // 13 * 9, resolution[0] // 7, resolution[1] // 11)
    connect_btn = Button(rect, (125, 125, 125), (200, 200, 200), "CONNECT")
    host = False
    while mainmenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            nick_box.event_handle(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                host = create_btn.check_clicked()
                mainmenu = not host and not connect_btn.check_clicked()
        screen.blit(textures['Logo'].image, ((resolution[0] - 644) // 2, resolution[1] // 11 * 2))
        nick_box.render(screen)
        create_btn.render(screen)
        connect_btn.render(screen)
        pygame.display.flip()
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mainmenu = not connect_btn.check_clicked()
            players_box.render(screen)
            connect_btn.render(screen)
            pygame.display.flip()
        return (host, nick_box.text, players_box.text)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mainmenu = not connect_btn.check_clicked()
        ip_box.render(screen)
        connect_btn.render(screen)
        pygame.display.flip()
    print(ip_box.text)
    print(nick_box.text)
    screen.fill((0, 0, 0))
    return (host, nick_box.text, ip_box.text)