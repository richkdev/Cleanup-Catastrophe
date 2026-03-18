import pygame
import random

from scripts import globals, utils
from scripts.sprites.basesprite import *
from scripts.sprites.sheet import *
from scripts.sprites.utils import *
from scripts.sprites.gui import *


class Player(RSprite):
    def __init__(
        self,
        sheetEnabled: bool = True,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = utils.newPath("assets/img/sprites/paul_idle.png"),
        size: pygame.typing.IntPoint = (24, 44),
        pos: pygame.typing.Point = (0, 0),
        *groups: RGroup,
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        # self.sheet = cut_sheet(
        #     utils.newPath("assets/img/sprites/jake.png"),
        #     utils.newPath("assets/img/sprites/jake.json")
        # )

        self.sheet.add_animation("run", cut_sheet_fixed_size(utils.newPath("assets/img/sprites/paul_run.png"),
                                 (31, 44)))
        self.sheet.add_animation("fish", cut_sheet_fixed_size(utils.newPath("assets/img/sprites/paul_boat.png"),
                                 (40, 42)))

        self.jump_strength = globals.GRAVITY*30
        self.acceleration.x, self.acceleration.y = 5, globals.GRAVITY
        self.max_velocity.x = 100

        self.is_colliding: bool = False
        self.grounded: bool = False

    def set_collidables(self, collideables: RGroup):
        self.collideables = collideables

    def animate(self):
        self.image = self.sheet.draw(flip_x=bool(self.velocity.x < 0), flip_y=False)
        self.sheet.update(self.dt*5 if self.grounded else self.velocity.length()/1000)

        if self.velocity.x != 0:
            self.sheet.set_animation("run")
        else:
            self.sheet.set_animation("idle")

    def jump(self):
        if self.grounded:
            self.grounded = False
            self.velocity.y = -self.jump_strength

    def collision(self, tiles: RGroup[WorldObject]):
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
        if self.grounded:
            self.velocity.y = 0
        else:
            self.velocity.y += self.acceleration.y

        self.is_colliding = self.collision(self.collideables)

class Rod(RSprite):
    def __init__(
        self,
        sheetEnabled: bool = True,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = utils.newPath("assets/img/sprites/fishrod.png"),
        size: pygame.typing.IntPoint = (9, 16),
        pos: pygame.typing.Point = (0, 0),
        *groups: RGroup,
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        self.is_fishing: bool = False
        self.durability: int = 20


class Trash(RSprite):
    def __init__(
        self,
        sheetEnabled: bool = True,
        sheetStatic: bool = True,
        image_path: pygame.typing._PathLike = utils.newPath(f"assets/img/sprites/trash.png"),
        size: pygame.typing.IntPoint = (12, 13),
        pos: pygame.typing.Point = (0, 0),
        *groups: RGroup
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        self.trash_id: pygame.typing.IntPoint
        self.trash_type: int
        self.is_explosive: bool

    def set_trash(self, trash_type: int = 1, trash_id: pygame.typing.IntPoint = (0, 0), offset: int = 5) -> None:
        self.trash_id = trash_id
        self.trash_type = trash_type
        self.is_explosive = self.trash_type == 4

        # self.image = globals.smallFont.render(f"{self.trash_type}", False, globals.BLACK, None) # for debug purposes
        self.image = self.sheet.states["idle"][trash_type-1]

        self.rect.move_ip(
            random.randint(-offset, offset),
            random.randint(-offset, offset)
        )

    def animate(self):
        pass


class MenuLogo(RSprite):
    def __init__(
        self,
        sheetEnabled: bool = False,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = utils.newPath(f"assets/img/ui/logo.png"),
        size: pygame.typing.IntPoint = (234, 73),
        pos: pygame.typing.Point = (0, 0),
        *groups: RGroup
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        self.image = pygame.transform.smoothscale_by(self.image, 0.3)
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_frect()

        self.rect.x, self.rect.y = self.pos

    def move(self):
        super().move()

        self.velocity.y = numpy.cos(pygame.time.get_ticks() / 100) * 25


class Background(RSprite):
    def __init__(
        self,
        sheetEnabled: bool = False,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = utils.newPath("assets/img/bg/sky.png"),
        size: pygame.typing.IntPoint = (int(globals.SCREEN_WIDTH*1.5), 300),
        pos: pygame.typing.Point = (0, 0),
        *groups: RGroup
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        self.old_image = self.image = multiply_image(self.image, (2, 300), (globals.SCREEN_WIDTH*2, 300))

        self.rect = self.image.get_frect()
        self.image_rect = self.image.get_rect()
