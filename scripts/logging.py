from .settings import logDirectory, path, emscripten, datetime
from os import makedirs
from typing import Any


def init_log() -> None:
    if not path.exists(logDirectory):
        makedirs(logDirectory)


def log(*content: Any | str, sep: str = " ") -> None:
    """Make sure that `content` is able to be converted to a string!

    Won't be called if `sys.platform == "emscripten"`"""

    if emscripten:
        return

    current_time = str(datetime.now()).replace(":", "-")
    with open(f"{logDirectory}{current_time}.log", "w+") as f:
        ctnt = "".join([str(c) + sep for c in content])
        f.write(ctnt)
