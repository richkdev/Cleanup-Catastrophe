import pygame
import asyncio
from scripts import globals, utils
from scripts.settings import *
from scripts.states.states import State, Splash
from scripts.sound import SoundManager

if not globals.emscripten:
    from scripts.discord import discord


class Game(object):
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

        self.window_flags = pygame.SCALED | pygame.OPENGL | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

        self.screen = pygame.display.set_mode(globals.SCREEN_SIZE, self.window_flags)

        if pygame.OPENGL:
            from scripts.renderer import ctx, pipeline, screen_texture
            self.ctx = ctx
            self.pipeline = pipeline
            self.screen_texture = screen_texture

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)

        globals.INITIAL_WINDOW_SIZE = self.screen.size

        print(pygame.display.Info(), pygame.print_debug_info(), globals.INITIAL_WINDOW_SIZE, globals.SCREEN_SIZE)

        pygame.display.set_caption(f"Cleanup Catastrophe! {globals.version}")
        pygame.display.set_icon(pygame.image.load(utils.newPath("icon.ico")))

        if pygame.OPENGL:
            pygame.mouse.set_relative_mode(True) # fixes mouse opengl scaling issue but it makes the mouse invisible
            pygame.mouse.set_visible(True) # so we set the mouse to visible using this func

        self.sprites = pygame.sprite.Group()

        self.sounds_lol = [
            ["cleanup-time", "assets/music/cleanup-time.wav"],
            ["getTrash", "assets/music/cleanup-time.wav"],
            ["noTrash", "assets/music/cleanup-time.wav"],
            ["explode", "assets/music/cleanup-time.wav"],
        ]
        self.sound_manager = SoundManager()
        for title, old_path in self.sounds_lol:
            self.sound_manager.add_sound(title, utils.newPath(old_path))
        del self.sounds_lol

        self.music_sound_id = 0
        self.running = True
        self.state: State

        if not globals.emscripten:
            self.loop = asyncio.get_event_loop()
            try:
                self.loop.run_until_complete(
                    asyncio.gather(self.game(), self.discord_stuff())
                )
            finally:
                self.loop.close()
        else:
            asyncio.run(self.game())

    async def game(self):
        self.state = Splash(self)

        while self.running:
            self.state.update()
            self.render()
            self.sound_manager.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            await asyncio.sleep(0)

        pygame.quit()

    async def discord_stuff(self):
        while self.running:
            try:
                match discord.connected:
                    case False:
                        discord.prepare()
                    case True:
                        discord.update(self.state.desc)
            except Exception as e:
                print(type(e).__name__, e)
            await asyncio.sleep(1)

    def render(self):
        if pygame.OPENGL:
            if not globals.emscripten:
                globals.WINDOW_SIZE = pygame.display.get_window_size()

                globals.FINAL_WINDOW_SIZE = utils.aspectScale(*globals.SCREEN_SIZE, *globals.WINDOW_SIZE)
                self.pipeline.viewport = (0, 0, *globals.FINAL_WINDOW_SIZE)
            else:
                self.pipeline.viewport = (0, 0, *globals.SCREEN_SIZE)

            self.ctx.new_frame()
            self.screen_texture.clear()

            if globals.retroMode:
                self.screen_texture.write(data=pygame.image.tobytes(self.screen, 'RGBA', flipped=False), size=globals.SCREEN_SIZE)
            else:
                self.screen_texture.write(data=pygame.image.tobytes(self.screen, 'RGBA', flipped=True), size=globals.SCREEN_SIZE)

            self.pipeline.render()

            pygame.display.flip()
            self.ctx.end_frame()
        else:
            pygame.display.flip()

        self.screen.fill(globals.BLACK)
