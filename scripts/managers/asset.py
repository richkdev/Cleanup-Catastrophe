import asyncio
import pygame
import pathlib
import json


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
        self.data: Asset

    async def get_data(self) -> Asset:
        if self.path.exists() and self.path.is_file():
            if any(ex in self.path.suffix for ex in self.IMAGE_EXTENSIONS):
                self.data = await self.loop.create_task(lazyload_image(self.path))
            elif any(ex in self.path.suffix for ex in self.SOUND_EXTENSIONS):
                self.data = await self.loop.create_task(lazyload_sfx(self.path))
            elif any(ex in self.path.suffix for ex in self.FONT_EXTENSIONS):
                self.data = await self.loop.create_task(lazyload_font(self.path))
            elif any(ex in self.path.suffix for ex in self.JSON_EXTENSIONS):
                self.data = await self.loop.create_task(lazyload_json(self.path))
            else:
                self.data = await self.loop.create_task(lazyload_text(self.path))
            return self.data
        else:
            raise FileNotFoundError(self.path)


class AssetManager:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
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
