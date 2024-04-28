import pygame
from random import randint

from scripts.settings import *


class Trash(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            newPath("assets/img/trash/trash" + str(randint(1, 3)) + ".png")).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.rect.x = randint(xBorder*2, WIDTH-xBorder*2)
        self.rect.y = randint(HEIGHT/2, HEIGHT-yBorder*2)

        self.dirty = 1
        self.visible = 1
