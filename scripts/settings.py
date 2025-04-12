import pygame
import sys
import os
import platform
from scripts import globals

if not getattr(pygame, "IS_CE", False):
    raise ImportError("This game requires pygame-ce 2.5.2 or above to function, not pygame.",
                      "Uninstall pygame then install pygame-ce 2.5.2 or above")

if sys.version_info < (3, 12):
    raise DeprecationWarning("This game requires Python versions 3.12 and above to function.")

print(f"Running on emscripten or nah? {globals.emscripten}\nSupports OpenGL? {pygame.OPENGL}")

print(f"CRT shader on? {globals.retroMode}")

print(platform.platform())

if globals.emscripten:
    platform.window.canvas.style.imageRendering = "pixelated"  # type: ignore -> no more blurriness yay

os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = 'permonitorv2'

# if not os.path.exists(newPath(logDirectory)):
#     os.makedirs(newPath(logDirectory))
# sys.stdout = open(newPath(f"{logDirectory}{current_time}.log"), "w+")
