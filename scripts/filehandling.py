import pygame
import random
import os

from enum import IntEnum, auto
from json import loads, dump

from scripts.common import saveFiles_path


class TrashType(IntEnum):
    EMPTY = 0
    TRASH_BAG = 1
    SNACK_BAG = 2
    PLASTIC_BAG = 3
    BOMB = auto()


if not saveFiles_path.exists():
    try:
        os.mkdir(saveFiles_path.parent)
        with open(saveFiles_path, "w") as f:
            f.write("[]")
    except FileExistsError:
        pass


def makeMap(size: pygame.typing.IntPoint = (4, 4)) -> list[list[TrashType]]:
    map = [[TrashType(random.choice(list(TrashType))) for _ in range(size[0])] for _ in range(size[1])]
    return map


def getLocal() -> list[dict[str, str|int]]:
    try:
        highscores: list[dict[str, str|int]] = loads(open(saveFiles_path).read())
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
