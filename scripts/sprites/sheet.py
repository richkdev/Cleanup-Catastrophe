import pygame
from pygame import Vector2, Surface
from scripts.settings import *


class Cutter(object):
    def __init__(self, filename: str, size: dict[str, int] = {"width": 48, "height": 48}):
        self.sheet = pygame.image.load(str(filename)).convert()
        self.sheet_items: list = []
        width, height = size['width'], size['height']
        self.frames_x: int = int(self.sheet.get_width() // width)

        for i in range(self.frames_x):
            self.sheet_items.append(self.sheet.subsurface(pygame.rect.Rect(i * width, 0, width, height)))

        self.frame = 0

    def draw(self, screen: pygame.surface.Surface, coords: tuple[int, int], frameSpeed: int = 1):
        screen.blit(self.sheet_items[self.frame], coords)
        self.frame += frameSpeed
        if self.frame == self.frames_x:
            self.frame = 0

# heavy WIP
# 2024-06-06 hulahhh: I suggest we get rid of a dictionary as an arugment and just use a pygame.math.Vector2 this way its simpler by just calling .x or .y (they are also really fast and you can do math with them) I wrote the lines but left them as a comment.

# 2024-06-06 hulahhh: i prototyped that idea from earlier. Could theoretically expand with frame times per animation meaning running will switch frames faster than idel or smt like that


def cut_sprite_sheet(path: str, size: Vector2 = Vector2(48, 48)) -> list[Surface]:
    ret = []
    sheet_img = pygame.image.load(path).convert()
    sheet_img.set_colorkey((0, 0, 0))

    for i in range(int(sheet_img.get_width() // size.x)):
        ret.append(sheet_img.subsurface(pygame.rect.Rect(i * size.x, 0, size.x, size.y)))

    return ret


class Animation:
    def __init__(self) -> None:
        self.states: dict[str, list[Surface]] = {}

        self.current_state: str = ""

        self.current_idx = 0.0

    def add_animation(self, name: str, sprites: list[Surface]) -> None:
        self.states[name] = sprites

    def set_action(self, action: str) -> None:
        if action in self.states:
            self.current_state = action

    def update(self, val: float = .2) -> None:
        self.current_idx += val

    def render(self, screen: Surface, pos: tuple) -> None:
        idx = int(self.current_idx % len(self.states[self.current_state]))
        surf = self.states[self.current_state][idx]
        screen.blit(surf, pos)
