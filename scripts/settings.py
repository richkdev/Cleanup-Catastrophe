import pygame
import sys
import os

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

import platform
from scripts import globals

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
    pygbag version                  {pygbag.VERSION if pygbag else "UNKNOWN"}
    PyInstaller version             {pyi.__version__ if pyi else "UNKNOWN"}

Platform info
    Platform name                   {platform.platform()}
    Running on Emscripten?          {globals.IS_WEB}
    Running on pygbag?              {globals.IS_PYGBAG}
    Running on Pyodide?             {globals.IS_PYODIDE}
    Supports OpenGL?                {bool(pygame.OPENGL)}
    Running on OpenGL?              {globals.FLAG_OPENGL}

Game info
    Game version                    {globals.VERSION}
    Maximum FPS                     {globals.FPS}
    CRT shader enabled?             {globals.retroMode}
    Vertex shader path              {globals.vertShader_path}
    Fragment shader path            {globals.fragShader_path}
    Discord Presence allowed?       {not globals.IS_WEB}

=====================================================
"""

if globals.IS_PYGBAG:
    platform.window.canvas.style.imageRendering = "pixelated" # type: ignore -> no more blurriness yay

os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'

# if not os.path.exists(newPath(logDirectory)):
#     os.makedirs(newPath(logDirectory))
# sys.stdout = open(newPath(f"{logDirectory}{current_time}.log"), "w+")
