import pygame
import os
import sys
from json import loads
from datetime import datetime
from scripts.utils import newPath

IS_RUNNING: bool = True
VERSION = open(newPath("VERSION"), "r").read()
SETTINGS: dict = loads(open(newPath("settings.json")).read())

IS_WEB: bool = sys.platform in ('emscripten', 'wasi')  # detect if wasm/emscripten context
IS_PYGBAG: bool = bool(int(os.getenv('PYGBAG', default=0)))
IS_PYODIDE: bool = "pyodide" in sys.modules

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 224
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FINAL_SCREEN_SIZE: tuple[int, int] = SCREEN_SIZE

INITIAL_WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE
WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE

xBorder: int = int(SCREEN_WIDTH ** 0.05)
yBorder: int = int(SCREEN_HEIGHT ** 0.05)

FLAG_OPENGL: bool = SETTINGS['opengl'] and bool(pygame.OPENGL)
FLAG_DEBUG: bool = SETTINGS['debug']

FPS: int = SETTINGS['maxFPS']
MIN_DT: float = FPS/100000
MAX_DT: float = FPS/100

volume: float = SETTINGS['volume'] / 100

retroMode: bool = SETTINGS['retroMode']
fragShader_path  = newPath(f"assets/shaders/fragment_shaders/{'crt' if retroMode else 'normal'}.glsl")
vertShader_path = newPath(f"assets/shaders/vertex_shaders/{'crt' if retroMode else 'normal'}.glsl")

mapDirectory = newPath(SETTINGS['mapDirectory'])
saveFileDirectory = newPath(SETTINGS['saveFileDirectory'])

startGame_time = str(datetime.now().replace(microsecond=0)).replace(":", "-")
logDirectory = newPath(SETTINGS['logDirectory'])

clock = pygame.time.Clock()

DARKRED = pygame.Color(100, 0, 0, 255)
RED = pygame.Color(255, 0, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
SAND = pygame.Color(255, 235, 100)
GREEN = pygame.Color(0, 255, 0, 255)
BLUE = pygame.Color(0, 0, 255, 255)
WHITE = pygame.Color(255, 255, 255, 255)
BLACK = pygame.Color(0, 0, 0, 255)

if not pygame.font.get_init():
    pygame.font.init()

bigFont = pygame.Font(newPath("assets/fonts/genesis.ttf"), 16)
smallFont = pygame.Font(newPath("assets/fonts/UnifontExMono.ttf"), 14)

GRAVITY: float = 2
GROUND_HEIGHT: float = SCREEN_HEIGHT/1.5
WATER_HEIGHT: float = SCREEN_HEIGHT*0.6

TEMPLATE_IMAGE_PATH = newPath("icon.ico")
TEMPLATE_IMAGE_SURF = pygame.image.load(TEMPLATE_IMAGE_PATH)
