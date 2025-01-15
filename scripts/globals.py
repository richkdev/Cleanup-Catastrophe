import pygame
import sys
from json import loads
from datetime import datetime
from scripts.utils import newPath

# global version, game_settings, emscripten
# global SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE
# global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_SIZE, SCALE_X, SCALE_Y

version = open(newPath("VERSION"), "r").read()
game_settings = loads(open(newPath("settings.json")).read())

emscripten = sys.platform in ('emscripten', 'wasi')  # detect if wasm/emscripten context

SCREEN_WIDTH: int = 320
SCREEN_HEIGHT: int = 224
SCREEN_SIZE: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

INITIAL_WINDOW_SIZE: tuple[int, int]

WINDOW_SIZE: tuple[int, int]

FINAL_WINDOW_SIZE: tuple[int, int]

xBorder: int = int(SCREEN_WIDTH ** 0.02)
yBorder: int = int(SCREEN_HEIGHT ** 0.02)

FPS: int = game_settings['maxFPS']
volume: float = game_settings['volume'] / 100

retroMode: bool = game_settings['retroMode']
fragShader_path: str
vertShader_path: str

match retroMode:
    case True:
        fragShader_path = newPath("assets/shaders/fragment_shaders/crt.glsl")
        vertShader_path = newPath("assets/shaders/vertex_shaders/crt.glsl")
    case False:
        fragShader_path = newPath("assets/shaders/fragment_shaders/normal.glsl")
        vertShader_path = newPath("assets/shaders/vertex_shaders/normal.glsl")

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
smallFont = pygame.font.SysFont("helvetica", 15)

GRAVITY: float = 2
GROUND_HEIGHT: int = int(SCREEN_HEIGHT//1.5)
