import pygame
from scripts.settings import *


def cutSheet(path: str, size: pygame.math.Vector2) -> list[pygame.surface.Surface]:
    frames = []
    sheet_img = pygame.image.load(path).convert_alpha()
    # sheet_img.set_colorkey((0, 0, 0))

    for i in range(int(sheet_img.get_width() // size.x)):
        frames.append(sheet_img.subsurface(
            pygame.rect.Rect(i * size.x, 0, size.x, size.y)))

    print(f"Loaded and split spritesheet at {path}")
    return frames


class Sheet(object):
    def __init__(self) -> None:
        self.states: dict[str, list[pygame.surface.Surface]] = {}
        self.current_state = ""
        self.current_idx = 0.0

    def add_animation(self, name: str, sprites: list[pygame.surface.Surface]) -> None:
        self.states[name] = sprites

    def set_action(self, action: str) -> None:
        if action in self.states:
            self.current_state = action

    def update(self, val: float = 0.1) -> None:
        self.current_idx += val

    def draw(self, flip_x: bool = False) -> pygame.surface.Surface:
        idx = int(self.current_idx % len(self.states[self.current_state]))
        surf = self.states[self.current_state][idx]
        surf = pygame.transform.flip(surf, flip_x, False)
        return surf
