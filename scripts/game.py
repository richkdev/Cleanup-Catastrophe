import pygame
import asyncio
from scripts.settings import *
from scripts.states.states import *
from scripts.sound import SoundManager

if not emscripten:
    from scripts.discord import discord


class Game(object):
    def __init__(self) -> None:
        if not emscripten:
            flags = HWSURFACE | DOUBLEBUF | SCALED | OPENGLBLIT | RESIZABLE
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, depth=1, display=0, vsync=1)
            from scripts.opengl import ctx, surf_to_texture, render_object
            self.ctx = ctx
            self.surf_to_texture = surf_to_texture
            self.render_object = render_object
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=1, display=0, vsync=0)

        pygame.mixer.set_num_channels(64)

        print(pygame.display.Info())
        print(pygame.display.get_window_size())

        pygame.display.set_caption(f"Cleanup Catastrophe! {version}")
        pygame.display.set_icon(pygame.image.load(newPath("icon.ico")))

        self.sprites = pygame.sprite.Group()

        self.sound_manager = SoundManager()
        self.sound_manager.add_sound(
            "cleanup-time", newPath("assets/music/cleanup-time.wav"))
        self.sound_manager.add_sound(
            "getTrash", newPath("assets/sfx/getTrash.wav"))
        self.sound_manager.add_sound(
            "noTrash", newPath("assets/sfx/noTrash.wav"))
        self.sound_manager.add_sound(
            "explode", newPath("assets/sfx/explode.wav"))

        self.running = True

        if not emscripten:
            self.loop = asyncio.get_event_loop()
            try:
                self.loop.run_until_complete(self.main())
            finally:
                self.loop.close()
        else:
            asyncio.run(self.main())

    async def main(self):
        if not emscripten:
            await asyncio.gather(self.game(), self.discord_stuff())
        else:
            asyncio.run(self.game())

    async def game(self):
        self.state = Splash(self)

        while self.running:
            self.state.update()
            self.render()
            self.sound_manager.update()  # 24-06-06 hulahhh: putting this here since its always tied to the game and not to individual states. Every state has a link to this class so it should work fine.

            self.event = pygame.event.get()

            for event in self.event:
                if event.type == QUIT:
                    pygame.quit()
                    self.running = False
                    break

            await asyncio.sleep(0)

    async def discord_stuff(self):
        while self.running:
            match discord.connected:
                case False:
                    discord.prepare()
                    discord.update(type(self.state).__name__)
                case True:
                    discord.update(type(self.state).__name__)
            await asyncio.sleep(0)

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
