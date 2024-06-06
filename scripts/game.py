import pygame
import asyncio
from scripts.settings import *
from scripts.logging import log, init_log

if not emscripten:
    from scripts.discord import discord

from scripts.states.states import *

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)

if emscripten:
    pygame.mixer.SoundPatch()  # type: ignore


class Game(object):
    def __init__(self):
        if not emscripten:
            flags = HWSURFACE | DOUBLEBUF | SCALED | OPENGLBLIT | RESIZABLE
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, depth=1, display=0, vsync=1)
            from scripts.opengl import ctx, surf_to_texture, render_object
            self.ctx = ctx
            self.surf_to_texture = surf_to_texture
            self.render_object = render_object

            init_log()
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        log(datetime.now(), "test_log", [1, 2, 3, 4, "test", "another one", {1: "a", 2: "b", 3: ...}])  # this is just a test log for demonstration purposes
        print(pygame.display.Info(), pygame.display.get_window_size())

        pygame.display.set_caption(f"Cleanup Catastrophe! {version}")
        pygame.display.set_icon(pygame.image.load(newPath("icon.ico")))

        self.sprites = pygame.sprite.Group()

        asyncio.gather(self.main(), self.discordStatus())
        self.running = True

    async def main(self):
        self.state = Splash(self)

        while self.running:
            self.state.update()
            self.render()
            await asyncio.sleep(0)

    async def discordStatus(self):
        while self.running:
            match discord.connected:
                case False:
                    discord.prepare()
                    discord.update(type(self.state).__name__)
                case True:
                    discord.update(type(self.state).__name__)
            await asyncio.sleep(10)

    def render(self):
        if not emscripten:
            frame_tex = self.surf_to_texture(self.screen)
            frame_tex.use(0)
            self.render_object.render(mode=0x0005)  # aka moderngl.TRIANGLE_STRIP
            frame_tex.release()
            pygame.display.flip()
            self.ctx.clear(0)
        else:
            pygame.display.flip()

        self.screen.fill(BLACK)
