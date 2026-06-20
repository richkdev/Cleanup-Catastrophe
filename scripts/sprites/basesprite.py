import pygame
import random

from scripts import common, utils
from scripts.sprites.sheet import Sheet


class BaseSprite(pygame.sprite.DirtySprite):
    """
    Bare bones sprite class, don't use directly!
    """

    def __init__(self, *groups):
        super().__init__(*groups)

        self.dt: float = 0.0

        self.dirty = 2
        self.blendmode = pygame.BLENDMODE_NONE # check https://pyga.me/docs/ref/special_flags_list.html
        self.visible = 1
        self.layer = 0

        self.image: pygame.Surface
        self.old_image: pygame.Surface

        self.sheet: Sheet
        self.has_sheet: bool
        self.animated: bool

        self.rect: pygame.FRect
        self.source_rect: pygame.Rect

        self.size: pygame.typing.IntPoint = (1, 1)

        self.pos: pygame.Vector2 = pygame.Vector2()
        self.old_pos: pygame.Vector2 = pygame.Vector2()

        self.velocity: pygame.Vector2 = pygame.Vector2()
        self.acceleration: pygame.Vector2 = pygame.Vector2()
        self.max_velocity: pygame.Vector2 = pygame.Vector2()

    def update(self, dt: float):
        super().update()

        self.dt = dt

        self.move()

        self.velocity.x = pygame.math.clamp(self.velocity.x, -self.max_velocity.x, self.max_velocity.x) if self.max_velocity.y != 0 else self.velocity.x
        self.velocity.y = pygame.math.clamp(self.velocity.y, -self.max_velocity.x, self.max_velocity.y) if self.max_velocity.y != 0 else self.velocity.y

        self.rect.x += self.velocity.x * self.dt
        self.rect.y += self.velocity.y * self.dt

        self.pos.x, self.pos.y = self.rect.x, self.rect.y

        if self.visible:
            self.animate()

    def animate(self):
        """modifiable"""

        if self.has_sheet and self.animated:
            self.image = self.sheet.draw(flip_x=False, flip_y=False)
            self.sheet.update()

    def move(self):
        """modifiable"""

        self.velocity += self.acceleration

    def move_to(self, pos: pygame.typing.Point):
        if pos != (self.pos.x, self.pos.y):
            self.pos.x, self.pos.y = pos[0], pos[1]
            self.rect.x, self.rect.y = self.pos

            # print(f"Moved {type(self).__name__} to {pos}")

    def move_ip(self, pos: pygame.typing.Point):
        if pos != (0, 0):
            self.pos += pos
            self.rect.x, self.rect.y = self.pos

            # print(f"Moved {type(self).__name__} in place by {pos}")

    def shake(self, seed: pygame.typing.Point):
        self.rect.x, self.rect.y = self.old_pos.x + random.uniform(0, seed[0]), self.old_pos.y + random.uniform(0, seed[1])


class RSprite(BaseSprite):
    """
    Custom sprite class with added utilities
    """

    def __init__(
        self,
        static_image_path: pygame.typing._PathLike | None = common.TEMPLATE_IMAGE_PATH,
        sheet_path: pygame.typing._PathLike | None = None,
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups: pygame.sprite.Group["RSprite"]
    ):
        super().__init__(*groups)

        self.pos = pygame.Vector2(pos)
        self.old_pos = self.pos.copy()
        self.size = size
        self.has_sheet = sheet_path != None
        self.animated = False

        if self.has_sheet:
            self.set_spritesheet(utils.newPath(str(sheet_path)))
        else:
            if static_image_path != None:
                self.set_image_path(utils.newPath(str(static_image_path)))

        self.old_image = self.image.copy()

        self.rect: pygame.FRect = pygame.FRect(self.pos, self.size)

        self.source_rect: pygame.Rect = self.image.get_rect()

        # self.mask = pygame.mask.from_surface(self.image) # maybe??

        self.callibrate()
        self.move_to(self.pos)

        print(f"Loaded {type(self).__name__} sprite, at {self.pos}, with size {self.size}")

    def callibrate(self):
        """
        callibrate the sprite for every time the `image` is modified.
        changes `old_image` &`source_rect`.
        does not change `pos`.
        """

        self.old_image = self.image.copy()
        self.source_rect = self.old_image.get_rect()

    def set_image_surf(self, image: pygame.Surface):
        """
        set the image to a static surface.
        """

        self.image = image.copy()

    def set_image_path(self, image_path: pygame.typing._PathLike):
        """
        set the image to a static image from a path.
        """

        self.image_path = utils.newPath(str(image_path))
        self.image = common.ASSET_DICT.get(self.image_path, pygame.image.load(self.image_path).convert_alpha())

    def set_spritesheet(self, path: pygame.typing._PathLike) -> None:
        """
        set the sprite's spritesheet to one from a path.
        """

        self.sheet = utils.cut_sheet(path)
        self.set_image_surf(self.sheet.states[self.sheet.current_state][0])


class RGroup[_RSprite: (RSprite | RGroup)](pygame.sprite.LayeredDirty[_RSprite]):
    """
    Custom sprite group with added utilities.
    """

    def __init__(self, *sprites: "_RSprite | RGroup[_RSprite]", pos: pygame.typing.Point | None = None):
        super().__init__(*sprites)

        self.pos = pygame.Vector2(pos if pos != None else (0, 0))

        for spr in self.sprites():
            if self.pos.x > spr.pos.x:
                self.pos.x = spr.pos.x
            if self.pos.y > spr.pos.y:
                self.pos.y = spr.pos.y

        print(f"Loaded {type(self).__name__} sprite group, at {self.pos}, with {len(self.sprites())} starting sprites")

    def update(self, dt: float):
        for sprite in self.sprites():
            sprite.update(dt)

    def move_to(self, pos: pygame.typing.Point):
        self.pos.x, self.pos.y = pos
        for sprite in self.sprites():
            sprite.move_to(pos)

    def move_ip(self, pos_ip: pygame.typing.Point):
        self.pos += pos_ip
        for sprite in self.sprites():
            sprite.move_ip(pos_ip)

    def shake(self, seed: pygame.typing.Point):
        for sprite in self.sprites():
            sprite.shake(seed)
