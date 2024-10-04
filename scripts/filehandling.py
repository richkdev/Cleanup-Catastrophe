from json import load, dump, JSONDecodeError
from random import randint

from scripts.settings import mapDirectory, saveFileDirectory


def loadMap() -> list[list[int]]:
    try:
        map = load(open(mapDirectory))
    except JSONDecodeError or FileNotFoundError:
        map = []
    return map


def makeMap(start: int = 4, stop: int = 4) -> list[list[int]]:
    """
    trashType
    0 = empty
    1-3 = not empty
    """
    
    rows, cols = randint(start, stop), randint(start, stop)
    map = [[randint(0, 4) for _ in range(rows)] for _ in range(cols)]
    return map


def saveMap(mapPath: str) -> None:
    dump(mapPath, open(mapDirectory, "w"))


def getLocal() -> list[dict[str, str|int]]:
    try:
        highscores = load(open(saveFileDirectory))
    except JSONDecodeError or FileNotFoundError:
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

    dump(highscores, open(saveFileDirectory, "w"), indent=4)
