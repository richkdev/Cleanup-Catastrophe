import pygame
import numpy
import pathlib
import sys
import os
import sys
import platform

from scripts import common

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


def newPath(relPath: str) -> pathlib.Path:
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    else:
        basePath = os.path.abspath('.')
    return pathlib.Path(os.path.join(basePath, relPath))


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


def mode7(
    image: pygame.Surface,
    target_size: pygame.typing.IntPoint,
    cam: pygame.Vector3 = pygame.Vector3(0, 0, 10),
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

    for y in range(target_size[1]):
        pz = y + cam.z
        sy = fov / pz

        for x in range(target_size[0]):
            px = x - image.size[0] / 2
            sx = px / pz

            rotated_sx = sx * numpy.cos(angle) - sy * numpy.sin(angle)
            rotated_sy = sx * numpy.sin(angle) + sy * numpy.cos(angle)

            texture_x = (rotated_sx * scale + cam.x) % image.size[0]
            texture_y = (rotated_sy * scale + cam.y) % image.size[1]

            color = image.get_at((int(texture_x), int(texture_y)))
            new_image.set_at((x, y), color)

    return new_image
