import pygame
import numpy

from random import randint

from scripts.settings import *

from scripts.sprites.sheet import Sheet, cutSheet


class Sprite(pygame.sprite.DirtySprite):
    """
    Sprite class with a `pygame.sprite.DirtySprite` base
    """

    def __init__(self, sheetEnabled: bool, imagepath: str, size: Vector2 = Vector2(0, 0)):
        pygame.sprite.DirtySprite.__init__(self)

        self.sheetEnabled = sheetEnabled
        self.image: Surface

        if self.sheetEnabled:
            self.sheet = Sheet()
            self.sheet.add_animation("idle", cutSheet(imagepath, size))
            self.action = "idle"
            self.sheet.set_action(self.action)
            self.image = self.sheet.states["idle"][0]
        else:
            self.image = pygame.image.load(newPath(imagepath)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))

        self.rect: FRect = self.image.get_frect()

        self.velocity = 0
        self.acceleration = 0

        self.visible = 1
        self.dirty = 1
        self._layer = 1

        print(f"Loaded {type(self).__name__} sprite, at ({self.rect.x}, {self.rect.y})")

    def update(self, key, dt):
        pygame.sprite.DirtySprite.update(self)

        self.key = key
        self.dt = dt

        if self.sheetEnabled:
            self.image = self.sheet.draw(flip_x=False, flip_y=False)
            self.sheet.update()


class WorldObject(Sprite):
    """
    Sprite class for objects in the `Lobby` state.
    """

    def __init__(self, imagepath: str, coords: tuple[int, int], desc: str, interactable: bool = False):
        super().__init__(False, imagepath, Vector2(34, 13))

        self.rect.x, self.rect.y = coords
        self.old_x = coords[0]

        self.interactable = interactable
        self.desc = desc


class TileSprite(Sprite):
    """
    Sprite class for mutliplying an image based on a given `target_size` and `tile_size`.    
    """

    def __init__(self, imagepath: str, coords: tuple[int, int], tile_size: Vector2, target_size: Vector2):
        super().__init__(False, imagepath, target_size)

        self.rect.x, self.rect.y = coords

        self.tile_size = tile_size
        self.target_size = target_size

    def update(self, key, dt):
        self.pattern = numpy.zeros((int(self.target_size.y), int(self.target_size.x), 3), dtype=numpy.uint8)

        for y in range(int(self.tile_size.y)):
            for x in range(int(self.tile_size.x)):
                self.pattern[x, y] = self.image.get_at((x % int(self.target_size.x), y % int(self.target_size.y)))[:3]

        self.pattern_image = pygame.surfarray.make_surface(self.pattern)
        self.image = Surface((int(self.target_size.x), int(self.target_size.y)))

        for y in range(0, int(self.target_size.y), int(self.tile_size.y)):
            for x in range(0, int(self.target_size.x), int(self.tile_size.x)):
                self.image.blit(self.pattern_image, (x, y))


class Text(pygame.sprite.DirtySprite):
    """
    Sprite class for displaying text on screen.
    """

    def __init__(self, text: str = "lorem ipsum", font: pygame.font.Font = bigFont, color = WHITE, coords = Vector2(0, 0)):
        pygame.sprite.DirtySprite.__init__(self)

        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(self.text, False, self.color, None)

        self.rect: Rect = self.image.get_rect()
        self.old_x, self.old_y = coords.x, coords.y
        self.rect.x, self.rect.y = self.old_x, self.old_y

    def update(self, key, dt):
        self.image = self.font.render(self.text, False, self.color, None)

    def displace(self, coords: Vector2):
        self.rect.x, self.rect.y = coords.x, coords.y

    def shake(self, seedX: int = 2, seedY: int = 2):
        self.rect.x, self.rect.y = self.old_x + randint(0, seedX), self.old_y + randint(0, seedY)


def drawText(text: str, color: Color, font: pygame.font.Font, screen: Surface, lineSpacing: int = -2, pos: tuple = (0, 0)):
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

            newText = Text(text=paragraph[:i], font=font, color=color, coords=Vector2(rect.left, y))
            y += fontHeight + lineSpacing

            paragraph = paragraph[i:]
            textGroup.add(newText)

        y += fontHeight + lineSpacing

    return textGroup
