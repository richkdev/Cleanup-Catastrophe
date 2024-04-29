import json, sys
from os import path
from pygame.time import Clock

version = open("VERSION").read()

settings = json.loads(open("settings.json").read())

WIDTH = settings["width"]
HEIGHT = settings["height"]

xBorder = WIDTH*0.02
yBorder = HEIGHT*0.02

FPS = settings["fps"]

fragmentShader = settings["fragmentShader"]
vertexShader = settings["vertexShader"]

saveFileDirectory = settings["saveFileDirectory"]

clock = Clock()

from sys import platform
emscripten = platform == "emscripten" # detect if wasm/emscripten

def newPath(relPath: str): # https://pyinstaller.org/en/stable/runtime-information.html
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, relPath) # pyinstaller temp folder
    else:
        return path.join(path.abspath("."), relPath)
