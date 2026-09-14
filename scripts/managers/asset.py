import pygame
import asyncio
import typing
import pathlib
import json

from scripts.managers.basemanager import LoopManager


async def lazyload_image(path: pathlib.Path) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()

async def lazyload_sfx(path: pathlib.Path) -> pygame.Sound:
    return pygame.mixer.Sound(path)

async def lazyload_font(path: pathlib.Path) -> pygame.Font:
    return pygame.font.Font(path, 16)

async def lazyload_json(path: pathlib.Path) -> list | dict:
    return json.loads(open(path).read())

async def lazyload_text(path: pathlib.Path) -> str:
    return open(path).read()


Asset = pygame.typing.FileLike | pygame.Surface | pygame.Sound | pygame.Font | list | dict

class LazyAsset:
    IMAGE_EXTENSIONS = ('bmp', 'gif', 'jpeg', 'jpg', 'lbm', 'png', 'pcx', 'pnm', 'pbm', 'pgm', 'ppm', 'qoi', 'tga', 'tiff', 'webp', 'xpm', 'xcf')
    SOUND_EXTENSIONS = ('wav', 'mp3', 'ogg', 'flac', 'opus', 'wv', 'mod', 'midi')
    FONT_EXTENSIONS = ('ttf')
    JSON_EXTENSIONS = ('json')

    def __init__(self, loop: asyncio.AbstractEventLoop, path: pathlib.Path) -> None:
        self.loop = loop
        self.path = path
        self.task: asyncio.Task[Asset]
        self.data: Asset

        func: typing.Callable[[pathlib.Path], typing.Awaitable[Asset]]
        if self.path.exists() and self.path.is_file():
            if any(ex in self.path.suffix for ex in self.IMAGE_EXTENSIONS):
                func = lazyload_image
            elif any(ex in self.path.suffix for ex in self.SOUND_EXTENSIONS):
                func = lazyload_sfx
            elif any(ex in self.path.suffix for ex in self.FONT_EXTENSIONS):
                func = lazyload_font
            elif any(ex in self.path.suffix for ex in self.JSON_EXTENSIONS):
                func = lazyload_json
            else:
                func = lazyload_text

            self.task = self.loop.create_task(coro=func(self.path), eager_start=True)
        else:
            raise FileNotFoundError(self.path)

    async def get_data(self) -> Asset:
        try:
            self.data
        except AttributeError:
            self.data = await self.task

        return self.data


class AssetManager(LoopManager):
    """
    manager for lazily loading assets (images, sfx, fonts, json, txt) on the event loop
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__(loop)

        self.asset_queue: list[pathlib.Path] = []
        self.asset_results: dict[pathlib.Path, LazyAsset] = {}

    def add_asset(self, path: pathlib.Path):
        self.asset_queue.append(path)

    def get_asset(self, path: pathlib.Path) -> LazyAsset:
        asset = self.asset_results[path]
        if asset == None:
            self.asset_results[path] = LazyAsset(self.loop, path)
            return self.asset_results[path]
        else:
            return asset

    def update(self):
        for item in self.asset_queue:
            data = LazyAsset(self.loop, item)

            self.asset_results.update(
                {item: data}
            )

            self.asset_queue.remove(item)

    def quit(self):
        self.asset_queue.clear()
        self.asset_results.clear()
