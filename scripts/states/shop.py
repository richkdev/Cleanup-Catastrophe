import pygame

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *
from scripts.sprites.gui import *


class Shop(State):
    is_gamemode = False
    desc = "Lookin\' for things to buy... or not."

    def prepare_assets(self):
        self.assets_raw = []

        self.sounds_raw = {
            "straight-fundamentals": "assets/music/straight-fundamentals.wav"
        }

    def prepare_sprites(self):
        self.buttons_data = [
            {
                "pos": (20, 20),
                "image": common.TEMPLATE_IMAGE_PATH,
                "name": "Plastic fishing rod",
                "desc": "Has 16 durability. Made by yours truly."
            },
            {
                "pos": (50, 20),
                "image": common.TEMPLATE_IMAGE_PATH,
                "name": "Wooden fishing rod",
                "desc": "Has 32 durability. Made by yours truly too."
            },
        ]

        self.buttons = ButtonGroup()
        for data in self.buttons_data:
            b = Button(
                static_image_path=data["image"],
                pos=data["pos"]
            )
            b.set_button(lambda: self.show_shop_item_desc(data["name"], data["desc"]))
            b.callibrate()
            self.buttons.add(b)

        self.modal = TextModal(pos=(0, 0))

    def show_shop_item_desc(self, name: str, desc: str):
        self.modal.move_to((common.SCREEN_WIDTH/2, 8))
        self.modal.heading_text.set_text(name, bg_color=color.WHITE)
        self.modal.desc_text.move_ip((0, 16))
        self.modal.desc_text.set_text(desc, bg_color=color.WHITE)

    def load_sprites(self):
        self.sprites.add(self.buttons, self.modal)

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
