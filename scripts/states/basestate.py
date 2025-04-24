import pygame
from pygame.locals import *  # type: ignore

from scripts import globals
from scripts.sound import SoundManager


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import Game


class State(object):
    """
    Base class for game states to use.
    """

    def __init__(self, game: "Game", gamemode: bool, desc: str):
        match gamemode:
            case True:
                self.desc = f"In a heck of a {desc.upper()}"
            case False:
                self.desc = desc

        self.game = game
        self.screen: pygame.surface.Surface = game.screen
        self.sprites: pygame.sprite.Group = game.sprites
        self.sound_manager: SoundManager = game.sound_manager
        self.sprites.empty()

        self.mouse = pygame.Vector2()

        print(f"Loaded {type(self).__name__} state, with description: {desc}")

    def update(self):
        self.key = pygame.key.get_pressed()
        self.event = pygame.event.get()

        self.mouse.x, self.mouse.y = pygame.mouse.get_pos()  # will use one day
        print(self.mouse.x, self.mouse.y)

        self.dt = max(0.001, min(globals.clock.tick_busy_loop(globals.FPS)/1000, 0.1))

        self.sprites.update(self.key, self.dt)
        # self.sprites.update(self.key, self.mouse, self.dt)
        self.sprites.draw(self.screen)
