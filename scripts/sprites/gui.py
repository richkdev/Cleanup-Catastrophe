import pygame

from scripts import globals

from scripts.sprites.basesprite import *

class Text(RSprite):
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
        align: int = pygame.FONT_CENTER
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

    def animate(self):
        pass
