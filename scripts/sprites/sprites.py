import pygame
from pygame.locals import *  # type: ignore

from scripts import globals, utils
from scripts.sprites.basesprite import Sprite, WorldObject, Text, drawText, resizeImage
from scripts.sprites.sheet import cutSheet

from random import randint


class Player(Sprite):
    def __init__(self, pos: tuple[int, int], collideables: pygame.sprite.Group):
        super().__init__(True, utils.newPath("assets/img/sprites/paul_idle.png"),
                         pygame.Vector2(24, 43))
        self.sheet.add_animation("run", cutSheet(utils.newPath("assets/img/sprites/paul_run.png"),
                                 pygame.Vector2(31, 44)))

        self.rect.x, self.rect.y = pos
        self.old_x, self.old_y = pos

        self.acceleration.y = globals.GRAVITY
        self.jump_strength = globals.GRAVITY*50

        self.stuck_left = False
        self.grounded = False
        self.collideables = collideables

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=bool(self.key[K_LEFT]), flip_y=False)
            self.sheet.update(0.15)

        if self.key[K_LEFT] or self.key[K_RIGHT]:
            self.sheet.set_action("run")
        else:
            self.sheet.set_action("idle")

        self.displace()

    def jump(self):
        if self.grounded:
            self.grounded = False
            self.velocity.y = -self.jump_strength
            print("did player jump?", bool(not self.grounded), self.velocity.y, self.acceleration.y)

    def collision_test(self, rect: pygame.Rect|pygame.FRect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def move(self, tiles: pygame.sprite.Group):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        
        hit_list = self.collision_test(self.rect, tiles)
        for tile in hit_list:
            if isinstance(tile, WorldObject) and tile.collidable:
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                    collision_types['right'] = True
                    self.velocity.x = 0

                if self.velocity.x < 0:
                    self.rect.left = tile.rect.right
                    collision_types['left'] = True
                    self.velocity.x = 0

        # hit_list = self.collision_test(self.rect, tiles)
        # for tile in hit_list:
        #     if isinstance(tile, WorldObject) and tile.collidable:
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    collision_types['bottom'] = True
                    self.velocity.y = 0

                if self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                    collision_types['top'] = True
                    self.velocity.y = 0

        return collision_types

    def displace(self):
        super().displace()

        self.velocity.x = 0

        self.collisions = self.move(self.collideables)

        if self.collisions['bottom']:
            self.grounded = True


class Rod(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath("assets/img/sprites/fishrod.png"),
                         pygame.Vector2(9, 16))

        self.rect.x, self.rect.y = -10, -10

        self.velocity.y = 80

        self.isFishing = False
        self.durability = 20


class Trash(Sprite):
    def __init__(self, trashType: int = 1, coords: pygame.typing.Point = (0, 0), offset: int = 8):
        super().__init__(True, utils.newPath(f"assets/img/sprites/trash.png"), pygame.Vector2(12, 13))

        self.image = self.sheet.states["idle"][trashType-1]

        self.rect.x, self.rect.y = int(
            coords[0] + randint(1, offset)), int(coords[1] + randint(1, offset))

        self.explosive = trashType == 4

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt
        
        self.displace()


class MenuLogo(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath(f"assets/img/ui/logo-small.png"),
                         pygame.Vector2(234, 73))

        # self.old_image = pygame.transform.scale(
        #     self.image, (self.image.get_width(), self.image.get_height()))

        # self.image = self.old_image

        # self.rect = self.image.get_frect()

        self.old_x = int(globals.SCREEN_WIDTH - self.rect.width)//2
        self.old_y = int(globals.SCREEN_HEIGHT - self.rect.height)//2

        self.rect.x = self.old_x
        self.rect.y = self.old_y


class Background(Sprite):
    def __init__(self):
        super().__init__(False, utils.newPath("assets/img/bg/sky.png"), pygame.Vector2((globals.SCREEN_WIDTH**1.5), 300))

        self.image = resizeImage(self.image, (2, 300), (globals.SCREEN_WIDTH**1.5, 300))
