import pygame
import asyncio
from scripts import common, utils
from scripts.settings import *
from scripts.sprites.basesprite import RGroup
from scripts.states.states import *
from scripts.sound import SoundManager

if not common.IS_WEB and not common.IS_PYGBAG:
    from scripts.discord import DiscordPresence


class Game:
    def __init__(self) -> None:
        # TODO: add other things used in runtime here
        pygame.init()

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_ES)
        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)

        if not pygame.font.get_init():
            pygame.font.init()

        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(64)

        if common.IS_PYGBAG:
            pygame.mixer.SoundPatch()  # type: ignore -> for web

    def run(self) -> None:
        self.window_flags = pygame.SCALED | pygame.RESIZABLE
        self.window_flags |= (pygame.OPENGL | pygame.DOUBLEBUF) if common.FLAG_OPENGL else 0
        self.screen = pygame.display.set_mode(common.SCREEN_SIZE, self.window_flags, vsync=1)
        self.draw_screen = pygame.Surface(self.screen.size, pygame.SRCALPHA)

        if common.FLAG_OPENGL:
            # TODO: turn renderer into a manager
            from scripts.renderer import ctx, pipeline, screen_texture
            self.ctx = ctx
            self.pipeline = pipeline
            self.screen_texture = screen_texture

        common.INITIAL_WINDOW_SIZE = pygame.display.get_window_size()
        common.FPS = max(common.FPS, *pygame.display.get_desktop_refresh_rates())

        if common.FLAG_DEBUG:
            print(get_game_data(), pygame.display.Info(), common.INITIAL_WINDOW_SIZE, common.SCREEN_SIZE)

        pygame.display.set_caption(f"Cleanup Catastrophe! ({common.VERSION})")
        pygame.display.set_icon(common.TEMPLATE_IMAGE_SURF)

        pygame.mouse.set_relative_mode(True) # fixes mouse scaling issue but it makes the mouse invisible
        pygame.mouse.set_visible(True) # so we set the mouse to visible using this func

        self.sprites = RGroup()

        self.sound_manager = SoundManager()

        self.states: dict[StateID, State] = {
            StateID.SPLASH: Splash(),
            StateID.LOBBY: Lobby(),
            StateID.CATASTROPHE: Catastrophe(),
            StateID.SHOP: Shop(),
            StateID.SCOREBOARD: Scoreboard(),
        }
        self.current_state: State
        self.states_accessed: list[StateID] = []

        if not common.IS_WEB:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(
                    asyncio.wait(
                        [self.loop.create_task(x) for x in [self.game(), self.discord_stuff()]],
                        return_when=asyncio.ALL_COMPLETED,
                    )
                )
            finally:
                self.loop.stop()
                self.loop.close()
        else:
            asyncio.run(self.game())

    def switch_state(self, state_id: StateID) -> None:
        if len(self.states_accessed) != 0:
            self.current_state.unload()

        self.prepare_state(state_id)

        self.current_state = self.states[state_id]

        self.states_accessed.append(state_id)

        self.current_state.load(self.screen, self.draw_screen, self.sprites, self.sound_manager, self.switch_state)

        print(f"Switched to {type(self.current_state).__name__} state, list of states accessed: {self.states_accessed}")

        # temporarily disabled until i figure out how to make it run alongside the main game and non-blocking
        # for state in self.current_state.next_states:
        #     self.prepare_state(state)

    def prepare_state(self, state_id: StateID) -> None:
        self.states[state_id].prepare()

    async def game(self) -> None:
        self.switch_state(StateID.SPLASH)

        while common.IS_RUNNING:
            self.current_state.update()
            self.render()

            await asyncio.sleep(0 if not common.IS_PYODIDE else 1/common.FPS)

        pygame.quit()

    async def discord_stuff(self) -> None:
        self.discord = DiscordPresence()

        while common.IS_RUNNING:
            if not self.discord.connected:
                await self.discord.prepare()
            else:
                await self.discord.update(self.current_state.desc)

            await asyncio.sleep(5)

        await self.discord.quit()

    def render(self) -> None:
        common.WINDOW_SIZE = pygame.display.get_window_size()

        common.FINAL_SCREEN_SIZE = utils.aspectScale(*common.SCREEN_SIZE, *common.WINDOW_SIZE)

        if common.FLAG_OPENGL:
            self.pipeline.viewport = (
                (common.WINDOW_SIZE[0]-common.FINAL_SCREEN_SIZE[0])//2,
                (common.WINDOW_SIZE[1]-common.FINAL_SCREEN_SIZE[1])//2,
                *common.FINAL_SCREEN_SIZE
            )

            self.ctx.new_frame()

            self.screen_texture.clear()
            self.screen_texture.write(data=pygame.image.tobytes(self.screen, 'RGBA', flipped=(not common.retroMode)), size=common.SCREEN_SIZE)

            self.pipeline.render()

            pygame.display.flip()
            self.ctx.end_frame()
        else:
            pygame.display.update()

        self.screen.fill(common.BLACK)
        self.draw_screen.fill(common.TRANSPARENT)
