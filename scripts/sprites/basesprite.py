import pygame
from random import randint

from scripts.settings import *

class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, imagepath):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(newPath(imagepath)).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface(setcolor=TRANSPARENT)

        self.velocity = 0

        self.visible = 1
        self.dirty = 1
        self._layer = 1

        print(f"Loaded {type(self).__name__} sprite")

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)
        
        self.key = key
        self.dt = dt


class Text(pygame.sprite.DirtySprite):
    def __init__(self, text: str = "lorem ipsum", font: pygame.font.Font = bigFont, color: tuple[int, int, int, int] = WHITE, coords: tuple[int, int] = (0, 0)):
        super().__init__()

        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, False, self.color, None)

        self.rect = self.image.get_rect()
        self.old_x, self.old_y = coords[0], coords[1]
        self.rect.x, self.rect.y = self.old_x, self.old_y

    def update(self, key, dt):
        self.image = self.font.render(self.text, False, self.color, None)

    def displace(self, coords: tuple[int, int] = (0, 0)):
        self.rect.x, self.rect.y = coords[0], coords[1]

    def shake(self, seed: int = 2):
        self.rect.x, self.rect.y = self.old_x + randint(1, seed), self.old_y + randint(1, seed)


def drawText(text: str, color: tuple[int, int, int, int], font: pygame.font.Font, screen: pygame.surface.Surface, lineSpacing: int = -2): # modified version of https://www.pygame.org/wiki/TextWrap
    rect = screen.get_rect()
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
