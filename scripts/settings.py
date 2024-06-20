import pygame
from pygame import Vector2, FRect, Surface, Rect
import sys
from json import loads
from os import path, makedirs
from datetime import datetime


def newPath(relPath: str):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relPath)  # type: ignore -> pyinstaller temp folder
    else:
        return path.join(path.abspath('.'), relPath)


version = open(newPath("VERSION"), "r").read()
settings = loads(open(newPath("settings.json")).read())

emscripten = sys.platform == 'emscripten'  # detect if wasm/emscripten context

WIDTH = 320
HEIGHT = 224

xBorder = int(WIDTH * 0.02)
yBorder = int(HEIGHT * 0.02)

FPS: int = settings['maxFPS']
volume: float = settings['volume'] / 100

fragmentShader: str = newPath(settings['fragmentShader'])
vertexShader: str = newPath(settings['vertexShader'])

mapDirectory: str = newPath(settings['mapDirectory'])
saveFileDirectory: str = newPath(settings['saveFileDirectory'])

current_time: str = str(datetime.now().replace(microsecond=0)).replace(":", "-")
logDirectory: str = newPath(settings['logDirectory'])

clock = pygame.time.Clock()

DARKRED = (100, 0, 0, 255)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)

pygame.font.init()

bigFont = pygame.font.Font(newPath("assets/fonts/genesis.ttf"), 20)
smallFont = pygame.font.SysFont("helvetica", 15)

if not path.exists(newPath(logDirectory)):
    makedirs(newPath(logDirectory))

# richy: very basic logging system, will remove later
sys.stdout = open(newPath(f"{logDirectory}{current_time}.log"), "w+")
