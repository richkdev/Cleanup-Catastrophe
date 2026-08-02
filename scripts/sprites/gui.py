import pygame
import typing

from scripts import common, color
from scripts.sprites.basesprite import *
from scripts.sprites.basesprite import RGroup, RSprite


class GUISprite(RSprite):
    """
    Base class for GUI sprites.
    """


class GUIGroup[_GUISprite: GUISprite](RGroup[_GUISprite]):
    """
    Base class for GUI sprite groups.
    """


class RCursor(GUISprite):
    def set_cursor(
        self,
        sheet_path: pygame.typing._PathLike = utils.newPath("assets/img/ui/cursor.json"),
        command: typing.Callable[[], None] = lambda: print("click!")
    ):
        self.set_spritesheet(sheet_path)
        self.callibrate()
        self.command = command

    def click(self, anim: str = "click"):
        self.sheet.set_animation(anim)
        self.command()


class Text(GUISprite):
    """
    Sprite class for displaying text.
    """

    def set_text(
        self,
        text: str = "lipsum",
        font: pygame.Font = common.SMALL_FONT,
        color: pygame.typing.ColorLike = color.BLACK,
        bg_color: pygame.typing.ColorLike | None = None,
        antialiased: bool = False,
        wrap_length: int = 0,
        # linesize: int = 18,
        align: int = pygame.FONT_LEFT
    ):
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
        self.size = self.image.size


class Button(Text):
    """
    Sprite class for displaying a clickable button.
    """

    def set_button(
        self,
        command: typing.Callable[[], None] = lambda: print("click!")
    ):
        self.command = command
        self.is_hovered: bool = False

    def click(self):
        self.command()

    def animate(self):
        if self.is_hovered:
            self.image.fill(color.BLUE, special_flags=pygame.BLEND_ADD)
        else:
            if self.image._pixels_address != self.old_image._pixels_address:
                self.image = self.old_image.copy()


class ButtonGroup(GUIGroup[Button]):
    """
    Sprite group for `Button` sprites.
    """

    def __init__(self, *sprites: Button | RGroup[Button], pos: pygame.typing.Point | None = None):
        super().__init__(*sprites, pos=pos)

        self.cursor: int = 0

    def move_cursor(self, val: int):
        self.cursor = val % len(self.sprites())

    def move_cursor_ip(self, val: int):
        self.move_cursor(self.cursor + val)

    def get_button_at_cursor(self) -> Button:
        return self.sprites()[self.cursor]

    def click_button_at_cursor(self):
        self.get_button_at_cursor().click()


class ProgressBar(GUISprite):
    """
    Sprite class for displaying a progress bar.
    NOTE: progress bar size is set in init
    """

    def set_progress(
        self,
        progress: float = 50,
        max_progress: float = 100,
        horizontal: bool = True,
        color: pygame.typing.ColorLike = color.GREEN,
        bg_color: pygame.typing.ColorLike = color.WHITE
    ):
        self.image = pygame.Surface(self.size)

        self.callibrate()

        self.progress = progress
        self.max_progress = max_progress
        self.horizontal = horizontal
        self.color = color
        self.bg_color = bg_color

        self.image.fill(bg_color)

        if self.horizontal:
            self.image.fill(
                self.color,
                (0, 0, (self.progress / self.max_progress) * self.size[0], self.size[1]),
            )
        else:
            self.image.fill(
                self.color,
                (0, ((self.max_progress - self.progress) / self.max_progress) * self.size[1], self.size[0], (self.progress / self.max_progress) * self.size[1]),
            )


class Statistic(GUIGroup[Text | GUISprite]):
    """
    Sprite group for displaying text with an icon next to it, consists of a `GUISprite` & `Text`.
    inspired by `pygame.sprite.GroupSingle`.
    """

    def __init__(self, *sprites, pos: pygame.typing.Point | None = None):
        self.icon_sprite = GUISprite()
        self.text_sprite = Text()
        self.text_sprite.set_text()

        super().__init__(self.icon_sprite, self.text_sprite, pos=pos)

    def set_icon(
        self,
        image_path: pygame.typing._PathLike = common.TEMPLATE_IMAGE_PATH,
        pos_ip: pygame.typing.Point = (0, 0)
    ):
        if self.icon_sprite.image_path != image_path:
            self.icon_sprite.set_image_path(image_path)
        if pos_ip != (0, 0):
            self.icon_sprite.move_ip(pos_ip)

    def set_text(
        self,
        text: str = "lipsum",
        font: pygame.Font = common.SMALL_FONT,
        color: pygame.typing.ColorLike = color.BLACK,
        bg_color: pygame.typing.ColorLike | None = None,
        antialiased: bool = False,
        wrap_length: int = 0,
        align: int = pygame.FONT_LEFT,
        pos_ip: pygame.typing.Point = (0, 0)
    ):
        if (self.text_sprite.text != text) or (self.text_sprite.font != font) or (self.text_sprite.color != color) or (self.text_sprite.bg_color != bg_color) or (self.text_sprite.antialiased != antialiased) or (self.text_sprite.wrap_length != wrap_length) or (self.text_sprite.font.align != align):
            self.text_sprite.set_text(text, font, color, bg_color, antialiased, wrap_length, align)
        if pos_ip != (0, 0):
            self.text_sprite.move_ip(pos_ip)


class TextModal(GUIGroup[Text]):
    """
    Sprite group for `Text` sprites with a heading and description sprite. To modify the text, you have to access the sprites directly.
    """

    def __init__(self, *sprites, pos: pygame.typing.Point | None = None):
        self.heading_text = Text()
        self.heading_text.set_text()

        self.desc_text = Text()
        self.desc_text.set_text()

        super().__init__(self.heading_text, self.desc_text, pos=pos)
