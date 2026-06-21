import pygame
import numpy
import random

from scripts import common, utils
from scripts.sprites.basesprite import *
from scripts.sprites.sheet import *
from scripts.sprites.gui import *
from scripts.filehandling import *


class WorldObject(RSprite):
    """
    Sprite class for interactable and/or collidable objects
    """

    def set_worldobj(self, desc: str = "lipsum", interactable: bool = False, collidable: bool = False):
        self.interactable = interactable
        self.collidable = collidable
        self.desc = desc


class Player(RSprite):
    def __init__(
        self,
        static_image_path: pygame.typing._PathLike | None = common.TEMPLATE_IMAGE_PATH,
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (24, 44),
        pos: pygame.typing.Point = (0, 0),
        *groups
    ):
        super().__init__(None, utils.newPath("assets/img/sprites/paul.json"), (24, 44), pos, *groups)

        self.jump_strength = common.GRAVITY*30
        self.acceleration.x, self.acceleration.y = 2.5, common.GRAVITY
        self.max_velocity.x = 300

        self.is_colliding: bool = False
        self.is_grounded: bool = False

    def set_collidables(self, collideables: RGroup[WorldObject]):
        self.collideables = collideables

    def animate(self):
        self.image = self.sheet.draw(flip_x=bool(self.velocity.x < 0), flip_y=False)
        self.sheet.update(self.dt*5 if self.is_grounded else self.velocity.x/1000)

        if self.velocity.x != 0:
            self.sheet.set_animation("run")
        else:
            self.sheet.set_animation("idle")

    def jump(self):
        if self.is_grounded:
            self.is_grounded = False
            self.velocity.y = -self.jump_strength

    def collision(self, tiles: RGroup[WorldObject]) -> bool:
        # slightly modded ver of https://github.com/sloukit/pydew-valley-uzh/blob/main/src/sprites/entities/entity.py#L170

        colliding_rect = None

        for tile in tiles:
            if isinstance(tile, WorldObject) and tile.collidable and tile.rect.colliderect(self.rect):
                colliding_rect = tile.rect
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

                self.is_grounded = shortest_distance == distances[2]

                self.pos.x, self.pos.y = self.rect.x, self.rect.y

        return bool(colliding_rect)

    def move(self):
        self.is_colliding = self.collision(self.collideables)
        self.velocity.y += self.acceleration.y if not self.is_grounded else -self.velocity.y


class Rod(RSprite):
    def __init__(
        self,
        static_image_path: pygame.typing._PathLike | None = common.TEMPLATE_IMAGE_PATH,
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups
    ):
        super().__init__(None, utils.newPath("assets/img/sprites/fishrod.json"), (11, 14), pos, *groups)

        self.is_fishing: bool = False
        self.durability: int = 20


class Trash(RSprite):
    def __init__(
        self,
        image_path: pygame.typing._PathLike | None = None,
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups
    ):
        super().__init__(None, utils.newPath("assets/img/sprites/trash.json"), (1, 1), pos, *groups)

        self.set_trash()

    def set_trash(self, trash_type: TrashType = TrashType.TRASH_BAG, trash_id: pygame.typing.IntPoint = (0, 0), offset: int = 5) -> None:
        self.trash_id = trash_id
        self.trash_type = trash_type
        self.is_explosive = self.trash_type == TrashType.BOMB
        self.animated = False

        if not self.is_explosive:
            self.image = self.sheet.states["trash"][int(self.trash_type)-1]
        else:
            self.image = self.sheet.states["bomb"][random.randint(0, 1)]

        self.rect = self.image.get_frect()
        self.size = self.image.size

        self.callibrate()

        self.move_ip((
            random.uniform(-offset, offset),
            random.uniform(-offset, offset)
        ))


class MenuLogo(RSprite):
    def __init__(
        self,
        static_image_path: pygame.typing._PathLike | None = common.TEMPLATE_IMAGE_PATH,
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (234, 73),
        pos: pygame.typing.Point = (0, 0),
        *groups
    ):
        super().__init__(utils.newPath("assets/img/ui/logo.png"), None, (234, 73), pos, *groups)

        self.image = pygame.transform.smoothscale_by(self.image, 0.3)

        self.callibrate()

    def move(self):
        super().move()

        self.velocity.y = numpy.cos(pygame.time.get_ticks() / 100) * 25


class BackgroundLayer(RSprite):
    def __init__(
        self,
        static_image_path: pygame.typing._PathLike | None = utils.newPath("assets/img/bg/sky.png"),
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups
    ):
        super().__init__(static_image_path, None, (common.SCREEN_WIDTH, common.SCREEN_HEIGHT), pos, *groups)

        self.old_image = utils.multiply_image(self.old_image, self.old_image.size, self.size)
        self.set_image_surf(self.old_image)

        self.callibrate()

        self.size = self.image.size


class ParallaxBackground(RGroup[BackgroundLayer]):
    def move_parallax(self, pos: pygame.typing.Point, offset: float):
        for obj in self.sprites():
            obj.move_ip((pos[0]/-(obj.layer+1+offset), pos[1]/-(obj.layer+1+offset)))
