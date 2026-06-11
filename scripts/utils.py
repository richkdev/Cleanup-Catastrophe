import pygame
import numpy
import pathlib
import json
import sys
import os
import sys
import platform
import functools

from scripts import common
from scripts.sprites.sheet import Sheet

try:
    import zengl
except ImportError:
    zengl = None

try:
    import PyInstaller as pyi
except ImportError:
    pyi = None

try:
    import pygbag
except ImportError:
    pygbag = None

if not hasattr(pygame, "IS_CE"):
    raise ImportError("This game requires pygame-ce to function.")

if sys.version_info < (3, 12):
    raise DeprecationWarning("This game requires Python versions 3.12+ to function.")


@functools.lru_cache
def get_game_data() -> str:
    return f"""
===================== GAME DATA =====================

Dependency info
    Python version                  {platform.python_version()}
    pygame-ce version               {pygame.version.vernum}
    SDL version                     {pygame.version.SDL}
    ZenGL version                   {zengl.__dict__['__version__'] if zengl else "UNKNOWN"}
    pygbag version                  {pygbag.__version__ if pygbag else "UNKNOWN"}
    PyInstaller version             {pyi.__version__ if pyi else "UNKNOWN"}

Platform info
    Platform name                   {platform.platform()}
    Running on Emscripten?          {common.IS_WEB}
    Running on pygbag?              {common.IS_PYGBAG}
    Running on Pyodide?             {common.IS_PYODIDE}
    Supports OpenGL?                {bool(pygame.OPENGL)}
    Running on OpenGL?              {common.FLAG_OPENGL}

Game info
    Game version                    {common.VERSION}
    Maximum FPS                     {common.FPS}
    CRT shader enabled?             {common.retroMode}
    Vertex shader path              {common.vertShader_path}
    Fragment shader path            {common.fragShader_path}
    Discord Presence allowed?       {not common.IS_WEB}

=====================================================
"""


@functools.lru_cache
def newPath(relPath: str) -> pathlib.Path:
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    else:
        basePath = os.path.abspath('.')
    return pathlib.Path(os.path.join(basePath, relPath))


@functools.lru_cache
def cut_sheet_fixed_size(
    path: pathlib.Path,
    size: pygame.typing.IntPoint
) -> list[pygame.Surface]:
    """
    utility to cut a spritesheet with fixed size into a list of pygame surfs
    """

    frames = []
    sheet_img: pygame.Surface = common.ASSET_DICT.get(path, pygame.image.load(path).convert_alpha())

    for i in range(int(sheet_img.get_width() / size[0])):
        frames.append(sheet_img.subsurface(pygame.Rect(i * size[0], 0, size[0], size[1])))

    print(f"Loaded and split fixed size spritesheet at {path}")
    return frames


@functools.lru_cache
def cut_sheet(path: pygame.typing._PathLike) -> Sheet:
    json_path = newPath(str(path))
    raw_data: list = common.ASSET_DICT.get(json_path, json.loads(open(json_path).read()))
    spritesheet = Sheet()

    for data in raw_data:
        spritesheet_path = json_path.parent / data['file'] # image needs to be in the same folder as json
        spritesheet_img: pygame.Surface = common.ASSET_DICT.get(spritesheet_path, pygame.image.load(spritesheet_path).convert_alpha())

        anim: list[pygame.Surface] = []
        for frame in data['frames']:
            size = frame['bounds']['x'], frame['bounds']['y'], frame['bounds']['w'], frame['bounds']['h']
            print(size)
            anim.insert(frame['frame'], spritesheet_img.subsurface(size))

        spritesheet.add_animation(
            data['action'],
            anim
        )

    print(f"Loaded and split dynamic size spritesheet at {spritesheet_path}")

    spritesheet.set_animation(raw_data[0]['action']) # default setting

    return spritesheet


@functools.lru_cache
def aspectScale(image_x: int, image_y: int, target_x: int, target_y: int) -> tuple[int, int]:
    """
    for zengl scaling.
    very slightly modified ver of https://www.pygame.org/pcr/transform_scale/
    """

    if image_x > image_y:
        # fit to width
        scale_factor = target_x/image_x
        scaled_y = scale_factor * image_y
        if scaled_y > target_y:
            scale_factor = target_y/image_y
            scaled_x = scale_factor * image_x
            scaled_y = target_y
        else:
            scaled_x = target_x
    else:
        # fit to height
        scale_factor = target_y/image_y
        scaled_x = scale_factor * image_x
        if scaled_x > target_x:
            scale_factor = target_x/image_x
            scaled_x = target_x
            scaled_y = scale_factor * image_y
        else:
            scaled_y = target_y

    del scale_factor

    scaled_x = int(scaled_x)
    scaled_y = int(scaled_y)

    return scaled_x, scaled_y


@functools.lru_cache
def multiply_image(
    input_image: pygame.Surface,
    tile_size: pygame.typing.IntPoint,
    target_size: pygame.typing.IntPoint
) -> pygame.Surface:
    """
    utility to produce an image with a size of target_size, contains repeated copies of the image from tile_size
    """

    output_image = pygame.Surface(target_size, pygame.SRCALPHA)

    for y in range(0, int(target_size[1]), int(tile_size[1])):
        for x in range(0, int(target_size[0]), int(tile_size[0])):
            output_image.blit(input_image, (x, y))

    return output_image


@functools.lru_cache
def mode7(
    image: pygame.Surface,
    target_size: pygame.typing.IntPoint,
    cam: pygame.typing.Point = (0, 0, 10),
    angle: int = 0,
    fov: int = 250,
    scale: int = 10
) -> pygame.Surface:
    """
    utility to produce a mode 7 effect on an image.
    dont call this every frame.
    might have to do some numba njit wizardry so that its faster.
    """

    new_image = pygame.Surface(target_size)
    new_image_arr = pygame.surfarray.pixels3d(new_image)

    for y in range(target_size[1]):
        pz = y + cam[2]
        sy = fov / pz

        for x in range(target_size[0]):
            px = x - image.size[0] / 2
            sx = px / pz

            sin = numpy.sin(angle)
            cos = numpy.cos(angle)

            rotated_sx = sx * cos - sy * sin
            rotated_sy = sx * sin + sy * cos

            texture_x = (rotated_sx * scale + cam[0]) % image.size[0]
            texture_y = (rotated_sy * scale + cam[1]) % image.size[1]

            color = image.get_at((int(texture_x), int(texture_y)))
            new_image_arr[x][y] = color[:3]

    return new_image
