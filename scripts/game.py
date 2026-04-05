import pygame
import asyncio
from scripts import globals, utils
from scripts.settings import *
from scripts.sprites.basesprite import RGroup
from scripts.states.states import *
from scripts.sound import SoundManager

if not globals.IS_WEB and not globals.IS_PYGBAG:
    from scripts.discord import DiscordPresence


class Game:
    def __init__(self) -> None:
        # TODO: add other things used in runtime here
        pygame.init()

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)

        pygame.font.init()

    def run(self) -> None:
        self.window_flags = pygame.SCALED | pygame.RESIZABLE
        self.window_flags |= (pygame.OPENGL | pygame.DOUBLEBUF) if globals.FLAG_OPENGL else 0
        self.screen = pygame.display.set_mode(globals.SCREEN_SIZE, self.window_flags, vsync=1)

        if globals.FLAG_OPENGL:
            # TODO: turn renderer into a manager
            from scripts.renderer import ctx, pipeline, screen_texture
            self.ctx = ctx
            self.pipeline = pipeline
            self.screen_texture = screen_texture

        globals.INITIAL_WINDOW_SIZE = pygame.display.get_window_size()
        globals.FPS = max(globals.FPS, *pygame.display.get_desktop_refresh_rates())

        if globals.FLAG_DEBUG:
            print(get_game_data(), pygame.display.Info(), globals.INITIAL_WINDOW_SIZE, globals.SCREEN_SIZE)

        pygame.display.set_caption(f"Cleanup Catastrophe! ({globals.VERSION})")
        pygame.display.set_icon(globals.TEMPLATE_IMAGE_SURF)

        pygame.mouse.set_relative_mode(True) # fixes mouse scaling issue but it makes the mouse invisible
        pygame.mouse.set_visible(True) # so we set the mouse to visible using this func

        self.sprites = RGroup()

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

        if not globals.IS_WEB:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
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

        # temporarily disabled until i figure out how to make it run alongside the main game and non-blocking
        # for state in self.current_state.next_states:
        #     self.prepare_state(state)

    def prepare_state(self, state_id: StateID) -> None:
        self.states[state_id].prepare()

    async def game(self) -> None:
        self.switch_state(StateID.SPLASH)

        while globals.IS_RUNNING:
            self.current_state.update()
            self.render()

            await asyncio.sleep(0 if not globals.IS_PYODIDE else 1/globals.FPS)

        pygame.quit()

    async def discord_stuff(self) -> None:
        self.discord = DiscordPresence()

        while globals.IS_RUNNING:
            try:
                if not self.discord.connected:
                    await self.discord.prepare()
                else:
                    await self.discord.update(self.current_state.desc)

            except Exception as e:
                print(type(e).__name__, e)

            await asyncio.sleep(5)

        self.discord.quit()

    def render(self) -> None:
        globals.WINDOW_SIZE = pygame.display.get_window_size()

        globals.FINAL_SCREEN_SIZE = utils.aspectScale(*globals.SCREEN_SIZE, *globals.WINDOW_SIZE)

        if globals.FLAG_OPENGL:
            self.pipeline.viewport = (
                (globals.WINDOW_SIZE[0]-globals.FINAL_SCREEN_SIZE[0])//2,
                (globals.WINDOW_SIZE[1]-globals.FINAL_SCREEN_SIZE[1])//2,
                *globals.FINAL_SCREEN_SIZE
            )

            self.ctx.new_frame()

            self.screen_texture.clear()
            self.screen_texture.write(data=pygame.image.tobytes(self.screen, 'RGBA', flipped=(not globals.retroMode)), size=globals.SCREEN_SIZE)

            self.pipeline.render()

            pygame.display.flip()
            self.ctx.end_frame()
        else:
            pygame.display.flip()

        self.screen.fill(globals.BLACK)
