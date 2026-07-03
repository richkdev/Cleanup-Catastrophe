import pygame
import numpy

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *


class Catastrophe(State):
    is_gamemode = True
    desc = "catastrophe"

    def prepare_assets(self):
        self.assets_raw = [
            "assets/img/bg/",
            "assets/img/sprites/",
        ]

        self.sounds_raw = {
            "waiting": "assets/music/waiting.wav",
            "explode": "assets/sfx/explode.wav",
            "ding": "assets/sfx/ding.wav",
            "noTrash": "assets/sfx/noTrash.wav",
            "reelin": "assets/sfx/reelin.wav",
        }

    def prepare_sprites(self):
        self.score = 0

        self.background = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/waters.png"))

        self.rod = Rod(pos=(common.SCREEN_WIDTH/2, common.Y_BORDER))

        self.textDisplay = Statistic(pos=(5, 10))
        self.textDisplay.set_icon(image_path=utils.newPath("assets/img/ui/clock.png"), pos_ip=(0, 0))
        self.textDisplay.set_text(text="0", pos_ip=(20, 0))

        self.progress = ProgressBar(
            pos=(0, common.SCREEN_HEIGHT-8),
            size=(common.SCREEN_WIDTH, 8)
        )

        self.trashSprites: RGroup[Trash] = RGroup()

        trash_id_map = filehandling.makeMap((4, 8))
        self.start_pos = (common.SCREEN_WIDTH + common.X_BORDER, common.WATER_HEIGHT)
        self.distance_between_trash = (
            common.SCREEN_WIDTH / 10,
            common.SCREEN_HEIGHT / 10
        )

        min_score = self.shared_state_data.get('min_score', None)
        self.minimum_score = min_score if min_score != None else 10

        for row in range(len(trash_id_map)):
            for col in range(len(trash_id_map[0])):
                if trash_id_map[row][col] != 0:
                    t = Trash(
                        pos=(
                            (row * self.distance_between_trash[0] + self.start_pos[0]),
                            (col * self.distance_between_trash[1] + self.start_pos[1])
                        )
                    )
                    t.set_trash(
                        trash_type=trash_id_map[row][col],
                        trash_id=(row, col),
                        offset=16
                    )
                    self.trashSprites.add(t)

    def load_sprites(self):
        self.game_start_time = pygame.time.get_ticks()

        self.sprites.add(
            self.background,
            self.trashSprites,
            # self.collidables, # only show for debug purposes i guess
            self.textDisplay,
            self.progress,
            self.rod
        )

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY,
            StateID.SCOREBOARD,
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("waiting", -1)
        self._persistent_sfx_id = 0

    def logic(self):
        self.progress.set_progress(
            progress=(self.score / self.minimum_score * 100)
        )

        self.textDisplay.set_text(f"{round((pygame.time.get_ticks() - self.game_start_time)/1000)}, {self.score}")

        if not any(not t.is_explosive for t in self.trashSprites) or self.score < 0:
            for i in self.trashSprites:
                i.kill()
                del i
            raise StateSwitch(StateID.SCOREBOARD, {'score': self.score})

        for t in self.trashSprites:
            if t.is_explosive:
                t.velocity.x = -3
            else:
                t.velocity.x = -numpy.random.uniform(4, 12)

            t.velocity.y = numpy.cos(pygame.time.get_ticks() / 100) * 5

            if t.rect.right <= 0:
                t.kill()
                del t

        match self.rod.is_fishing:
            case False:
                if self.key[K_LEFT] and self.rod.rect.left >= common.X_BORDER:
                    self.rod.velocity.x = -50
                elif self.key[K_RIGHT] and self.rod.rect.right <= common.SCREEN_WIDTH:
                    self.rod.velocity.x = +50
                else:
                    self.rod.velocity.x = 0

                if self.key[K_DOWN]:
                    self.rod.move_to((self.rod.pos.x, self.rod.old_pos.y))
                    print("fishing!")
                    self.rod.is_fishing = True
                    self.rod.velocity.y = 50
                    self.sprites.add(self.rod)
                    self._persistent_sfx_id = common.SOUND_MANAGER.sfx.play("reelin", loop=-1, max_time=4000)

                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                self.rod.velocity.x = 0

                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
                    if isinstance(collided, Trash):
                        self.rod.durability -= 1
                        common.SOUND_MANAGER.sfx.stop_sfx(self._persistent_sfx_id)
                        match collided.is_explosive:
                            case True:
                                self.score -= int(self.score*0.05)
                                common.SOUND_MANAGER.sfx.play("explode")
                            case False:
                                self.score += 1
                                common.SOUND_MANAGER.sfx.play("ding")
                        print(f"Session score: {self.score}, durability: {self.rod.durability}")
                        collided.kill()
                        del collided
                        self.rod.is_fishing = False
                        self.rod.velocity.y = 0
                        self.rod.move_to((self.rod.pos.x, self.rod.old_pos.y))

                if self.rod.rect.centery >= common.SCREEN_HEIGHT:
                    self.rod.is_fishing = False
                    self.rod.velocity.y = 0
                    self.rod.move_to((self.rod.pos.x, self.rod.old_pos.y))
                    common.SOUND_MANAGER.sfx.play("noTrash")

        pygame.draw.line(
            self.draw_screen, color.DARKRED,
            (self.rod.rect.centerx, 0),
            (self.rod.rect.centerx, self.rod.pos.y),
            1
        )

        if self.key[K_ESCAPE]:
            self.rod.kill()
            raise StateSwitch(StateID.LOBBY)
