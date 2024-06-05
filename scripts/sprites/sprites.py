import pygame
from random import randint

from scripts.settings import *
from scripts.sprites.basesprite import Sprite, Text, drawText


class Player(Sprite):
    def __init__(self):
        super().__init__("assets/img/sprites/player.png")

        self.rect.x, self.rect.y = WIDTH/5, HEIGHT/3

        self.velocity = WIDTH/4


class Rod(Sprite):
    def __init__(self):
        super().__init__("assets/img/sprites/fishrod.png")

        self.rect.x, self.rect.y = -10, -10

        self.velocity = WIDTH/4

        self.isFishing = False


class Trash(Sprite):
    def __init__(self, type: int = 0, coords: tuple[int, int] = (0, 0)):
        self.trashType = ['trash1', 'trash2', 'trash3', 'bomb'][type]

        super().__init__(f"assets/img/trash/{self.trashType}.png")

        self.rect.x, self.rect.y = coords[0] + randint(xBorder, xBorder*3), coords[1] + randint(yBorder, yBorder*3)

        self.explosive = 'bomb' in self.trashType


class MenuLogo(Sprite):
    def __init__(self):
        super().__init__("assets/img/ui/logo-small.png")

        self.old_image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.image = self.old_image

        self.rect = self.image.get_rect()
        
        self.old_x = (WIDTH-self.rect.width)/2
        self.old_y = (HEIGHT-self.rect.height)/2

        self.rect.x = self.old_x
        self.rect.y = self.old_y


class Background(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(
            "assets/img/bg/ocean.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Islands(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(
            "assets/img/bg/islands.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH-self.rect.width)/2
        self.rect.y = 60

        self.velocity = WIDTH/10
