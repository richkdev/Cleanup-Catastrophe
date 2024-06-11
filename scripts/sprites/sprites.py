import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *
from scripts.sprites.basesprite import Sprite, Text, drawText
from scripts.sprites.sheet import cutSheet

from random import randint


class Player(Sprite):
    def __init__(self, pos=(WIDTH / 5, HEIGHT / 3)):
        super().__init__(True, newPath("assets/img/sprites/paul_idle.png"),
                         Vector2(24, 43))
        self.sheet.add_animation("run", cutSheet(newPath("assets/img/sprites/paul_run.png"),
                                 Vector2(31, 44)))

        self.rect.x, self.rect.y = pos

        self.velocity = 0
        self.acceleration = 10
        self.top_speed = 100

    def update(self, key, dt):
        super().update(key, dt)

        if self.key[K_LEFT] or self.key[K_RIGHT]:
            self.sheet.set_action("run")
        else:
            self.sheet.set_action("idle")


class Rod(Sprite):
    def __init__(self):
        super().__init__(False, newPath("assets/img/sprites/fishrod.png"),
                         Vector2(9, 16))

        self.rect.x, self.rect.y = -10, -10

        self.velocity = WIDTH / 4

        self.isFishing = False
        self.durable = 20


class Trash(Sprite):
    def __init__(self, type: int = 0, coords: tuple[int, int] = (0, 0), offset: int = 8):
        self.trashType = ['trash1', 'trash2', 'trash3', 'bomb'][type]

        super().__init__(True, newPath(
            f"assets/img/trash/{self.trashType}.png"), Vector2(12, 13))

        self.rect.x, self.rect.y = int(
            coords[0] + randint(1, offset)), int(coords[1] + randint(1, offset))

        self.explosive = 'bomb' in self.trashType


class MenuLogo(Sprite):
    def __init__(self):
        super().__init__(False, newPath(f"assets/img/ui/logo-small.png"),
                         Vector2(234, 73))

        self.old_image = pygame.transform.scale(
            self.image, (self.image.get_width(), self.image.get_height()))

        self.image = self.old_image

        self.rect = self.image.get_frect()

        self.old_x = (WIDTH - self.rect.width) / 2
        self.old_y = (HEIGHT - self.rect.height) / 2

        self.rect.x = self.old_x
        self.rect.y = self.old_y


class Background(Sprite):
    def __init__(self):
        super().__init__(False, newPath("assets/img/bg/ocean.png"),
                         Vector2(300, 300))


class Islands(Sprite):
    def __init__(self):
        super().__init__(False, newPath("assets/img/bg/islands.png"),
                         Vector2(324, 87))

        self.rect.x = (WIDTH - self.rect.width) / 2
        self.rect.y = 60


class WorldObject(Sprite):
    def __init__(self, imagepath: str, coords: tuple[int, int], desc: str):
        super().__init__(False, imagepath, Vector2(34, 13))

        self.rect.x, self.rect.y = coords

        self.old_x = coords[0]
        self.desc = desc
