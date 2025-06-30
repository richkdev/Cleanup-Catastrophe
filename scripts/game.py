import pygame
import asyncio
from scripts import globals, utils
from scripts.settings import *
from scripts.states.states import *
from scripts.sound import SoundManager

if not globals.emscripten:
    from scripts.discord import DiscordPresence


class Game:
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug

    def run(self) -> None:
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

        self.sound_manager = SoundManager()
        self.sound_manager.global_volume = globals.volume

        self.states: dict[StateID, State] = {
            StateID.SPLASH: Splash(False, "At the splash screen..."),
            StateID.LOBBY: Lobby(False, "At the lobby..."),
            StateID.CATASTROPHE: Catastrophe(True),
            StateID.SHOP: Shop(False, "Lookin\' for things to buy... or not."),
            StateID.SCOREBOARD: Scoreboard(False, "Lookin\' at the scoreboard"),
        }
        self.current_state: State
        self.states_accessed: list[StateID] = []

        if not globals.emscripten:
            self.discord = DiscordPresence()

        self.running: bool = True

        if not globals.emscripten:
            self.loop = asyncio.get_event_loop()
            try:
                self.loop.run_until_complete(
                    asyncio.gather(self.game(), self.discord_stuff(), return_exceptions=True)
                )
            finally:
                self.loop.close()
        else:
            asyncio.run(self.game())

    def switch_state(self, state_id: StateID) -> None:
        if len(self.states_accessed) != 0:
            self.current_state.unload()

        self.prepare_state(state_id)

        self.current_state = self.states[state_id]

        self.states_accessed.append(state_id)

        self.current_state.load(self.screen, self.sprites, self.sound_manager, self.switch_state)

        print(f"Switched to {type(self.current_state).__name__} state, list of states accessed: {self.states_accessed}")

        for state in self.current_state.next_states:
            self.prepare_state(state)

    def prepare_state(self, state_id: StateID) -> None:
        self.states[state_id].prepare()

    async def game(self) -> None:
        self.switch_state(StateID.SPLASH)

        while self.running:
            self.current_state.update()
            self.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            await asyncio.sleep(0)

        pygame.quit()

    async def discord_stuff(self) -> None:
        while self.running:
            try:
                match self.discord.connected:
                    case False:
                        await self.discord.prepare()
                    case True:
                        await self.discord.update(self.current_state.desc)
            except Exception as e:
                print(type(e).__name__, e)

            await asyncio.sleep(5)

        self.discord.quit()

    def render(self) -> None:
        if pygame.OPENGL:
            if not globals.emscripten:
                globals.WINDOW_SIZE = pygame.display.get_window_size()

                globals.FINAL_WINDOW_SIZE = utils.aspectScale(*globals.SCREEN_SIZE, *globals.WINDOW_SIZE)
                self.pipeline.viewport = ((globals.WINDOW_SIZE[0]-globals.FINAL_WINDOW_SIZE[0])//2, 0, *globals.FINAL_WINDOW_SIZE)
            else:
                self.pipeline.viewport = (0, 0, *globals.SCREEN_SIZE)

            self.ctx.new_frame()
            self.screen_texture.clear()

            self.screen_texture.write(data=pygame.image.tobytes(self.screen, 'RGBA', flipped=(not globals.retroMode)), size=globals.SCREEN_SIZE)

            self.pipeline.render()

            pygame.display.flip()
            self.ctx.end_frame()
        else:
            pygame.display.flip()

        self.screen.fill(globals.BLACK)
