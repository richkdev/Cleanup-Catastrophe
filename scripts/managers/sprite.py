import pygame
import json

from scripts import common, utils

from scripts.managers.basemanager import BaseManager
from scripts.states.basestate import StateID
from scripts.sprites.sprites import RSprite, RGroup
from scripts.sprites.gui import GUISprite, Text, GUIGroup

_Sprite = RSprite | GUISprite
_Group = RGroup | GUIGroup

_T_Sprite = type[RSprite] | type[GUISprite]
_T_Group = type[RGroup] | type[GUIGroup]

SPRITE_NAME_DICT: dict[str, _T_Sprite] = {RSprite.__name__: RSprite}
for thing in RSprite.__subclasses__() + GUISprite.__subclasses__() + Text.__subclasses__():
    SPRITE_NAME_DICT.update({thing.__name__: thing})

GROUP_NAME_DICT: dict[str, _T_Group] = {RGroup.__name__: RGroup}
for thing in RGroup.__subclasses__() + GUIGroup.__subclasses__():
    GROUP_NAME_DICT.update({thing.__name__: thing})


def parse_sprite(sprite_data: dict) -> _Sprite:
    sprite_type = SPRITE_NAME_DICT.get(str(sprite_data.get('type', "RSprite")), RSprite)
    sprite = sprite_type(
        static_image_path=sprite_data.get('static_image_path'),
        sheet_path=sprite_data.get('sheet_path'),
        size=sprite_data.get('size', (1, 1)),
        pos=sprite_data.get('pos', (0, 0))
    )

    try:
        del sprite_data['type']
        del sprite_data['static_image_path']
        del sprite_data['sheet_path']
        del sprite_data['size']
        del sprite_data['pos']
    except KeyError:
        pass

    for name, val in sprite_data.items():
        sprite.set_data(name, val)

    return sprite


def parse_group(group_data: dict) -> _Group:
    group_type = GROUP_NAME_DICT.get(str(group_data.get('type', "RGroup")), RGroup)
    group = group_type(*[parse_sprite(sprite_data) for sprite_data in group_data.get('sprites', [])])

    return group


def parse_data(data: dict) -> _Group:
    data_type = data.get('type')

    if data_type in GROUP_NAME_DICT.keys():
        return parse_group(data)
    elif data_type in SPRITE_NAME_DICT.keys():
        return RGroup(parse_sprite(data))
    else:
        raise KeyError(f"invalid sprite/group data, received {data_type}")


class SpriteManager(BaseManager):
    """
    manager for automatically creating sprites (based on the sprite's class name) & place them based on parsed json data to be loaded for a state (based on state id)
    """

    def __init__(self):
        self.sprites: dict[StateID, _Group] = {}

    def get_sprites(self, state_id: StateID) -> _Group:
        return self.sprites[state_id]

    def remove_sprite(self, state_id: StateID, sprite: _Sprite):
        self.sprites[state_id].remove(sprite)

    def add_sprites(self, state_id: StateID, json_path: pygame.typing._PathLike) -> None:
        path = utils.newPath(json_path)
        data: dict = common.ASSET_DICT.get(path, json.loads(open(path).read())) # type: ignore

        self.sprites[state_id] = parse_data(data) # TODO

    def remove_sprites(self, state_id: StateID):
        self.sprites[state_id].kill()

    def quit(self) -> None:
        for state_id in self.sprites.keys():
            self.sprites[state_id].kill()
