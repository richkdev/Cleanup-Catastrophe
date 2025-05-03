import pygame
from pygame.locals import *  # type: ignore

import enum
import typing

from scripts import globals
from scripts.sound import SoundManager


class StateID(enum.IntEnum):
    SPLASH = 0
    LOBBY = enum.auto()
    CATASTROPHE = enum.auto()
    SHOP = enum.auto()
    SCOREBOARD = enum.auto()


class State:
    """
    Base class for game states to use.
    """

    def __init__(self, is_gamemode: bool, desc: str = "lipsum") -> None:
        self.screen: pygame.Surface
        self.sprites: pygame.sprite.Group
        self.sound_manager: SoundManager
        self.switch_state: typing.Callable[[StateID], None]

        self.is_gamemode = is_gamemode
        self.desc = f"In a heck of a {type(self).__name__}" if self.is_gamemode else desc

        self.is_loaded: bool = False

        self.key: pygame.key.ScancodeWrapper
        self.event: list[pygame.Event]
        self.mouse = pygame.Vector2()
        self.dt: float = 0.0

        print(f"Prepared {type(self).__name__} state")

    def load(
        self,
        screen: pygame.Surface,
        sprites: pygame.sprite.Group,
        sound_manager: SoundManager,
        switch_state: typing.Callable[[StateID], None],
    ) -> None:
        self.screen = screen
        self.sprites = sprites
        self.sound_manager = sound_manager
        self.switch_state = switch_state

        self.load_sprites()
        self.load_sounds()

        print(f"Loaded {type(self).__name__} state")

    def load_sprites(self) -> None:
        ...

    def load_sounds(self) -> None:
        ...

    def update(self) -> None:
        self.key = pygame.key.get_pressed()
        self.event = pygame.event.get()

        self.mouse.x, self.mouse.y = pygame.mouse.get_pos()  # will use one day
        print(self.mouse.x, self.mouse.y)

        self.dt = max(0.001, min(globals.clock.tick_busy_loop(globals.FPS)/1000, 0.1))

        self.sprites.update(self.key, self.dt)
        self.sprites.draw(self.screen)

        self.sound_manager.update()

        self.logic()

    def logic(self) -> None:
        ...

    def unload(self) -> None:
        self.sprites.empty()
        self.sound_manager.stop_all()
