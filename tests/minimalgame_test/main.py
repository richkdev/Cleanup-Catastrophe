# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///

# WIP!!!!!!! havent added test spritegroup things at all!!!

import pygame
import asyncio

class Game(object):
    def __init__(self) -> None:
        self.window = pygame.Window(size=(500, 500), opengl=True, resizable=True)
        self.screen = self.window.get_surface()

        print(pygame.display.Info(), pygame.print_debug_info(), globals.INITIAL_WINDOW_SIZE, globals.SCREEN_SIZE)

        self.sprites = pygame.sprite.Group()

        asyncio.run(self.game())

    async def game(self):
        # fancy sprite stuff here

        while self.running:
            self.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            await asyncio.sleep(0)

        pygame.quit()

    def render(self):
        pygame.display.flip()
        self.window.flip()

        self.screen.fill(pygame.Color(0, 0, 0))

Game()
