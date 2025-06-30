import pygame

from scripts import globals, utils
from scripts.sprites.basesprite import *
from scripts.sprites.sheet import cutSheet

import random
import math


class Player(Sprite):
    def __init__(self, pos: pygame.typing.Point, collideables: pygame.sprite.AbstractGroup):
        super().__init__(True, utils.newPath("assets/img/sprites/paul_idle.png"),
                         (24, 43))
        self.sheet.add_animation("run", cutSheet(utils.newPath("assets/img/sprites/paul_run.png"),
                                 (31, 44)))
        self.sheet.add_animation("fish", cutSheet(utils.newPath("assets/img/sprites/paul_boat.png"),
                                 (40, 42)))

        self.rect.x, self.rect.y = pos
        self.old_pos.x, self.old_pos.y = pos

        self.acceleration.y = globals.GRAVITY
        self.jump_strength = globals.GRAVITY*30

        self.is_colliding: bool = False
        self.grounded: bool = False
        self.collideables = collideables

    def update(self, key, dt):
        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=bool(self.velocity.x < 0), flip_y=False)
            self.sheet.update(self.dt*5 if self.grounded else abs(self.velocity.x)/1000)

        if self.velocity.x != 0:
            self.sheet.set_action("run")
        else:
            self.sheet.set_action("idle")

        self.move()

    def jump(self):
        if self.grounded:
            self.grounded = False
            self.velocity.y = -self.jump_strength

    def collision(self, tiles: pygame.sprite.AbstractGroup):
        # slightly modded ver of https://github.com/sloukit/pydew-valley-uzh/blob/main/src/sprites/entities/entity.py#L170

        colliding_rect = None

        for tile in tiles:
            if isinstance(tile, WorldObject) and tile.collidable and tile.rect.colliderect(self.rect):
                colliding_rect = tile.rect
                distances_rect = colliding_rect

                distances_rect = tile.rect

                distances = (
                    abs(self.rect.right - distances_rect.left),
                    abs(self.rect.left - distances_rect.right),
                    abs(self.rect.bottom - distances_rect.top),
                    abs(self.rect.top - distances_rect.bottom),
                )

                shortest_distance = min(distances)
                if shortest_distance == distances[0]:
                    self.rect.right = colliding_rect.left

                if shortest_distance == distances[1]:
                    self.rect.left = colliding_rect.right

                if shortest_distance == distances[2]:
                    self.rect.bottom = colliding_rect.top
                    self.grounded = True
                else:
                    self.grounded = False

                if shortest_distance == distances[3]:
                    self.rect.top = colliding_rect.bottom

        return bool(colliding_rect)

    def move(self):
        super().move()

        self.velocity.x = 0

        if self.grounded:
            self.velocity.y = 0

        self.is_colliding = self.collision(self.collideables)


class Rod(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath("assets/img/sprites/fishrod.png"),
                         (9, 16))

        self.rect.x, self.rect.y = -10, -10

        self.isFishing = False
        self.durability = 20


class Trash(Sprite):
    def __init__(self, trashType: int = 1, coords: pygame.typing.Point = (0, 0), offset: int = 0):
        super().__init__(True, utils.newPath(f"assets/img/sprites/trash.png"), (12, 13))

        self.image = self.sheet.states["idle"][trashType-1]

        self.old_pos = pygame.Vector2(self.rect.x, self.rect.y)

        self.rect.move_ip(coords[0] + random.randint(-offset, offset), coords[1] + random.randint(-offset, offset))

        self.explosive = trashType == 4

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt
        
        self.move()

        # might want to make it so that there's a bool to toggle for sprites with static images (from spritesheet and non-spritesheet surfaces)


class MenuLogo(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath(f"assets/img/ui/logo.png"),
                         (234, 73))

        self.image = pygame.transform.smoothscale_by(self.image, 0.3)
        self.rect = self.image.get_frect()

        self.old_pos.x = int(globals.SCREEN_WIDTH - self.rect.width)//2
        self.old_pos.y = int(globals.SCREEN_HEIGHT - self.rect.height)//2

        self.rect.x = self.old_pos.x
        self.rect.y = self.old_pos.y

        self.coeficient = 50

    def move(self):
        super().move()

        self.velocity.y = math.sin(pygame.time.get_ticks() / 2 / self.coeficient) * self.coeficient

class Background(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath("assets/img/bg/sky.png"), (int(globals.SCREEN_WIDTH*1.5), 300))

        self.image = resizeImage(self.image, (2, 300), (globals.SCREEN_WIDTH**1.5, 300))
