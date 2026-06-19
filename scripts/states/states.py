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

        self.background = BackgroundLayer()

        self.rod = Rod(pos=(common.SCREEN_WIDTH/2, common.Y_BORDER))

        self.textDisplay = Statistic(pos=(5, 10))
        self.textDisplay.set_icon(image_path=utils.newPath("assets/img/ui/clock.png"), pos_ip=(0, 0))
        self.textDisplay.set_text(text="0", pos_ip=(20, 0))

        self.trashSprites: RGroup[Trash] = RGroup()

        trash_id_map = filehandling.makeMap((4, 8))
        self.start_pos = (common.SCREEN_WIDTH + common.X_BORDER, common.WATER_HEIGHT)
        self.distance_between_trash = (
            common.SCREEN_WIDTH / 10,
            common.SCREEN_HEIGHT / 10
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
                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
                    if isinstance(collided, Trash):
                        self.rod.durability -= 1
                        match collided.is_explosive:
                            case True:
                                self.score -= int(self.score*0.05)
                                common.SOUND_MANAGER.sfx.play("explode")
                            case False:
                                self.score += 1
                                common.SOUND_MANAGER.sfx.play("getTrash")
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
        lay1 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky1.png"))
        lay2 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky2.png"))
        lay3 = BackgroundLayer(static_image_path=utils.newPath("assets/img/bg/sky3.png"))

        self.background = ParallaxBackground(lay3, lay2, lay1)

        self.stat_score = Statistic(pos=(5, 10))
        self.stat_score.set_icon(utils.newPath("assets/img/ui/coin.png"), (0, 0))
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)), (20, 0))

        self.temp_ground = WorldObject(
            static_image_path=utils.newPath(f"assets/img/bg/sand.png"),
            size=(common.SCREEN_WIDTH*3, int(common.SCREEN_HEIGHT-common.GROUND_HEIGHT)),
            pos=(-common.SCREEN_WIDTH, common.GROUND_HEIGHT)
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
            pos=(common.GROUND_HEIGHT-50, 50)
        )
        self.temp_platform.set_worldobj(
            desc="platform",
            interactable=False,
            collidable=True
        )
        self.temp_platform.image = utils.multiply_image(
            input_image=self.temp_platform.image,
            tile_size=(6, 20),
            target_size=self.temp_platform.size
        )
        self.temp_platform.callibrate()

        self.collidables: RGroup[WorldObject] = RGroup(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(
            pos=((common.SCREEN_WIDTH-24)/2, common.GROUND_HEIGHT-50),
        )
        self.player.set_collidables(self.collidables)

        self.interactables_map: dict[str, list] = {
            "Shop": [20, StateID.SHOP, (55, 58), "explode"],
            "Score": [120, StateID.SCOREBOARD, (47, 43), "noTrash"],
            "Play": [220, StateID.CATASTROPHE, (35, 33), "getTrash"]
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

        self.clouds_group = RGroup()
        self.trees_group = RGroup()

        self.clouds_map = [(random.uniform(-0.5, 0.5)*self.temp_ground.size[0], random.uniform(-10, 10) + common.CLOUD_HEIGHT) for _ in range(25)]
        for pos in self.clouds_map:
            d = WorldObject(
                sheet_path=utils.newPath(f"assets/img/bg/clouds.json"),
                pos=pos,
                size=(15, 15),
            )
            d.set_worldobj(
                desc="cloud",
                interactable=False,
                collidable=False
            )
            d.image = d.sheet.states[d.sheet.current_state][random.randint(0, 2)]
            d.image.set_alpha(random.randint(200, 225))
            self.clouds_group.add(d)

        self.trees_map = [(random.uniform(0, 1)*self.temp_ground.size[0], (common.GROUND_HEIGHT-random.uniform(51, 61))) for _ in range(15)]
        for pos in self.trees_map:
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
            self.trees_group.add(d)

        self.map_group = RGroup(self.clouds_group, self.trees_group, self.interactables, self.collidables)
        self.map_vel = pygame.Vector2()

    def load_sprites(self):
        self.sprites.add(
            self.background,
            self.map_group,
            self.player,
            self.stat_score,
        )

    def load_assets(self):
        common.SOUND_MANAGER.bgm.play("supadood", -1)

    def logic(self):
        self.stat_score.set_text(str(self.shared_state_data.get('score', 0)))

        for cloud in self.clouds_group:
            if cloud.pos.x >= self.temp_ground.rect.right:
                cloud.move_to((self.temp_ground.rect.left, cloud.pos.y))
            cloud.velocity.x = random.uniform(0, 10)

        if (self.key[K_LEFT] or self.key[K_a]):
            self.map_vel.x -= self.player.acceleration.x if abs(self.map_vel.x) < self.player.max_velocity.x else 0
        elif (self.key[K_RIGHT] or self.key[K_d]):
            self.map_vel.x += self.player.acceleration.x if abs(self.map_vel.x) < self.player.max_velocity.x else 0
        else:
            self.map_vel.x = 0

        if (self.key[K_UP] or self.key[K_w]):
            self.player.jump()

        # crude cam implementation, will change later
        self.map_vel.y = pygame.math.lerp(self.map_vel.y, self.player.velocity.y, 0.5)

        if not self.player.is_colliding:
            self.player.move_to((self.player.old_pos.x, self.player.pos.y))
            self.map_group.move_ip(-self.map_vel*self.dt)
            self.background.move_parallax(self.map_vel*self.dt, 10)

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
