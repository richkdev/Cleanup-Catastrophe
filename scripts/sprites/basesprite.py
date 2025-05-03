import pygame
import numpy

from random import randint

from scripts import globals, utils

from scripts.sprites.sheet import Sheet, cutSheet


class Sprite(pygame.sprite.DirtySprite):
    """
    Sprite class with a `DirtySprite` base
    """

    def __init__(self, sheetEnabled: bool, imagepath: str, size: pygame.Vector2):
        pygame.sprite.DirtySprite.__init__(self)

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
                self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))

        self.image_rect: pygame.FRect = self.image.get_frect()
        self.rect: pygame.FRect = pygame.FRect(0, 0, *size) # must be specified when init
        # self.mask = pygame.mask.from_surface(self.image) # maybe??

        self.old_x: int
        self.old_y: int
        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.top_speed = pygame.Vector2()

        print(f"Loaded {type(self).__name__} sprite, at ({self.rect.x}, {self.rect.y})")

    def update(self, key: pygame.key.ScancodeWrapper, dt: int):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=False, flip_y=False)
            self.sheet.update()

        self.displace()

    def displace(self):
        self.velocity += self.acceleration

        self.rect.x += self.velocity.x * self.dt
        self.rect.y += self.velocity.y * self.dt


class WorldObject(Sprite):
    """
    Sprite class for interactable and/or collidable objects in the `Lobby` state.
    """

    def __init__(
            self,
            imagepath: str,
            coords: pygame.Vector2 = pygame.Vector2(0, 0),
            size: pygame.Vector2 = pygame.Vector2(0, 0),
            desc: str = "lipsum",
            interactable: bool = False,
            collidable: bool = False
        ):
        super().__init__(False, imagepath, size)

        self.rect = self.image.get_frect()
        self.rect.x, self.rect.y = coords

        self.interactable = interactable
        self.collidable = collidable
        self.desc = desc


class Text(pygame.sprite.DirtySprite):
    """
    Sprite class for displaying text on screen.
    """

    def __init__(self, text: str = "", font: pygame.font.Font = globals.bigFont, color: pygame.typing.ColorLike = globals.BLACK, coords: pygame.typing.Point = (0, 0)):
        pygame.sprite.DirtySprite.__init__(self)

        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, False, self.color, None)

        self.rect: pygame.FRect = self.image.get_frect()
        self.old_x, self.old_y = coords[0], coords[1]
        self.rect.x, self.rect.y = self.old_x, self.old_y

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.image = self.font.render(self.text, False, self.color, None)

    def displace(self, coords: pygame.Vector2):
        self.rect.x, self.rect.y = coords.x, coords.y

    def shake(self, seedX: int, seedY: int):
        self.rect.x, self.rect.y = self.old_x + randint(0, seedX), self.old_y + randint(0, seedY)


def drawText(text: str, color: pygame.typing.ColorLike, font: pygame.font.Font, screen: pygame.Surface = pygame.Surface(globals.SCREEN_SIZE), lineSpacing: int = -2, pos: tuple = (0, 0)):
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

            newText = Text(text=paragraph[:i], font=font, color=color, coords=pygame.Vector2(rect.left, y))
            y += fontHeight + lineSpacing

            paragraph = paragraph[i:]
            textGroup.add(newText)

        y += fontHeight + lineSpacing

    return textGroup


def resizeImage(input_image: pygame.Surface, tile_size: tuple[int, int], target_size: tuple[int, int]):
    pattern = numpy.zeros((int(target_size[1]), int(target_size[0]), 3), dtype=numpy.uint8)

    for y in range(int(tile_size[1])):
        for x in range(int(tile_size[0])):
            pattern[x, y] = input_image.get_at((x % int(target_size[0]), y % int(target_size[1])))[:3]

    pattern_image = pygame.surfarray.make_surface(pattern)
    output_image = pygame.Surface(target_size)

    for y in range(0, int(target_size[1]), int(tile_size[1])):
        for x in range(0, int(target_size[0]), int(tile_size[0])):
            output_image.blit(pattern_image, (x, y))

    return output_image
