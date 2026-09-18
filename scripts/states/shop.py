import pygame

from pygame.locals import *  # type: ignore

from scripts import common, colors, utils, filehandling
from scripts.managers.input import InputStuff

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
        common.SPRITE_MANAGER.add_sprites(StateID.SHOP, "assets/layouts/shop.json")
        self.buttons: ButtonGroup

        self.modal = TextModal(pos=(0, 0))

    def show_shop_item_desc(self, name: str, desc: str):
        self.modal.move_to((common.SCREEN_WIDTH/2, 8))
        self.modal.heading_text.set_text(name, bg_color=colors.WHITE)
        self.modal.desc_text.move_ip((0, 16))
        self.modal.desc_text.set_text(desc, bg_color=colors.WHITE)

    def load_sprites(self):
        self.buttons = common.SPRITE_MANAGER.get_sprites(StateID.SHOP)
        for b in self.buttons:
            b.set_clicks(0)
            b.set_button(
                lambda
                    clicks=b.total_clicks,
                    name=b.data["item_name"],
                    desc=b.data["item_desc"],
                    data=b.data["item_data"],
                    shared_data=self.shared_state_data,
                    func=self.show_shop_item_desc:
                        func(name, desc) if clicks % 2 == 0
                        else shared_data.update({data[0]: data[1]})
                        # TODO: make it so that it doesnt replace the current item's stats n stuff
            )

        self.sprites.add(self.buttons, self.modal)

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("straight-fundamentals", loop=-1)

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        self.buttons.move_cursor_ip(common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_RIGHT) - common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_LEFT))
        self.buttons.move_cursor_ip(5 * (common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_DOWN)))

        for sprite in self.buttons:
            sprite.is_hovered = self.buttons.get_button_at_cursor() == sprite

            if not sprite.is_hovered and sprite.total_clicks != 0:
                sprite.set_clicks(0)

        if common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_CONFIRM):
            self.buttons.click_button_at_cursor()

        if common.INPUT_MANAGER.get_key_jp(InputStuff.ACTION_CANCEL):
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
