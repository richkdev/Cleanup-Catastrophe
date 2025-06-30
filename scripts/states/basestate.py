import pygame
from pygame.locals import *  # type: ignore

import enum
import typing

from scripts import globals, utils
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

        self.parent_sprites: pygame.sprite.Group
        self.sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.sound_manager: SoundManager
        self.sounds: dict[str, str] = {}

        self.switch_state: typing.Callable[[StateID], None]
        self.next_states: list[StateID] = []

        self.is_gamemode = is_gamemode
        self.desc = f"In a heck of a {type(self).__name__}" if self.is_gamemode else desc

        self.is_prepared: bool = False
        self.is_loaded: bool = False
        self.is_reloadable: bool = False

        self.substate: int

        self.key: pygame.key.ScancodeWrapper
        self.event: list[pygame.Event]
        self.mouse = pygame.Vector2()
        self.dt: float = 0.0

    def prepare(self) -> None:
        if not self.is_prepared or self.is_reloadable:
            self.prepare_next_states()
            self.prepare_sounds()
            self.prepare_sprites()
            self.is_prepared = True

            print(f"Prepared {type(self).__name__} state")

    def prepare_sprites(self) -> None:
        ...

    def prepare_sounds(self) -> None:
        ...

    def prepare_next_states(self) -> None:
        ...

    def load(
        self,
        screen: pygame.Surface,
        sprites: pygame.sprite.Group,
        sound_manager: SoundManager,
        switch_state: typing.Callable[[StateID], None],
    ) -> None:
        self.screen = screen

        self.parent_sprites = sprites
        self.parent_sprites.add(self.sprites)

        for name, path in self.sounds.items():
            sound_manager.add_sound(name, utils.newPath(path))
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

        self.mouse.x, self.mouse.y = pygame.mouse.get_pos()  # will use one 

        # scale_x = globals.FINAL_WINDOW_SIZE[0]/globals.SCREEN_SIZE[0]
        # scale_y = globals.FINAL_WINDOW_SIZE[1]/globals.SCREEN_SIZE[1]
        # print(self.mouse.x//scale_x, self.mouse.y//scale_y)

        dt = globals.clock.tick_busy_loop(globals.FPS)/1000
        self.dt = max(globals.MIN_DT, min(dt, globals.MAX_DT))

        self.logic()

        self.parent_sprites.update(self.key, self.dt)
        self.parent_sprites.draw(self.screen)

        self.sound_manager.update()

    def logic(self) -> None:
        ...

    def unload(self) -> None:
        self.parent_sprites.remove(self.sprites)
        self.sound_manager.stop_all()
        self.sounds.clear()
