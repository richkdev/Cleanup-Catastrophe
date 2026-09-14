import pygame
import enum

from scripts.sprites.basesprite import *

@enum.unique
class TrashType(enum.IntEnum):
    EMPTY = 0
    TRASH_BAG = 1
    SNACK_BAG = 2
    PLASTIC_BAG = 3
    BOMB = enum.auto()


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
            self.image = self.sheet.states["bomb"][common.RNG.integers(0, 1, dtype=int)]

        self.rect = self.image.get_frect()
        self.size = self.image.size

        self.callibrate()

        self.move_ip((
            common.RNG.uniform(-offset, offset),
            common.RNG.uniform(-offset, offset)
        ))
