import pygame
from pygame import Color, Vector2, FRect, Surface, Rect
import sys
from json import loads
import os
from datetime import datetime

if not getattr(pygame, "IS_CE", False):
    raise ImportError("This game requires pygame-ce 2.5.0 and above to function, not pygame.",
                      "Uninstall pygame then install pygame-ce 2.5.0+")

if sys.version_info < (3, 12):
    raise DeprecationWarning("This game requires Python versions 3.12+ to function.")

def newPath(relPath: str):
    relPath = relPath.replace("/", os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS  # type: ignore -> pyinstaller temp folder
    else:
        basePath = os.path.abspath('.')
    return os.path.join(basePath, relPath)


version = open(newPath("VERSION"), "r").read()
settings = loads(open(newPath("settings.json")).read())

emscripten = sys.platform in ('emscripten', 'wasi')  # detect if wasm/emscripten context

WIDTH: int = 320
HEIGHT: int = 224

xBorder = int(WIDTH * 0.02)
yBorder = int(HEIGHT * 0.02)

FPS: int = settings['maxFPS']
volume: float = settings['volume'] / 100

retroMode: bool = settings['retroMode']
fragmentShader: str
vertexShader: str

match retroMode:
    case True:
        fragmentShader = newPath("assets/shaders/fragment_shaders/crt.glsl")
        vertexShader = newPath("assets/shaders/vertex_shaders/crt.glsl")
    case False:
        fragmentShader = newPath("assets/shaders/fragment_shaders/normal.glsl")
        vertexShader = newPath("assets/shaders/vertex_shaders/normal.glsl")

mapDirectory: str = newPath(settings['mapDirectory'])
saveFileDirectory: str = newPath(settings['saveFileDirectory'])

current_time: str = str(datetime.now().replace(microsecond=0)).replace(":", "-")
logDirectory: str = newPath(settings['logDirectory'])

clock = pygame.time.Clock()

DARKRED = Color(100, 0, 0, 255)
RED = Color(255, 0, 0, 255)
YELLOW = Color(255, 255, 0, 255)
GREEN = Color(0, 255, 0, 255)
BLUE = Color(0, 0, 255, 255)
WHITE = Color(255, 255, 255, 255)
BLACK = Color(0, 0, 0, 255)
TRANSPARENT = Color(0, 0, 0, 0)

pygame.font.init()

bigFont = pygame.font.Font(newPath("assets/fonts/genesis.ttf"), 20)
smallFont = pygame.font.SysFont("helvetica", 15)

if not os.path.exists(newPath(logDirectory)):
    os.makedirs(newPath(logDirectory))

# sys.stdout = open(newPath(f"{logDirectory}{current_time}.log"), "w+")
