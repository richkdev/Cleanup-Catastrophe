import pygame

from pygame.locals import *  # type: ignore

from scripts import common, colors, utils, filehandling
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *
from scripts.sprites.gui import *


class Scoreboard(State):
    is_gamemode = False
    desc = "Lookin\' at the scoreboard."

    def prepare_assets(self):
        self.assets_raw = [
            "savefiles/"
        ]

        self.sounds_raw = {
            "wake-up-call": "assets/music/pause.wav"
        }

    def prepare_sprites(self):
        self.text_input_place: str = ""

        self.text_input = TextInput()

    def load_sprites(self):
        self.sprites.add(self.text_input)

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("wake-up-call")

    def logic(self):
        if self.key_jp[K_RETURN] and not self.text_input.can_input:
            self.text_input.set_input_mode(True)

        if self.text_input.can_input:
            for event in self.event:
                if event.type == pygame.TEXTINPUT:
                    self.text_input_place += event.text
                if event.type == pygame.TEXTEDITING:
                    temp = list(self.text_input_place)
                    temp[event.start:(event.start+event.length)] = event.text
                    self.text_input_place = "".join(temp)

            if self.key_jp[K_RETURN] and len(self.text_input_place) > 0:
                self.text_input.confirm()
                filehandling.set_local_score(self.text_input_place, int(self.shared_state_data.get('score', 0)))
                self.text_input_place = filehandling.get_local_scores()

        self.text_input.set_text(self.text_input_place, color=colors.WHITE)

        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
