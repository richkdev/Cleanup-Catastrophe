import pygame
from pygame.locals import *  # type: ignore

import sys
from json import loads
from os import path
from datetime import datetime

pygame.init()


def newPath(relPath: str):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relPath)  # type: ignore -> pyinstaller temp folder
    else:
        return path.join(path.abspath('.'), relPath)


version = open(newPath("VERSION"), "r").read()
settings = loads(open(newPath("settings.json")).read())

emscripten = (sys.platform == 'emscripten') and OPENGL  # detect if wasm/emscripten context

WIDTH = 320
HEIGHT = 224

xBorder = int(WIDTH * 0.02)
yBorder = int(HEIGHT * 0.02)

FPS = settings['maxFPS']
volume = settings['volume'] / 100

fragmentShader = newPath(settings['fragmentShader'])
vertexShader = newPath(settings['vertexShader'])

mapDirectory = newPath(settings['mapDirectory'])
saveFileDirectory = newPath(settings['saveFileDirectory'])
logDirectory = newPath(settings['logDirectory'])

clock = pygame.time.Clock()

DARKRED = (100, 0, 0, 255)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)

bigFont = pygame.font.Font(newPath("assets/fonts/genesis.ttf"), 20)
smallFont = pygame.font.SysFont("helvetica", 15)

# sound paths premade
sound_clean_up_time = newPath("assets/music/cleanup-time.wav")
