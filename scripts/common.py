import pygame
import os
import sys
import pathlib
import numpy

from json import loads
from datetime import datetime
from scripts.utils import newPath
from scripts.managers.asset import AssetManager, Asset

IS_RUNNING: bool = True

VERSION = open(newPath("VERSION"), "r").read()
SETTINGS: dict = loads(open(newPath("settings.json")).read())

IS_WEB: bool = sys.platform in ('emscripten', 'wasi')  # detect if wasm/emscripten context
IS_PYGBAG: bool = bool(int(os.getenv('PYGBAG', default=0)))
IS_PYODIDE: bool = "pyodide" in sys.modules
IS_DISCORD_ALLOWED = not IS_WEB and not IS_PYGBAG

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 224
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FINAL_SCREEN_SIZE: tuple[int, int] = SCREEN_SIZE

INITIAL_WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE
WINDOW_SIZE: tuple[int, int] = SCREEN_SIZE

X_BORDER = 8
Y_BORDER = 8

FLAG_OPENGL: bool = SETTINGS['opengl'] and bool(pygame.OPENGL) and not IS_WEB
FLAG_DEBUG: bool = SETTINGS['debug']

FPS: float = SETTINGS['maxFPS']
MIN_DT: float = (1/FPS)/1000
MAX_DT: float = 1

VOLUME: float = SETTINGS['volume'] / 100

retroMode: bool = SETTINGS['retroMode']
fragShader_path  = newPath(f"assets/shaders/fragment_shaders/{'crt' if retroMode else 'normal'}.glsl")
vertShader_path = newPath(f"assets/shaders/vertex_shaders/{'crt' if retroMode else 'normal'}.glsl")

saveFiles_path = newPath(SETTINGS['savefiles'])

startGame_time = str(datetime.now().replace(microsecond=0)).replace(":", "-")
logDirectory = newPath(SETTINGS['logs'])

CLOCK = pygame.time.Clock()

if not pygame.font.get_init():
    pygame.font.init()


BIG_FONT_PATH = newPath("assets/fonts/genesis.ttf")
SMALL_FONT_PATH = newPath("assets/fonts/UnifontExMono.ttf")

BIG_FONT = pygame.Font(BIG_FONT_PATH, 16)
SMALL_FONT = pygame.Font(SMALL_FONT_PATH, 16)

GRAVITY: float = 2.5

CLOUD_HEIGHT: float = SCREEN_HEIGHT*0.1
GROUND_HEIGHT: float = SCREEN_HEIGHT*0.65
WATER_HEIGHT: float = SCREEN_HEIGHT*0.35

##########################

TEMPLATE_IMAGE_PATH = newPath("icon.ico")
TEMPLATE_IMAGE_SURF = pygame.image.load(TEMPLATE_IMAGE_PATH)

TEMPLATE_JSON_PATH = newPath("assets/img/sprites/template.json")

##########################

ASSET_MANAGER: AssetManager

ASSET_DICT: dict[str | pathlib.Path, Asset] = {
    TEMPLATE_IMAGE_PATH: TEMPLATE_IMAGE_SURF,
    BIG_FONT_PATH: BIG_FONT,
    SMALL_FONT_PATH: SMALL_FONT,
}

from scripts.managers.sound import SoundManager

SOUND_MANAGER: SoundManager

if IS_DISCORD_ALLOWED:
    from scripts.managers.discord import DiscordRPCManager
    DISCORD_MANAGER: DiscordRPCManager

RNG: numpy.random.Generator = numpy.random.default_rng()
