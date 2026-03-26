import pygame
import random
import numpy

from pygame.locals import *  # type: ignore

from scripts import globals, utils, filehandling

from scripts.states.basestate import State, StateID
from scripts.sprites.sprites import *


class Splash(State):
    def prepare_sprites(self):
        self.introText = Text()
        self.introText.set_text(
            text=f"press [ENTER] to begin",
            color=globals.WHITE,
            font=globals.smallFont,
        )
        self.introText.rect.center = (globals.SCREEN_WIDTH/2, globals.SCREEN_HEIGHT/1.25)

        self.logo = MenuLogo()
        self.logo.rect.center = (
            globals.SCREEN_WIDTH / 2,
            globals.SCREEN_HEIGHT / 2
        )

        self.sprites.add(
            self.logo,
            self.introText
        )

    def prepare_sounds(self):
        self.sounds = {
            "cleanup-time": "assets/music/cleanup-time.wav",
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_sounds(self):
        self.sound_manager.play("cleanup-time", loop=-1)

    def logic(self):
        if self.key[K_RETURN] or self.key[K_SPACE]:
            self.switch_state(self.next_states[0])


class Catastrophe(State):
    def prepare_sprites(self):
        self.score = 0

        self.background = Background()

        self.temp_ground = WorldObject(
            image_path=utils.newPath(f"assets/img/bg/sand.png"),
        )
        self.temp_ground.set_worldobj(
            desc="ground",
            interactable=False,
            collidable=True
        )
        self.temp_ground.image = multiply_image(
            input_image=self.temp_ground.image,
            tile_size=(1, 1),
            target_size=(globals.SCREEN_WIDTH, 1)
        )
        self.temp_ground.image_rect = self.temp_ground.image.get_rect()
        self.temp_ground.image_size = self.temp_ground.image_rect.size
        self.temp_ground.rect = self.temp_ground.image.get_frect()
        self.temp_ground.rect.x, self.temp_ground.rect.y = 0, globals.WATER_HEIGHT
        # TODO: make a new class for a resizable sprite

        self.collidables = RGroup(self.temp_ground)

        self.player = Player(
            pos=(0, globals.WATER_HEIGHT - 50),
        )
        self.player.set_collidables(self.collidables)

        self.rod = Rod(pos=(-100, -100))
        self.textDisplay = Text(pos=(10, 10))
        self.textDisplay.set_text(text="", font=globals.bigFont, color=globals.WHITE)

        self.trashSprites: RGroup[Trash] = RGroup()

        trash_id_map = filehandling.makeMap((4, 8))
        filehandling.saveMap(trash_id_map)
        self.start_pos = (globals.xBorder*20, globals.WATER_HEIGHT + 30)
        self.distance_between_trash = (
            globals.SCREEN_WIDTH * len(trash_id_map[0]) / 30,
            globals.SCREEN_HEIGHT * len(trash_id_map) / 150
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
        self.sprites.add(
            self.background,
            self.trashSprites,
            # self.collidables, # only show for debug purposes i guess
            self.player,
            self.textDisplay,
            self.rod
        )

    def prepare_sounds(self):
        self.sounds = {
            "waiting": "assets/music/waiting.wav",
            "explode": "assets/sfx/explode.wav",
            "getTrash": "assets/sfx/getTrash.wav",
            "noTrash": "assets/sfx/noTrash.wav",
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY,
            StateID.SCOREBOARD,
        ]

    def load_sounds(self):
        self.sound_manager.play("waiting")

    def logic(self):
        if self.score <= 0:
            self.textDisplay.color = globals.DARKRED
            self.textDisplay.shake((1, 0))
        else:
            self.textDisplay.color = globals.BLACK

        self.textDisplay.set_text(f"FPS: {round(globals.clock.get_fps())}\nSCORE: {self.score}\nDURABILITY: {self.rod.durability}")

        if not any(isinstance(t, Trash) and (not t.is_explosive) for t in self.trashSprites) or self.score < 0:
            self.switch_state(self.next_states[1])

        last_trash = list(self.trashSprites)[-1]
        if last_trash.rect.right <= 0:
            # checks if the last trash is at the rightmost of the spawn map, if so, will automatically end the game
            self.switch_state(self.next_states[1])

        for t in self.trashSprites:
            if t.is_explosive:
                t.velocity.x = -3
            else:
                t.velocity.x = -random.randint(4, 12)

        match self.rod.is_fishing:
            case False:
                if self.key[K_LEFT] and self.player.rect.x >= globals.xBorder:
                    self.player.velocity.x = -50
                elif self.key[K_RIGHT] and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder):
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
                                self.sound_manager.play("explode")
                            case False:
                                self.score += 1
                                self.sound_manager.play("getTrash")
                        print(f"Session score: {self.score}, durability: {self.rod.durability}")
                        collided.kill()
                        self.rod.is_fishing = False
                        self.rod.velocity.y = 0

                if self.rod.rect.y >= (globals.SCREEN_HEIGHT - self.rod.rect.height - globals.yBorder):
                    self.rod.is_fishing = False
                    self.sound_manager.play("noTrash")
                else:
                    pygame.draw.line(self.screen, globals.DARKRED,
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)
                    # TODO: make it so that all the pygame.draw stuff is displayed on top of self.screen so that it is actually visible!!!

        if self.key[K_ESCAPE]:
            self.switch_state(self.next_states[1])


class Lobby(State):
    def prepare_sounds(self):
        self.sounds = {
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

        self.temp_ground = WorldObject(
            image_path=utils.newPath(f"assets/img/bg/sand.png")
        )
        self.temp_ground.set_worldobj(
            desc="ground",
            interactable=False,
            collidable=True
        )
        self.temp_ground.image = multiply_image(
            input_image=self.temp_ground.image,
            tile_size=(3, 20),
            target_size=(globals.SCREEN_WIDTH, 50)
        )

        noise = numpy.random.uniform(0.8, 1.0, (25, 25))
        img = noise[..., None] * [*globals.SAND[:3]]

        self.temp_ground.image = mode7(
            pygame.surfarray.make_surface(
                img.swapaxes(0, 1)
            ),
            (globals.SCREEN_WIDTH, int(globals.SCREEN_HEIGHT+1-globals.GROUND_HEIGHT)),
        )
        self.temp_ground.rect = self.temp_ground.image.get_frect()
        self.temp_ground.rect.x, self.temp_ground.rect.y = 0, globals.GROUND_HEIGHT

        self.temp_platform = WorldObject(
            image_path=utils.newPath(f"assets/img/bg/grass.png"),
        )
        self.temp_platform.set_worldobj(
            desc="platform",
            interactable=False,
            collidable=True
        )
        self.temp_platform.image = multiply_image(
            input_image=self.temp_platform.image,
            tile_size=(3, 20),
            target_size=(50, 50)
        )
        self.temp_platform.rect = self.temp_platform.image.get_frect()
        self.temp_platform.rect.x, self.temp_platform.rect.y = 150, 50

        self.collidables = RGroup()
        self.collidables.add(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(
            pos=(globals.SCREEN_HEIGHT/3, globals.GROUND_HEIGHT-50),
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
                image_path=utils.newPath(f"assets/img/ui/{name}.png"),
                pos=(stuff[0], (globals.GROUND_HEIGHT - stuff[2][1])),
                size=stuff[2],
            )
            d.set_worldobj(
                desc=name,
                interactable=True,
                collidable=True
            )
            self.interactables.add(d)

        self.backgroundStuff_map = [(random.randint(1, 11)*20, (globals.GROUND_HEIGHT-61)) for _ in range(15)]
        self.backgroundStuff = RGroup()
        for pos in self.backgroundStuff_map:
            d = WorldObject(
                image_path=utils.newPath(f"assets/img/bg/tree.png"),
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
        )

    def load_sounds(self):
        self.sound_manager.play("supadood", loop=-1)

    def logic(self):
        self.player.rect.clamp_ip(self.screen.get_rect())

        if (self.key[K_LEFT] or self.key[K_a]) and self.player.rect.x >= globals.xBorder:
            self.player.velocity.x -= self.player.acceleration.x if abs(self.player.velocity.x) < self.player.max_velocity.x else 0
        elif (self.key[K_RIGHT] or self.key[K_d]) and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder):
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
            self.sound_manager.play(self.interactables_map[collided_sprite.desc][3])

            self.switch_state(self.interactables_map[collided_sprite.desc][1])


class Scoreboard(State):
    def prepare_sprites(self):
        filehandling.saveLocal("the person that played this game", 10000000000, True)
        highscores = filehandling.getLocal()
        text = ""

        for i in highscores:
            text += f"{(i['name'])}: {i['score']}\n"

        text += "todo: implement shared state data, because your score isnt actually 10 billion lol"

        self.text = Text()
        self.text.set_text(
            text=text,
            color=globals.WHITE,
            font=globals.smallFont
        )

    def load_sprites(self):
        self.sprites.add(self.text)

    def prepare_sounds(self):
        self.sounds = {
            "wake-up-call": "assets/music/pause.wav"
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_sounds(self):
        self.sound_manager.play("wake-up-call", loop=-1)

    def logic(self):
        if self.key[K_ESCAPE]:
            self.switch_state(StateID.LOBBY)


class Shop(State):
    def prepare_sprites(self):
        text = "This is the shop, in future iterations of this project even this page will be completed!\nHang tight as we develop this project."
        text_sprite = Text()
        text_sprite.set_text(
            text=text,
            color=globals.WHITE,
            font=globals.smallFont
        )
        self.sprites.add(text_sprite)

    def prepare_sounds(self):
        self.sounds = {
            "straight-fundamentals": "assets/music/straight-fundamentals.wav"
        }

    def load_sounds(self):
        self.sound_manager.play("straight-fundamentals", loop=-1)

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        if self.key[K_ESCAPE]:
            self.switch_state(self.next_states[0])
