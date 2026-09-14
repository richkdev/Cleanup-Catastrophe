import pygame
import os

from json import loads, dump

from scripts.sprites.trash import TrashType
from scripts.common import RNG, saveFiles_path


if not saveFiles_path.exists():
    try:
        os.mkdir(saveFiles_path.parent)
        with open(saveFiles_path, "w") as f:
            f.write("[]")
    except FileExistsError:
        pass


def make_trashmap(size: pygame.typing.IntPoint = (4, 4)) -> list[list[TrashType]]:
    map = [[TrashType(RNG.choice(list(TrashType))) for _ in range(size[0])] for _ in range(size[1])]
    return map


def get_local_scores_json() -> list[dict[str, str|int]]:
    try:
        highscores: list[dict[str, str|int]] = loads(open(saveFiles_path).read())
    except FileNotFoundError:
        highscores = []
    return highscores


def get_local_scores() -> str:
    highscores = get_local_scores_json()
    text = ""

    for i in highscores:
        text += f"{(i['name'])}: {i['score']}\n"

    text += "end."
    return text


def set_local_score(name: str, score: int) -> None:
    highscores = get_local_scores_json()

    player_exists = False
    for i in highscores:
        if str(i['name']) == name:
            if int(i['score']) < score:
                i['score'] = score
            player_exists = True
            if not player_exists:
                highscores.append({"name": name, "score": score})

    dump(highscores, open(saveFiles_path, "w"), indent=4)
