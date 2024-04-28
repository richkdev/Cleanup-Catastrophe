import pygame
from math import sin

from scripts.settings import *


class Background(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            "assets/img/background/bg.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0

        self.dirty = 1
        self.visible = 1
        self.layer = 1


class Islands(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            "assets/img/background/islands.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH-self.rect.width)/2
        self.rect.y = WIDTH/5

        self.dirty = 1
        self.visible = 1

        self.velocity = WIDTH/5


class MenuLogo(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            "assets/img/menu/logo.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width()/3, self.image.get_height()/3))

        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH-self.rect.width)/2
        self.rect.y = HEIGHT/10

        self.dirty = 1
        self.visible = 1

    def update(self):
        self.rect.y = (sin(pygame.time.get_ticks()/2 %
                       HEIGHT/50)*10) + HEIGHT/10
