import pygame
import random
import numpy

from pygame.locals import *  # type: ignore

from scripts import common, utils, filehandling, color
from scripts.states.basestate import State, StateID, StateSwitch
from scripts.sprites.sprites import *


class Splash(State):
    is_gamemode = False
    desc = "At the splash screen..."

    def prepare_assets(self):
        self.assets_raw = [
            "assets/img/ui/logo.png",
        ]

        self.sounds_raw = {
            "cleanup-time": "assets/music/cleanup-time.wav",
        }

    def prepare_sprites(self):
        self.introText = Text()
        self.introText.set_text(
            text=f"press [ENTER] to begin",
            color=color.WHITE,
            font=common.BIG_FONT,
            antialiased=False,
            align=pygame.FONT_CENTER
        )
        self.introText.move_to(((common.SCREEN_WIDTH-self.introText.size[0])/2, common.SCREEN_HEIGHT/1.25))

        self.logo = MenuLogo()
        self.logo.move_to(((common.SCREEN_WIDTH-self.logo.size[0])/2, (common.SCREEN_HEIGHT-self.logo.size[1])/2))

        self.sprites.add(
            self.logo,
            self.introText
        )

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("cleanup-time", -1)

    def logic(self):
        if self.key[K_RETURN] or self.key[K_SPACE]:
            raise StateSwitch(StateID.LOBBY)


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
            "getTrash": "assets/sfx/getTrash.wav",
            "noTrash": "assets/sfx/noTrash.wav",
        }

    def prepare_sprites(self):
        self.score = 0

        self.background = Background()

        self.temp_ground = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/sand.png"),
            pos=(0, common.WATER_HEIGHT),
            size=(common.SCREEN_WIDTH, 1),
        )
        self.temp_ground.set_worldobj(
            desc="ground",
            interactable=False,
            collidable=True
        )
        self.temp_ground.image = utils.multiply_image(
            input_image=self.temp_ground.image,
            tile_size=(1, 1),
            target_size=(common.SCREEN_WIDTH, 1)
        )
        self.temp_ground.callibrate()

        self.collidables = RGroup(self.temp_ground)

        self.player = Player(
            pos=(0, common.WATER_HEIGHT - 50),
        )
        self.player.set_collidables(self.collidables)

        self.rod = Rod(pos=(-100, -100))

        self.textDisplay = Statistic(pos=(5, 10))
        self.textDisplay.set_icon(image_path=utils.newPath("assets/img/ui/clock.png"), pos_ip=(0, 0))
        self.textDisplay.set_text(text="0", pos_ip=(20, 0))

        self.trashSprites: RGroup[Trash] = RGroup()

        trash_id_map = filehandling.makeMap((4, 8))
        self.start_pos = (common.SCREEN_WIDTH + common.X_BORDER, common.WATER_HEIGHT + common.Y_BORDER)
        self.distance_between_trash = (
            common.SCREEN_WIDTH * len(trash_id_map[0]) / 30,
            common.SCREEN_HEIGHT * len(trash_id_map) / 150
        )

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
                        offset=10
                    )
                    self.trashSprites.add(t)

    def load_sprites(self):
        self.game_start_time = pygame.time.get_ticks()

        self.sprites.add(
            self.background,
            self.trashSprites,
            # self.collidables, # only show for debug purposes i guess
            self.player,
            self.textDisplay,
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

    def logic(self):
        self.textDisplay.set_text(f"{round((pygame.time.get_ticks() - self.game_start_time)/1000)}, {len(self.trashSprites)}")

        if not any(t.is_explosive for t in self.trashSprites) or self.score < 0:
            for i in self.trashSprites:
                i.kill()
                del i
            raise StateSwitch(StateID.SCOREBOARD, {'score': self.score})

        for t in self.trashSprites:
            if t.is_explosive:
                t.velocity.x = -3
            else:
                t.velocity.x = -numpy.random.uniform(4, 12)

            t.velocity.y = numpy.cos(pygame.time.get_ticks() / 100) * numpy.random.uniform(-5, 5)

            if t.rect.right <= 0:
                t.kill()
                del t

        match self.rod.is_fishing:
            case False:
                if self.key[K_LEFT] and self.player.rect.x >= common.X_BORDER:
                    self.player.velocity.x = -50
                elif self.key[K_RIGHT] and self.player.rect.x <= (common.SCREEN_WIDTH - self.player.rect.width - common.X_BORDER):
                    self.player.velocity.x = +50
                else:
                    self.player.velocity.x = 0

                if self.key[K_DOWN]:
                    self.rod.move_to((self.player.rect.right - 8, self.player.rect.top + 5))
                    print("fishing!")
                    self.rod.is_fishing = True
                    self.rod.velocity.y = 50
                    self.sprites.add(self.rod)
                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
                    if isinstance(collided, Trash):
                        self.rod.durability -= 1
                        match collided.is_explosive:
                            case True:
                                self.score -= 1
                                common.SOUND_MANAGER.sfx.play("explode")
                            case False:
                                self.score += 1
                                common.SOUND_MANAGER.sfx.play("getTrash")
                        print(f"Session score: {self.score}, durability: {self.rod.durability}")
                        collided.kill()
                        self.rod.is_fishing = False
                        self.rod.velocity.y = 0

                if self.rod.rect.y >= (common.SCREEN_HEIGHT - self.rod.rect.height - common.Y_BORDER):
                    self.rod.is_fishing = False
                    common.SOUND_MANAGER.sfx.play("noTrash")
                else:
                    pygame.draw.line(self.draw_screen, color.DARKRED,
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)

        if self.key[K_ESCAPE]:
            self.rod.kill()
            raise StateSwitch(StateID.LOBBY)


class Lobby(State):
    is_gamemode = False
    desc = "At the lobby..."

    def prepare_assets(self):
        self.assets_raw = [
            "assets/img/bg/",
            "assets/img/sprites/",
        ]

        self.sounds_raw = {
            "supadood": "assets/music/supadood.wav",
            "explode": "assets/sfx/explode.wav",
            "getTrash": "assets/sfx/getTrash.wav",
            "noTrash": "assets/sfx/noTrash.wav",
        }

    def prepare_next_states(self):
        self.is_reloadable = False
        self.next_states = [
            StateID.SHOP,
            StateID.CATASTROPHE,
            StateID.SCOREBOARD,
        ]

    def prepare_sprites(self):
        self.background = Background()

        self.stat_score = Statistic(pos=(5, 10))
        self.stat_score.set_icon(utils.newPath("assets/img/ui/coin.png"), (0, 0))
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)), (20, 0))

        self.temp_ground = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/sand.png"),
            size=(common.SCREEN_WIDTH, int(common.SCREEN_HEIGHT+1-common.GROUND_HEIGHT)),
            pos=(0, common.GROUND_HEIGHT)
        )
        self.temp_ground.set_worldobj(
            desc="ground",
            interactable=False,
            collidable=True
        )
        self.temp_ground.image = utils.multiply_image(
            common.ASSET_DICT.get(utils.newPath("assets/img/bg/sand.png")),
            self.temp_ground.image.size,
            self.temp_ground.size
        )
        self.temp_ground.callibrate()

        self.temp_platform = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/grass.png"),
            size=(50, 50),
            pos=(150, 50)
        )
        self.temp_platform.set_worldobj(
            desc="platform",
            interactable=False,
            collidable=True
        )
        self.temp_platform.image = utils.multiply_image(
            input_image=self.temp_platform.image,
            tile_size=(3, 20),
            target_size=self.temp_platform.size
        )
        self.temp_platform.callibrate()

        self.collidables: RGroup[WorldObject] = RGroup()
        self.collidables.add(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(
            pos=(common.SCREEN_HEIGHT/3, common.GROUND_HEIGHT-50),
        )
        self.player.set_collidables(self.collidables)

        self.interactables_map: dict[str, list] = {
            "Shop": [20, StateID.SHOP, (55, 58), "explode"],
            "Play": [120, StateID.CATASTROPHE, (35, 33), "getTrash"],
            "Score": [220, StateID.SCOREBOARD, (50, 25), "noTrash"]
        }
        self.interactables: RGroup[WorldObject] = RGroup()
        for name, stuff in self.interactables_map.items():
            d = WorldObject(
                static_image_path=utils.newPath(f"assets/img/ui/{name}.png"),
                pos=(stuff[0], (common.GROUND_HEIGHT - stuff[2][1])),
                size=stuff[2],
            )
            d.set_worldobj(
                desc=name,
                interactable=True,
                collidable=True
            )
            self.interactables.add(d)

        self.backgroundStuff_map = [(random.randint(1, 11)*20, (common.GROUND_HEIGHT-61)) for _ in range(15)]
        self.backgroundStuff = RGroup()
        for pos in self.backgroundStuff_map:
            d = WorldObject(
                static_image_path=utils.newPath(f"assets/img/bg/tree.png"),
                pos=pos,
                size=(23, 61),
            )
            d.set_worldobj(
                desc="tree",
                interactable=False,
                collidable=False
            )
            self.backgroundStuff.add(d)

    def load_sprites(self):
        self.sprites.add(
            self.background,
            self.backgroundStuff,
            self.interactables,
            self.collidables,
            self.player,
            self.stat_score,
        )

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("supadood", -1)

    def logic(self):
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)))

        if (self.key[K_LEFT] or self.key[K_a]) and self.player.rect.x >= common.X_BORDER:
            self.player.velocity.x -= self.player.acceleration.x if abs(self.player.velocity.x) < self.player.max_velocity.x else 0
        elif (self.key[K_RIGHT] or self.key[K_d]) and self.player.rect.x <= (common.SCREEN_WIDTH - self.player.rect.width - common.X_BORDER):
            self.player.velocity.x += self.player.acceleration.x if abs(self.player.velocity.x) < self.player.max_velocity.x else 0
        else:
            self.player.velocity.x = 0

        if (self.key[K_UP] or self.key[K_w]):
            self.player.jump()

        # TODO: implement camera system later as a class/functions
        self.camera_offset = pygame.Vector2()

        collided_sprite = pygame.sprite.spritecollideany(self.player, self.interactables, None)

        if isinstance(collided_sprite, WorldObject) and collided_sprite.interactable and self.key[K_RETURN]:
            print("interacted with an interactable worldobject")

            # in each of these checks we could do something special like play a sound effect.
            # it's kinda hardcoded rn but i'll change it later
            common.SOUND_MANAGER.sfx.play(self.interactables_map[collided_sprite.desc][3])

            raise StateSwitch(self.interactables_map[collided_sprite.desc][1], self.shared_state_data)


class Scoreboard(State):
    is_gamemode = False
    desc = "Lookin\' at the scoreboard."

    def prepare_sprites(self):
        filehandling.saveLocal("guy", int(self.shared_state_data.get('score', 0)))
        highscores = filehandling.getLocal()
        text = ""

        for i in highscores:
            text += f"{(i['name'])}: {i['score']}\n"

        text += "end."

        self.text = Text()
        self.text.set_text(
            text=text,
            color=color.WHITE,
            font=common.SMALL_FONT,
            align=pygame.FONT_CENTER
        )

    def load_sprites(self):
        self.sprites.add(self.text)

    def prepare_assets(self):
        self.assets_raw = [
            "savefiles/"
        ]

        self.sounds_raw = {
            "wake-up-call": "assets/music/pause.wav"
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("wake-up-call")

    def logic(self):
        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)


class Shop(State):
    is_gamemode = False
    desc = "Lookin\' for things to buy... or not."

    def prepare_assets(self):
        self.assets_raw = []

        self.sounds_raw = {
            "straight-fundamentals": "assets/music/straight-fundamentals.wav"
        }

    def prepare_sprites(self):
        text = "SHOP"
        text_sprite = Text()
        text_sprite.set_text(
            text=text,
            color=color.WHITE,
            font=common.BIG_FONT
        )
        text_sprite.velocity.x = 5

        self.buttons = ButtonGroup()
        for y in range(3):
            for x in range(5):
                b = Button(pos=(20 + x*50, 50 + y*50))
                b.set_text(
                    text=f"btn",
                    font=common.SMALL_FONT,
                    bg_color=color.YELLOW,
                )
                b.set_button()
                self.buttons.add(b)

        self.sprites.add(self.buttons)

        self.sprites.add(text_sprite)

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("straight-fundamentals", loop=-1)

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        self.buttons.move_cursor_ip(self.key_jp[K_RIGHT] - self.key_jp[K_LEFT])
        self.buttons.move_cursor_ip(5 * (self.key_jp[K_DOWN] - self.key_jp[K_UP]))

        for sprite in self.buttons:
            sprite.is_hovered = self.buttons.get_button_at_cursor() == sprite

        if self.key_jp[K_RETURN]:
            self.buttons.click_button_at_cursor()

        if self.key[K_ESCAPE]:
            raise StateSwitch(StateID.LOBBY, self.shared_state_data)
