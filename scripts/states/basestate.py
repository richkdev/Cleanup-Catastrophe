import pygame
from pygame.locals import *  # type: ignore

import enum
import typing

from scripts import globals, utils
from scripts.sprites.basesprite import RGroup
from scripts.sound import SoundManager


class StateID(enum.IntEnum):
    """
    State identifier.
    """
    SPLASH = 0
    LOBBY = enum.auto()
    CATASTROPHE = enum.auto()
    SHOP = enum.auto()
    SCOREBOARD = enum.auto()
    RADIO = enum.auto()


class State:
    """
    Base class for game states to use.
    """
    event: list[pygame.Event]
    key: pygame.key.ScancodeWrapper
    mouse: pygame.Vector2 = pygame.Vector2()
    dt: float = 0.0

    def __init__(self, is_gamemode: bool, desc: str = "lipsum") -> None:
        self.screen: pygame.Surface
        self.draw_screen: pygame.Surface

        self.parent_sprites: RGroup
        self.sprites = RGroup()

        self.sound_manager: SoundManager
        self.sounds: dict[str, str] = {}

        self.switch_state: typing.Callable[[StateID], None]
        self.next_states: list[StateID] = []

        self.is_prepared: bool = False
        self.is_loaded: bool = False
        self.is_reloadable: bool = False

        self.is_gamemode: bool = is_gamemode
        self.desc: str = f"In a heck of a {desc.upper()}" if self.is_gamemode else desc

    def prepare(self) -> None:
        if not self.is_prepared or self.is_reloadable:
            self.prepare_sounds()
            self.prepare_sprites()
            self.prepare_next_states()
            self.is_prepared = True

            print(f"Prepared {type(self).__name__} state")

    def prepare_sprites(self) -> None:
        raise NotImplementedError

    def prepare_sounds(self) -> None:
        raise NotImplementedError

    def prepare_next_states(self) -> None:
        ...

    def load(
        self,
        screen: pygame.Surface,
        draw_screen: pygame.Surface,
        sprites: RGroup,
        sound_manager: SoundManager,
        switch_state: typing.Callable[[StateID], None],
    ) -> None:
        self.screen = screen
        self.draw_screen = draw_screen

        for name, path in self.sounds.items():
            if "music" in path:
                sound_manager.bgm.add_music(name, utils.newPath(path))
            else:
                sound_manager.sfx.add_sfx(name, utils.newPath(path))
        self.sound_manager = sound_manager

        self.switch_state = switch_state

        self.load_sprites()
        self.load_sounds()

        self.parent_sprites = sprites
        self.parent_sprites.add(self.sprites)

        print(f"Loaded {type(self).__name__} state")

    def load_sprites(self) -> None:
        ...

    def load_sounds(self) -> None:
        ...

    def update(self) -> None:
        self.update_stuff()

        for event in self.event:
            if event.type == pygame.QUIT:
                globals.IS_RUNNING = False

        self.logic()

        self.parent_sprites.update(self.dt)
        self.parent_sprites.draw(self.screen)

        self.screen.blit(self.draw_screen)

        self.sound_manager.sfx.update()

    def update_stuff(self):
        self.event = pygame.event.get()
        self.key = pygame.key.get_pressed()
        self.dt = max(globals.MIN_DT, min(globals.clock.tick(globals.FPS if not globals.IS_WEB else 0)/1000, globals.MAX_DT))

    def logic(self) -> None:
        ...

    def unload(self) -> None:
        self.parent_sprites.remove(self.sprites)
        self.sound_manager.bgm.stop()
        self.sound_manager.bgm.unload()
        self.sound_manager.sfx.stop_all()
        self.sounds.clear()
