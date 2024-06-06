import pygame
from scripts.settings import *

class Cutter(object):
    def __init__(self, filename: str, size: dict[str, int] = {"width": 48, "height": 48}):
        self.sheet = pygame.image.load(str(filename)).convert()
        self.sheet_items: list = []
        width, height = size['width'], size['height']
        self.frames_x: int = int(self.sheet.get_width()//width)

        for i in range(self.frames_x):
            self.sheet_items.append(self.sheet.subsurface(pygame.rect.Rect(i*width, 0, width, height)))

        self.frame = 0

    def draw(self, screen: pygame.surface.Surface, coords: tuple[int, int], frameSpeed: int = 1):
        screen.blit(self.sheet_items[self.frame], coords)
        self.frame += frameSpeed
        if self.frame == self.frames_x:
            self.frame = 0

# heavy WIP
