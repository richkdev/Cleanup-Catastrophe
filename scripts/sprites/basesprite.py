import pygame

from random import randint

from scripts import common, utils
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
        self.image_path: pygame.typing._PathLike
        self.image: pygame.Surface
        self.old_image: pygame.Surface

        self.sheet: Sheet
        self.action: str = "idle"

        self.rect: pygame.FRect
        self.source_rect: pygame.Rect

        self.size: pygame.typing.IntPoint = (1, 1)

        self.pos: pygame.Vector2 = pygame.Vector2()
        self.old_pos: pygame.Vector2 = pygame.Vector2()

        self.velocity: pygame.Vector2 = pygame.Vector2()
        self.acceleration: pygame.Vector2 = pygame.Vector2()
        self.max_velocity: pygame.Vector2 = pygame.Vector2()

    def update(self, dt: float):
        super().update(self)

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
        self.pos.x, self.pos.y = pos[0], pos[1]
        self.rect.x, self.rect.y = self.pos

        print(f"Moved {type(self).__name__} to {pos}")

    def move_ip(self, pos: pygame.typing.Point):
        self.pos += pos
        self.rect.x, self.rect.y = self.pos

        print(f"Moved {type(self).__name__} in place by {pos}")

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
        image_path: pygame.typing._PathLike = common.TEMPLATE_IMAGE_PATH,
        # image_src: pygame.Surface = globals.TEMPLATE_IMAGE_SURF, # TODO: make this work so that we dont have to load it images every single time and it can receive json spritesheet stuff as well
        size: pygame.typing.IntPoint = (1, 1),
        pos: pygame.typing.Point = (0, 0),
        *groups: pygame.sprite.Group["RSprite"]
    ) -> None:
        super().__init__(*groups)

        self.sheetEnabled = sheetEnabled
        self.sheetStatic = sheetStatic
        self.pos = pygame.Vector2(pos)
        self.old_pos = self.pos.copy()
        self.size = size
        self.image_path = utils.newPath(str(image_path))

        match self.sheetEnabled:
            case True:
                self.sheet = Sheet()
                self.action = "idle"
                self.sheet.add_animation(self.action, cut_sheet_fixed_size(self.image_path, self.size))
                self.sheet.set_animation(self.action)
                self.image = self.sheet.states[self.action][0]
            case False:
                self.set_image(self.image_path)

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

    def set_image(self, image_path: pygame.typing._PathLike = common.TEMPLATE_IMAGE_PATH) -> None:
        """
        set the image to a static surf.
        changes `image_path`, `image`.
        does not change `old_image`.
        does not callibrate the sprite.
        """

        self.image_path = utils.newPath(str(image_path))
        self.image = common.ASSET_DICT.get(self.image_path, pygame.image.load(self.image_path).convert_alpha())


class RGroup[_RSprite: RSprite](pygame.sprite.Group[_RSprite]):
    """
    Custom sprite group with added utilities.
    """

    def __init__(self, *sprites: "_RSprite | RGroup[_RSprite]", pos: pygame.typing.Point | None = None):
        super().__init__(*sprites)

        self.pos = pygame.Vector2(pos if pos != None else (0, 0))

        if pos != None:
            self.move_to(self.pos)

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
