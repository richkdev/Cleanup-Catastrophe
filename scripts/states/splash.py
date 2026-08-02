import pygame

from pygame.locals import *  # type: ignore

from scripts import common, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *
from scripts.sprites.gui import *


class Splash(State):
    is_gamemode = False
    desc = "At the splash screen..."

    def prepare_assets(self):
        self.assets_raw = [
            "assets/img/ui/logo.png",
        ]

        self.sounds_raw = {
            "cleanup-time": "assets/music/cleanup-time.wav",
        }

    def prepare_sprites(self):
        self.introText = Text()
        self.introText.set_text(
            text=f"press [ENTER] to begin",
            color=color.WHITE,
            font=common.BIG_FONT,
            antialiased=False,
            align=pygame.FONT_CENTER
        )
        self.introText.move_to(((common.SCREEN_WIDTH-self.introText.size[0])/2, common.SCREEN_HEIGHT/1.25))

        self.logo = MenuLogo()
        self.logo.move_to(((common.SCREEN_WIDTH-self.logo.size[0])/2, (common.SCREEN_HEIGHT-self.logo.size[1])/2))

    def load_sprites(self):
        self.sprites.add(
            self.logo,
            self.introText
        )

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("cleanup-time", -1)

    def logic(self):
        if self.key[K_RETURN] or self.key[K_SPACE]:
            raise StateSwitch(StateID.LOBBY)
