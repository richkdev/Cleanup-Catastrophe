import pygame
import json
import pathlib
from scripts.common import ASSET_DICT

def cut_sheet_fixed_size(
    path: pathlib.Path,
    size: pygame.typing.IntPoint
) -> list[pygame.Surface]:
    """
    utility to cut a spritesheet with fixed size into a list of pygame surfs
    """

    frames = []
    sheet_img: pygame.Surface = ASSET_DICT.get(path, pygame.image.load(path).convert_alpha())

    for i in range(int(sheet_img.get_width() / size[0])):
        frames.append(sheet_img.subsurface(pygame.Rect(i * size[0], 0, size[0], size[1])))

    print(f"Loaded and split fixed size spritesheet at {path}")
    return frames


class Sheet:
    def __init__(self) -> None:
        self.states: dict[str, list[pygame.surface.Surface]] = {}
        self.current_state: str
        self.current_idx = 0.0

    def add_animation(self, name: str, sprites: list[pygame.surface.Surface]) -> None:
        self.states[name] = sprites

    def set_animation(self, name: str) -> None:
        if name in self.states:
            self.current_state = name

    def update(self, val: float = 0.1) -> None:
        self.current_idx += val

    def draw(self, flip_x: bool = False, flip_y: bool = False) -> pygame.surface.Surface:
        idx = int(self.current_idx % len(self.states[self.current_state]))
        surf = self.states[self.current_state][idx]
        surf = pygame.transform.flip(surf, flip_x, flip_y)
        return surf


def cut_sheet(
    image_path: pygame.typing._PathLike,
    json_path: pygame.typing._PathLike
) -> Sheet:
    raw_data: list = ASSET_DICT.get(json_path, json.loads(open(json_path).read()))
    sheet = Sheet()
    sheet_img: pygame.Surface = ASSET_DICT.get(image_path, pygame.image.load(image_path).convert_alpha())

    for d in raw_data:
        anim: list[pygame.Surface] = []
        for f in d['frames']:
            anim.append(sheet_img.subsurface(f['bounds']['x'], f['bounds']['y'], f['bounds']['w'], f['bounds']['h']))

        sheet.add_animation(
            d['action'],
            anim
        )

    print(f"Loaded and split dynamic size spritesheet at {image_path} with data from {json_path}")

    sheet.set_animation(raw_data[0].action) # default setting

    return sheet
