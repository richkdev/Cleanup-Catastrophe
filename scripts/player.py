import pygame

from scripts.settings import *


class Player(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            newPath("assets/img/user/player.png")).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/5
        self.rect.y = HEIGHT/5

        self.dirty = 1
        self.visible = 1

        self.velocity = WIDTH/5


class FishRod(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(
            newPath("assets/img/user/fishrod.png")).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH-self.rect.width)/2
        self.rect.y = 0

        self.dirty = 0
        self.visible = 0

        self.velocity = WIDTH/5
        self.isFishing = False
