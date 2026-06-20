import pygame
import random
import numpy

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *


class Shop(State):
    is_gamemode = False
    desc = "Lookin\' for things to buy... or not."

    def prepare_assets(self):
        self.assets_raw = []

        self.sounds_raw = {
            "straight-fundamentals": "assets/music/straight-fundamentals.wav"
        }

    def prepare_sprites(self):
        text = "SHOP"
        text_sprite = Text()
        text_sprite.set_text(
            text=text,
            color=color.WHITE,
            font=common.BIG_FONT
        )
        text_sprite.velocity.x = 5

        self.buttons = ButtonGroup()
        for y in range(3):
            for x in range(5):
                b = Button(pos=(20 + x*50, 50 + y*50))
                b.set_text(
                    text=f"btn",
                    font=common.SMALL_FONT,
                    bg_color=color.YELLOW,
                )
                b.set_button()
                self.buttons.add(b)

        self.sprites.add(self.buttons)

        self.sprites.add(text_sprite)

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("straight-fundamentals", loop=-1)

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        self.buttons.move_cursor_ip(self.key_jp[K_RIGHT] - self.key_jp[K_LEFT])
        self.buttons.move_cursor_ip(5 * (self.key_jp[K_DOWN] - self.key_jp[K_UP]))

        for sprite in self.buttons:
            sprite.is_hovered = self.buttons.get_button_at_cursor() == sprite

        if self.key_jp[K_RETURN]:
            self.buttons.click_button_at_cursor()

        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
