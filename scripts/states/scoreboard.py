import pygame

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *


class Scoreboard(State):
    is_gamemode = False
    desc = "Lookin\' at the scoreboard."

    def prepare_sprites(self):
        filehandling.saveLocal("guy", int(self.shared_state_data.get('score', 0)))
        highscores = filehandling.getLocal()
        text = ""

        for i in highscores:
            text += f"{(i['name'])}: {i['score']}\n"

        text += "end."

        self.text = Text()
        self.text.set_text(
            text=text,
            color=color.WHITE,
            font=common.SMALL_FONT,
            align=pygame.FONT_CENTER
        )

    def load_sprites(self):
        self.sprites.add(self.text)

    def prepare_assets(self):
        self.assets_raw = [
            "savefiles/"
        ]

        self.sounds_raw = {
            "wake-up-call": "assets/music/pause.wav"
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("wake-up-call")

    def logic(self):
        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
