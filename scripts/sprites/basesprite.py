import pygame
from random import randint

from scripts.settings import *

from scripts.sprites.sheet import Sheet, cutSheet


class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, sheetEnabled: bool, imagepath: str, size: Vector2 = Vector2(0, 0)):
        pygame.sprite.DirtySprite.__init__(self)

        self.sheetEnabled = sheetEnabled
        self.image: Surface
        if self.sheetEnabled:
            self.sheet = Sheet()
            self.sheet.add_animation("idle", cutSheet(imagepath, size))
            self.action = "idle"
            self.sheet.set_action(self.action)
            self.image = self.sheet.states["idle"][0]
        else:
            self.image = pygame.image.load(newPath(imagepath)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))

        self.rect: FRect = self.image.get_frect()

        self.velocity = 1
        self.acceleration = 0

        self.visible = 1
        self.dirty = 1
        self._layer = 1

        print(f"Loaded {type(self).__name__} sprite, at ({self.rect.x}, {self.rect.y})")

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=(self.velocity < 0), flip_y=False)
            self.sheet.update()


class Text(pygame.sprite.DirtySprite):
    def __init__(self, text: str = "lorem ipsum", font: pygame.font.Font = bigFont, color: tuple[int, int, int, int] = WHITE, coords: tuple[int, int] = (0, 0)):
        pygame.sprite.DirtySprite.__init__(self)

        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, False, self.color, None)

        self.rect: Rect = self.image.get_rect()
        self.old_x, self.old_y = coords[0], coords[1]
        self.rect.x, self.rect.y = self.old_x, self.old_y

    def update(self, key, dt):
        self.image = self.font.render(self.text, False, self.color, None)

    def displace(self, coords: tuple[int, int] = (0, 0)):
        self.rect.x, self.rect.y = coords[0], coords[1]

    def shake(self, seedX: int = 2, seedY: int = 2):
        self.rect.x, self.rect.y = self.old_x + randint(0, seedX), self.old_y + randint(0, seedY)


def drawText(text: str, color: tuple[int, int, int, int], font: pygame.font.Font, screen: Surface, lineSpacing: int = -2, pos: tuple = (0, 0)):  # modified version of https://www.pygame.org/wiki/TextWrap
    pos = (pos[0] + screen.get_width() / 2, pos[1] + screen.get_height() / 2)
    rect = screen.get_rect(center=pos)
    textGroup = pygame.sprite.Group()

    y = rect.top

    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        if y + fontHeight > rect.bottom:
            break

        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        newText = Text(text=text[:i], font=font, color=color, coords=(rect.left, y))
        y += fontHeight + lineSpacing

        text = text[i:]
        textGroup.add(newText)

    return textGroup
