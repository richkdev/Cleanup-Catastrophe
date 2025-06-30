import pygame
import typing

from random import randint

from scripts import globals, utils

from scripts.sprites.sheet import Sheet, cutSheet


class Sprite(pygame.sprite.DirtySprite):
    """
    Sprite class with a `DirtySprite` base
    """

    def __init__(self, sheetEnabled: bool, imagepath: str, size: pygame.typing.IntPoint, pos: pygame.typing.Point = (0, 0)):
        super().__init__() # i really should fix things up in this base class

        self.sheetEnabled = sheetEnabled
        self.image: pygame.Surface

        match self.sheetEnabled:
            case True:
                self.sheet = Sheet()
                self.sheet.add_animation("idle", cutSheet(imagepath, size))
                self.action = "idle"
                self.sheet.set_action(self.action)
                self.image = self.sheet.states["idle"][0]
            case False:
                self.image = pygame.image.load(utils.newPath(imagepath)).convert_alpha()

        self.image_rect: pygame.Rect = self.image.get_rect()
        self.image_size = self.image.size

        self.rect: pygame.FRect = pygame.FRect(0, 0, *size) # set frect size to a custom hitbox size later, needs major refactor so that each child takes a pos param with pygame.typing.Point type

        # self.mask = pygame.mask.from_surface(self.image) # maybe??

        self.old_pos = pygame.Vector2(self.rect.x, self.rect.y)

        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.top_speed = pygame.Vector2()

        print(f"Loaded {type(self).__name__} sprite, at ({self.rect.x}, {self.rect.y})")

    def update(self, key: pygame.key.ScancodeWrapper, dt: float):
        super().update()

        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=False, flip_y=False)
            self.sheet.update()

        self.move()

    def move(self):
        self.velocity += self.acceleration

        self.rect.x += self.velocity.x * self.dt
        self.rect.y += self.velocity.y * self.dt

    def displace(self, pos: pygame.typing.Point):
        self.rect.x, self.rect.y = pos[0], pos[1]

    def shake(self, seedX: int, seedY: int):
        self.rect.x, self.rect.y = self.old_pos.x + randint(0, seedX), self.old_pos.y + randint(0, seedY)

class SpriteGroup(pygame.sprite.Group):
    def sprites(self) -> list[Sprite]:
        return super().sprites()

    def displace(self, pos: pygame.typing.Point):
        for sprite in self.sprites():
            sprite.rect.x += pos[0]
            sprite.rect.y += pos[1]

class WorldObject(Sprite):
    """
    Sprite class for interactable and/or collidable objects
    """

    def __init__(
            self,
            imagepath: str,
            coords: pygame.typing.Point = pygame.Vector2(),
            size: pygame.typing.IntPoint = (1, 1),
            desc: str = "lipsum",
            interactable: bool = False,
            collidable: bool = False
        ):
        super().__init__(False, imagepath, size)

        self.image_rect.size = size
        self.rect = pygame.FRect(*self.image_rect.topleft, *size)
        self.rect.x, self.rect.y = coords

        self.interactable = interactable
        self.collidable = collidable
        self.desc = desc


class Text(Sprite):
    """
    Sprite class for displaying text on screen.
    """

    def __init__(
        self, text: str = "",
        font: pygame.font.Font = globals.bigFont,
        color: pygame.typing.ColorLike = globals.BLACK,
        pos: pygame.typing.Point = (0, 0)
    ):
        super().__init__(False, utils.newPath("assets/img/sprites/trash.png"), (0, 0))
        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, False, self.color, None)

        self.rect: pygame.FRect = self.image.get_frect()

        self.old_pos = pygame.Vector2(pos)
        self.rect.x, self.rect.y = pos

    def update(self, key, dt):
        self.key = key
        self.dt = dt

        self.image = self.font.render(self.text, False, self.color, None)

        self.move()


def drawText(
        text: str,
        color: pygame.typing.ColorLike,
        font: pygame.font.Font,
        screen: pygame.Surface = pygame.Surface(globals.SCREEN_SIZE),
        lineSpacing: int = -2,
        pos: pygame.typing.Point = (0, 0)
    ) -> pygame.sprite.Group:
    """
    Modified version of https://www.pygame.org/wiki/TextWrap.
    """

    pos = (pos[0] + screen.get_width() / 2, pos[1] + screen.get_height() / 2)
    rect = screen.get_rect(center=pos)
    textGroup = pygame.sprite.Group()

    y = rect.top

    fontHeight = font.size("Tg")[1]

    paragraphs = text.split('\n')  # Split text by newline characters first
    for paragraph in paragraphs:
        while paragraph:
            i = 1

            if y + fontHeight > rect.bottom:
                break

            while font.size(paragraph[:i])[0] < rect.width and i < len(paragraph):
                i += 1

            # If we've reached the end of the text, break out of the loop
            if not i == len(paragraph):
                # Find the last space in the current substring
                i = paragraph.rfind(" ", 0, i) + 1

            newText = Text(text=paragraph[:i], font=font, color=color, pos=pygame.Vector2(rect.left, y))
            y += fontHeight + lineSpacing

            paragraph = paragraph[i:]
            textGroup.add(newText)

        y += fontHeight + lineSpacing

    return textGroup


def resizeImage(input_image: pygame.Surface, tile_size: pygame.typing.Point, target_size: pygame.typing.Point):
    output_image = pygame.Surface(target_size, pygame.SRCALPHA)

    for y in range(0, int(target_size[1]), int(tile_size[1])):
        for x in range(0, int(target_size[0]), int(tile_size[0])):
            output_image.blit(input_image, (x, y))

    return output_image
