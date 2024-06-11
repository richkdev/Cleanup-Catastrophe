import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *
from scripts.sound import SoundManager


# this will always be false at runtime. with this "hack" you can have typehints on the game parameter now.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game


class State(object):
    def __init__(self, game: "Game"):
        self.game = game
        self.screen: pygame.surface.Surface = game.screen
        self.sprites: pygame.sprite.Group = game.sprites
        self.sound_manager: SoundManager = game.sound_manager
        self.sprites.empty()

        print(f"Loaded {type(self).__name__} state")

    def update(self):
        self.key = pygame.key.get_pressed()
        self.key_just_pressed = pygame.key.get_just_pressed()
        self.dt = clock.tick_busy_loop(FPS) / 1000

        self.sprites.update(self.key, self.dt)
        self.sprites.draw(self.screen)
