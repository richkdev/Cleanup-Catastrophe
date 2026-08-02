import pygame

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
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
        self.surf = pygame.surfarray.make_surface(self.arr[..., None] * color.CYAN[:3])
        self.surf.fill(color.BLUE, special_flags=pygame.BLEND_ADD)
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

        if not self.mouse_rel:
            self.cursor.move_ip((
                (self.key[K_RIGHT] - self.key[K_LEFT]) * 1,
                (self.key[K_DOWN] - self.key[K_UP]) * 1,
            ))
        else:
            self.cursor.move_ip(self.mouse_rel/2)

        pygame.mouse.set_pos(self.cursor.pos)

        if self.key_jp[K_RETURN]:
            self.shared_state_data.update(
                {"seed": self.surf.subsurface((*self.cursor.pos, 1, 1))}
            )
            raise StateSwitch(StateID.CATASTROPHE, self.shared_state_data)

        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
