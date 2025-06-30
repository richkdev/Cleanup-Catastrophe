import pygame
import sys
from json import loads
from datetime import datetime
from scripts.utils import newPath

version = open(newPath("VERSION"), "r").read()
game_settings = loads(open(newPath("settings.json")).read())

emscripten = sys.platform in ('emscripten', 'wasi')  # detect if wasm/emscripten context
pyodide = "pyodide" in sys.modules

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 224
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

INITIAL_WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE
WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE
FINAL_WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE

xBorder: int = int(SCREEN_WIDTH ** 0.05)
yBorder: int = int(SCREEN_HEIGHT ** 0.05)

FPS: int = game_settings['maxFPS']
MIN_DT: float = FPS/1000000
MAX_DT: float = FPS/100

volume: float = game_settings['volume'] / 100

retroMode: bool = game_settings['retroMode']
fragShader_path: str  = newPath(f"assets/shaders/fragment_shaders/{"crt" if retroMode else "normal"}.glsl")
vertShader_path: str = newPath(f"assets/shaders/vertex_shaders/{"crt" if retroMode else "normal"}.glsl")

mapDirectory: str = newPath(game_settings['mapDirectory'])
saveFileDirectory: str = newPath(game_settings['saveFileDirectory'])

startGame_time: str = str(datetime.now().replace(microsecond=0)).replace(":", "-")
logDirectory: str = newPath(game_settings['logDirectory'])

clock = pygame.time.Clock()

DARKRED = pygame.Color(100, 0, 0, 255)
RED = pygame.Color(255, 0, 0, 255)
YELLOW = pygame.Color(255, 255, 0, 255)
GREEN = pygame.Color(0, 255, 0, 255)
BLUE = pygame.Color(0, 0, 255, 255)
WHITE = pygame.Color(255, 255, 255, 255)
BLACK = pygame.Color(0, 0, 0, 255)
TRANSPARENT = pygame.Color(0, 0, 0, 0)

pygame.font.init()

bigFont = pygame.font.Font(newPath("assets/fonts/genesis.ttf"), 20)
smallFont = pygame.font.Font(newPath("assets/fonts/UnifontExMono.ttf"), 15)

GRAVITY: float = 2
GROUND_HEIGHT: int = int(SCREEN_HEIGHT//1.5)
