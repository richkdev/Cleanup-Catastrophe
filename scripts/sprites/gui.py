import pygame
import typing

from scripts import globals
from scripts.sprites.basesprite import *
from scripts.sprites.basesprite import RGroup, RSprite


class GUISprite(RSprite):
    """
    Base class for GUI sprites.
    """

_GUISprite = typing.TypeVar("_GUISprite", bound=GUISprite)


class GUIGroup(RGroup[_GUISprite]):
    """
    Base class for GUI sprite groups
    """


class Text(GUISprite):
    """
    Sprite class for displaying text on screen.
    """

    def set_text(
        self,
        text: str = "lorem ipsum dolor sit amet",
        font: pygame.Font | None = globals.bigFont,
        color: pygame.typing.ColorLike = globals.BLACK,
        antialiased: bool = True,
        bg_color: pygame.typing.ColorLike | None = None,
        wrap_length: int = 0,
        # linesize: int = 18,
        align: int = pygame.FONT_LEFT
    ):
        if font != None:
            self.font = font

        self.text = text
        self.antialiased = antialiased
        self.color = color
        self.bg_color = bg_color
        self.wrap_length = wrap_length

        # self.font.set_linesize(linesize)
        self.font.align = align

        self.image = self.font.render(self.text, self.antialiased, self.color, self.bg_color, self.wrap_length).convert_alpha()

        self.callibrate()


class Button(Text):
    def set_button(
        self,
        command: typing.Callable[[], None] = lambda: print("click!")
    ):
        self.command = command
        self.is_hovered: bool = False

        self.callibrate()

    def click(self):
        self.command()

    def animate(self):
        if self.is_hovered:
            self.image.fill(globals.BLUE, special_flags=pygame.BLEND_ADD)
        else:
            self.image = self.old_image.copy()


class ButtonGroup(GUIGroup[Button]):
    def __init__(self, *sprites: Button | RGroup[Button]):
        super().__init__(*sprites)

        self.cursor: int = 0

    def move_cursor(self, val: int):
        self.cursor = val % len(self.sprites())

    def move_cursor_ip(self, val: int):
        self.move_cursor(self.cursor + val)

    def get_button_at_cursor(self) -> Button:
        return self.sprites()[self.cursor]

    def click_button_at_cursor(self):
        self.get_button_at_cursor().click()
