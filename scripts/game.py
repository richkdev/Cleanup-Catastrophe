import pygame
import asyncio
from scripts import globals, utils
from scripts.settings import *
from scripts.states.states import State, Splash
from scripts.sound import SoundManager

if not globals.emscripten:
    from scripts.discord import discord


class Game(object):
    def __init__(self) -> None:
        flags = pygame.SCALED | pygame.OPENGL | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

        # self.window = pygame.Window(size=globals.SCREEN_SIZE, opengl=True, resizable=True)  # might use later
        # self.screen = self.window.get_surface()

        try:
            self.screen = pygame.display.set_mode(globals.SCREEN_SIZE, flags, vsync=1)
        except pygame.error:
            self.screen = pygame.display.set_mode(globals.SCREEN_SIZE, flags)

        if pygame.OPENGL:
            from scripts.renderer import ctx, pipeline, screen_texture
            self.ctx = ctx
            self.pipeline = pipeline
            self.screen_texture = screen_texture

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)

        pygame.mixer.set_num_channels(64)

        globals.INITIAL_WINDOW_SIZE = pygame.display.get_window_size()
        # globals.INITIAL_WINDOW_SIZE = self.window.size

        print(pygame.display.Info(), globals.INITIAL_WINDOW_SIZE, globals.SCREEN_SIZE)

        pygame.display.set_caption(f"Cleanup Catastrophe! {globals.version}")
        pygame.display.set_icon(pygame.image.load(utils.newPath("icon.ico")))

        self.sprites = pygame.sprite.Group()

        self.sound_manager = SoundManager()
        self.sound_manager.add_sound(
            "cleanup-time", utils.newPath("assets/music/cleanup-time.wav"))
        self.sound_manager.add_sound(
            "getTrash", utils.newPath("assets/sfx/getTrash.wav"))
        self.sound_manager.add_sound(
            "noTrash", utils.newPath("assets/sfx/noTrash.wav"))
        self.sound_manager.add_sound(
            "explode", utils.newPath("assets/sfx/explode.wav"))

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
                # globals.WINDOW_SIZE = self.window.size

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
            # self.window.flip()
            self.ctx.end_frame()
        else:
            pygame.display.flip()
            # self.window.flip()

        self.screen.fill(globals.BLACK)
