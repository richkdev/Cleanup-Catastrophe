import pygame
from pygame.locals import *  # type: ignore

import enum
import pathlib

from scripts import common, utils
from scripts.sprites.basesprite import RGroup


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


class StateSwitch(BaseException):
    def __init__(self, state_id: StateID, *args) -> None:
        super().__init__(*args)
        self.state_id = state_id


class State:
    """
    Base class for game states to use.
    """
    event: list[pygame.Event]
    key: pygame.key.ScancodeWrapper
    key_jp: pygame.key.ScancodeWrapper
    mouse: pygame.Vector2 = pygame.Vector2()
    dt: float = 0.0

    is_gamemode: bool = False
    desc: str = "lipsum"

    def __init__(self) -> None:
        self.screen: pygame.Surface
        self.draw_screen: pygame.Surface

        self.parent_sprites: RGroup
        self.sprites = RGroup()

        self.assets_raw: list[str] = []
        self.sounds_raw: dict[str, str] = {}

        self.assets: list[pathlib.Path] = []

        # self.sound_manager: SoundManager

        self.next_states: list[StateID] = []

        self.is_prepared: bool = False
        self.is_loaded: bool = False
        self.is_reloadable: bool = False

        self.desc: str = f"In a heck of a {self.desc.upper()}" if self.is_gamemode else self.desc

    async def prepare(self) -> None:
        if not self.is_prepared or self.is_reloadable:
            self.prepare_assets()

            for asset_raw in self.assets_raw:
                asset = utils.newPath(asset_raw)

                if asset.is_dir():
                    files = asset.iterdir()
                    for file in files:
                        filepath = asset.joinpath(file)
                        self.assets.append(filepath)
                        common.ASSET_MANAGER.add_asset(filepath)
                        common.ASSET_MANAGER.update()

                if asset.is_file():
                    self.assets.append(asset)
                    common.ASSET_MANAGER.add_asset(asset)
                    common.ASSET_MANAGER.update()

            for name, path in self.sounds_raw.items():
                asset = utils.newPath(path)

                if "sfx" in path:
                    self.assets.append(asset)
                    common.ASSET_MANAGER.add_asset(asset)
                    common.ASSET_MANAGER.update()

            for asset in self.assets:
                common.ASSET_DICT.update(
                    {asset: await common.ASSET_MANAGER.get_asset(asset).get_data()}
                )

            self.prepare_sprites()
            self.prepare_next_states()
            self.is_prepared = True

            print(f"Prepared {type(self).__name__} state")

    def prepare_assets(self) -> None:
        raise NotImplementedError

    def prepare_sprites(self) -> None:
        raise NotImplementedError

    def prepare_next_states(self) -> None:
        ...

    async def load(
        self,
        screen: pygame.Surface,
        draw_screen: pygame.Surface,
        sprites: RGroup
    ) -> None:
        self.screen = screen
        self.draw_screen = draw_screen

        for name, path in self.sounds_raw.items():
            if "music" in path:
                common.SOUND_MANAGER.bgm.add_music(name, utils.newPath(path))
            else:
                common.SOUND_MANAGER.sfx.add_sfx(name, utils.newPath(path))

        self.load_assets()
        self.load_sprites()

        self.parent_sprites = sprites
        self.parent_sprites.add(self.sprites)

        print(f"Loaded {type(self).__name__} state")

    def load_sprites(self) -> None:
        ...

    def load_assets(self) -> None:
        ...

    def update(self) -> None:
        self.update_stuff()

        for event in self.event:
            if event.type == pygame.QUIT:
                common.IS_RUNNING = False

        self.logic()

        self.parent_sprites.update(self.dt)
        self.parent_sprites.draw(self.screen)

        self.screen.blit(self.draw_screen)

        common.SOUND_MANAGER.sfx.update()

    def update_stuff(self) -> None:
        self.event = pygame.event.get()
        self.key = pygame.key.get_pressed()
        self.key_jp = pygame.key.get_just_pressed()
        self.dt = max(common.MIN_DT, min(common.CLOCK.tick(common.FPS if not common.IS_WEB else 0)/1000, common.MAX_DT))

    def logic(self) -> None:
        ...

    def unload(self) -> None:
        self.parent_sprites.remove(self.sprites)
        common.SOUND_MANAGER.bgm.stop()
        common.SOUND_MANAGER.bgm.unload()
        common.SOUND_MANAGER.sfx.stop_all()
