import pygame
import typing

from scripts import globals
from scripts.sprites.basesprite import *
from scripts.sprites.basesprite import RGroup, RSprite


class GUISprite(RSprite):
    """
    Base class for GUI sprites.
    """


class GUIGroup(RGroup[GUISprite]):
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
        font: pygame.Font = globals.bigFont,
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

        self.image = self.font.render(self.text, antialiased, self.color, self.bg_color, self.wrap_length)
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_frect()


class Button(Text):
    def set_button(
        self,
        command: typing.Callable[[], None] = lambda: print("click!")
    ):
        self.command = command

    def click(
        self
    ):
        self.command()
