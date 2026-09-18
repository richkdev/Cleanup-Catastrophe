import pygame

from pygame.locals import *  # type: ignore

from scripts import common, colors, utils, filehandling
from scripts.managers.input import InputStuff

from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.gui import *


class OceanMap(State):
    is_gamemode = False
    desc = "Choosing for a place to fish"

    def prepare_assets(self):
        self.assets_raw = []

        self.sounds_raw = {
            "bliss": "assets/music/bliss.wav"
        }

    def prepare_sprites(self):
        self.arr = common.RNG.uniform(0.5, 1, (common.SCREEN_WIDTH//2, common.SCREEN_HEIGHT//2))
        self.surf = pygame.surfarray.make_surface(self.arr[..., None] * colors.CYAN[:3])
        self.surf.fill(colors.BLUE, special_flags=pygame.BLEND_ADD)
        self.surf = pygame.transform.smoothscale_by(pygame.transform.smoothscale_by(self.surf, 0.4), 2.5)
        self.surf = pygame.transform.scale_by(self.surf, 2)

        self.cursor = RCursor()
        self.cursor.set_cursor()

    def load_sprites(self):
        self.sprites.add(self.cursor)

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("bliss", loop=-1)

    def prepare_next_states(self):
        self.is_reloadable = False
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        self.screen.blit(self.surf)

        rel = common.INPUT_MANAGER.get_mouse_rel()
        if not rel:
            self.cursor.move_ip((
                (common.INPUT_MANAGER.get_key(InputStuff.ACTION_RIGHT) - common.INPUT_MANAGER.get_key(InputStuff.ACTION_LEFT)) * 1,
                (common.INPUT_MANAGER.get_key(InputStuff.ACTION_DOWN) - common.INPUT_MANAGER.get_key(InputStuff.ACTION_UP)) * 1,
            ))
        else:
            self.cursor.move_ip(rel/2)

        pygame.mouse.set_pos(self.cursor.pos)

        if common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_CONFIRM):
            self.shared_state_data.update(
                {"seed": hash(self.surf.get_at(self.cursor.pos).hex)}
            )
            raise StateSwitch(StateID.CATASTROPHE, self.shared_state_data)

        if common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_CANCEL):
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
