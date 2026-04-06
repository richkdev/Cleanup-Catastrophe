import pygame
import random
import os

from json import load, dump

from scripts.globals import saveFiles_path

if not saveFiles_path.exists():
    try:
        os.mkdir(saveFiles_path.parent)
    except FileExistsError:
        pass


def makeMap(size: pygame.typing.IntPoint = (4, 4)) -> list[list[int]]:
    """
    trashType
    0 = empty
    1-3 = not empty
    """

    map = [[random.randint(0, 4) for _ in range(size[0])] for _ in range(size[1])]
    return map


def getLocal() -> list[dict[str, str|int]]:
    try:
        highscores = load(open(saveFiles_path))
    except FileNotFoundError:
        highscores = []
    return highscores


def saveLocal(name: str, score: int) -> None:
    highscores = getLocal()

    player_exists = False
    for i in highscores:
        if str(i['name']) == name:
            if int(i['score']) <= score:
                i['score'] = score
            player_exists = True
            if not player_exists:
                highscores.append({"name": name, "score": score})

    dump(highscores, open(saveFiles_path, "w"), indent=4)
