import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *


class State(object):
    def __init__(self, game):
        self.game = game
        self.screen: pygame.surface.Surface = game.screen
        self.sprites: pygame.sprite.Group = game.sprites
        self.sprites.empty()

        print(f"Loaded {type(self).__name__} state")

    def update(self):
        self.key = pygame.key.get_pressed()
        self.dt = clock.tick_busy_loop(FPS)/1000

        self.sprites.update(self.key, self.dt)
        self.sprites.draw(self.screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
