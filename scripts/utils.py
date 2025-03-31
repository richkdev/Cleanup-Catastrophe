import sys
import os
from scripts import globals

def newPath(relPath: str):
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    elif globals.emscripten and globals.pyodide:
        basePath = currentURL # type: ignore -> currentURL is set by pyodide
    else:
        basePath = os.path.abspath('.')
    return os.path.join(basePath, relPath)


def aspectScale(image_x, image_y, target_x, target_y):
    # very slightly modified version of https://www.pygame.org/pcr/transform_scale/

    if image_x > image_y:
        # fit to width
        scale_factor = target_x/image_x
        scaled_y = scale_factor * image_y
        if scaled_y > target_y:
            scale_factor = target_y/image_y
            scaled_x = scale_factor * image_x
            scaled_y = target_y
        else:
            scaled_x = target_x
    else:
        # fit to height
        scale_factor = target_y/image_y
        scaled_x = scale_factor * image_x
        if scaled_x > target_x:
            scale_factor = target_x/image_x
            scaled_x = target_x
            scaled_y = scale_factor * image_y
        else:
            scaled_y = target_y

    del scale_factor

    scaled_x = int(scaled_x)
    scaled_y = int(scaled_y)

    return scaled_x, scaled_y
