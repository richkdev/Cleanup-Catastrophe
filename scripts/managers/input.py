import pygame
import pathlib
import enum
import json

from scripts import common, utils
from scripts.managers.basemanager import BaseManager

@enum.unique
class InputStuff(enum.StrEnum):
    ACTION_CONFIRM = enum.auto()
    ACTION_CANCEL = enum.auto()

    ACTION_LEFT = enum.auto()
    ACTION_RIGHT = enum.auto()
    ACTION_UP = enum.auto()
    ACTION_DOWN = enum.auto()


def parse_scancode(name: str) -> int:
    """
    NOTE: name is case sensitive!
    """

    return int(vars(pygame.constants).get(name, pygame.K_RETURN))


class InputManager(BaseManager):
    """
    manager for simplifying mapping input. converts scancode wrapper to a
    """

    def __init__(self):
        self.input_map: dict[InputStuff, list[int]] = {}

        self.events: list[pygame.Event] = []
        self.key: pygame.key.ScancodeWrapper
        self.key_jp: pygame.key.ScancodeWrapper
        self.mouse: pygame.Vector2 = pygame.Vector2()
        self.mouse_rel: pygame.Vector2 = pygame.Vector2()

        self.joysticks: list[pygame.joystick.JoystickType] = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def load_input_map(self, json_path: pathlib.Path):
        path = utils.newPath(str(json_path))
        data: dict[str, list[str]] = common.ASSET_DICT.get(path, json.loads(open(path).read())) # type: ignore

        for input_name, scancodes in data.items():
            self.input_map.update({InputStuff(input_name.lower()): [parse_scancode(c) for c in scancodes]})

    def update(self):
        self.events = pygame.event.get()
        self.key = pygame.key.get_pressed()
        self.key_jp = pygame.key.get_just_pressed()
        self.mouse.x, self.mouse.y = pygame.mouse.get_pos(False)
        self.mouse_rel.x, self.mouse_rel.y = pygame.mouse.get_rel()

    def get_input_map(self) -> dict[InputStuff, list[int]]:
        return self.input_map

    def get_event(self) -> list[pygame.Event]:
        return self.events

    def get_key(self, name: InputStuff) -> bool:
        return any(self.key[key] for key in self.input_map[name])

    def get_key_jp(self, name: InputStuff) -> bool:
        return any(self.key_jp[key] for key in self.input_map[name])

    def get_mouse(self) -> pygame.Vector2:
        return self.mouse

    def get_mouse_rel(self) -> pygame.Vector2:
        return self.mouse_rel

    def quit(self):
        ...
