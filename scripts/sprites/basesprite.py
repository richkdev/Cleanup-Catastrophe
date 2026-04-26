import pygame
import typing

from random import randint

from scripts import globals, utils
from scripts.sprites.sheet import Sheet, cut_sheet_fixed_size


class BaseSprite(pygame.sprite.DirtySprite):
    """
    Bare bones sprite class, don't use directly!
    """

    def __init__(self, *groups):
        super().__init__(*groups)

        self.key: pygame.key.ScancodeWrapper
        self.dt: float = 0.0

        self.dirty = 1
        self.blendmode = pygame.BLENDMODE_NONE # check https://pyga.me/docs/ref/special_flags_list.html
        self.visible = 1

        self.sheetEnabled: bool
        self.sheetStatic: bool = False
        self.image_path: str
        self.image: pygame.Surface
        self.old_image: pygame.Surface

        self.sheet: Sheet
        self.action: str = "idle"

        self.image_rect: pygame.Rect
        self.image_size: pygame.typing.IntPoint

        self.size: pygame.typing.IntPoint = (1, 1)
        self.rect: pygame.FRect

        self.pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.old_pos: pygame.Vector2

        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.max_velocity = pygame.Vector2()

    def update(self, dt: float):
        pygame.sprite.DirtySprite.update(self)

        self.dt = dt

        self.move()

        self.rect.x += self.velocity.x * self.dt
        self.rect.y += self.velocity.y * self.dt

        if self.visible:
            self.animate()

    def animate(self):
        """modifiable"""

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=False, flip_y=False)

            if not self.sheetStatic:
                self.sheet.update()

    def move(self):
        """modifiable"""

        self.velocity += self.acceleration

    def move_to(self, pos: pygame.typing.Point):
        self.pos.x, self.pos.y = self.rect.x, self.rect.y = pos[0], pos[1]

    def move_ip(self, pos: pygame.typing.Point):
        self.rect.x += pos[0]
        self.rect.y += pos[1]
        self.pos.x, self.pos.y = self.rect.x, self.rect.y

    def shake(self, seed: pygame.typing.IntPoint):
        self.rect.x, self.rect.y = self.old_pos.x + randint(0, seed[0]), self.old_pos.y + randint(0, seed[1])


class RSprite(BaseSprite):
    """
    Custom sprite class with added utilities
    """

    def __init__(
        self,
        sheetEnabled: bool = False,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = globals.TEMPLATE_IMAGE_PATH,
        # image_src: pygame.Surface = globals.TEMPLATE_IMAGE_SURF, # TODO: make this work so that we dont have to load it images every single time and it can receive json spritesheet stuff as well
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups: pygame.sprite.Group["RSprite"]
    ) -> None:
        super().__init__(*groups)

        self.sheetEnabled = sheetEnabled
        self.sheetStatic = sheetStatic
        self.pos = pygame.Vector2(pos)

        match self.sheetEnabled:
            case True:
                self.sheet = Sheet()
                self.action = "idle"
                self.sheet.add_animation(self.action, cut_sheet_fixed_size(image_path, size))
                self.sheet.set_animation(self.action)
                self.image = self.sheet.states[self.action][0]
            case False:
                self.image = pygame.image.load(utils.newPath(str(image_path))).convert_alpha()

        self.old_image = self.image.copy()

        self.image_rect: pygame.Rect = self.image.get_rect()
        self.image_size = self.image.get_size()

        self.rect: pygame.FRect = pygame.FRect(pos, size) # TODO: set frect size to a custom hitbox size later, needs major refactor so that each child takes a pos param with pygame.typing.Point type

        # self.mask = pygame.mask.from_surface(self.image) # maybe??

        self.old_pos = self.pos.copy()

        self.callibrate()

        print(f"Loaded {type(self).__name__} sprite, at ({pos})")

    def add(self, *groups: pygame.sprite.Group["RSprite"]) -> None:
        return super().add(*groups)

    def callibrate(self):
        """callibrate the sprite for every time image data is modified"""

        self.old_image = self.image.copy()
        self.rect = self.old_image.get_frect()
        self.pos = self.rect.x, self.rect.y = self.old_pos
        self.image_rect = self.old_image.get_rect()
        self.image_size = self.image_rect.size

_RSprite = typing.TypeVar("_RSprite", bound=RSprite) # solution: https://sorokin.engineer/posts/en/python_type_aliasing.html


class RGroup(pygame.sprite.Group[_RSprite]):
    """
    Custom sprite group with added utilities.
    """

    def __init__(self, *sprites: "_RSprite | RGroup[_RSprite]") -> None:
        pygame.sprite.Group.__init__(self, *sprites)

    def add(
        self,
        *sprites: "_RSprite | RGroup",
        **kwargs: typing.Any
    ) -> None:
        return pygame.sprite.Group.add(self, *sprites, **kwargs)

    def update(self, dt: float) -> None:
        for sprite in self.sprites():
            sprite.update(dt)

    def sprites(self) -> list[_RSprite]:
        return pygame.sprite.Group.sprites(self)

    def move_ip(self, pos: pygame.typing.Point) -> None:
        for sprite in self.sprites():
            sprite.move_ip(pos)


class WorldObject(RSprite):
    """
    Sprite class for interactable and/or collidable objects
    """

    def __init__(
        self,
        sheetEnabled: bool = False,
        sheetStatic: bool = False,
        image_path: pygame.typing._PathLike = globals.TEMPLATE_IMAGE_PATH,
        # image_src: pygame.Surface = globals.TEMPLATE_IMAGE_SURF,
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0), # TODO: make this do something later!
        *groups: RGroup
    ):
        super().__init__(sheetEnabled, sheetStatic, image_path, size, pos, *groups)

        self.image_rect.size = size
        self.rect = pygame.FRect(*self.image_rect.topleft, *size)
        self.rect.x, self.rect.y = pos

        self.desc: str = "lipsum"
        self.interactable: bool = False
        self.collidable: bool

    def set_worldobj(self, desc: str, interactable: bool, collidable: bool):
        self.interactable = interactable
        self.collidable = collidable
        self.desc = desc
