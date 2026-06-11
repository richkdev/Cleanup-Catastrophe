import pygame


class Sheet:
    def __init__(self) -> None:
        self.states: dict[str, list[pygame.surface.Surface]] = {}
        self.current_state: str
        self.current_idx = 0.0

    def add_animation(self, name: str, sprites: list[pygame.surface.Surface]) -> None:
        self.states[name] = sprites

    def set_animation(self, name: str) -> None:
        if name in self.states:
            self.current_state = name

    def update(self, val: float = 0.1) -> None:
        self.current_idx += val

    def draw(self, flip_x: bool = False, flip_y: bool = False) -> pygame.surface.Surface:
        idx = int(self.current_idx % len(self.states[self.current_state]))
        surf = self.states[self.current_state][idx]
        surf = pygame.transform.flip(surf, flip_x, flip_y)
        return surf
