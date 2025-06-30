import pygame
from pygame.locals import *  # type: ignore

from scripts import globals, utils, filehandling

from scripts.states.basestate import State, StateID
from scripts.sprites.sprites import *

import random


class Splash(State):
    def prepare_sprites(self):
        self.introText = Text(
            text="press [ENTER] key to begin",
            color=globals.WHITE,
            font=globals.smallFont,
        )
        self.introText.rect.center = (globals.SCREEN_WIDTH/2, globals.SCREEN_HEIGHT/1.25)

        self.logo = MenuLogo()

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
        self.sound_manager.play("cleanup-time")

    def logic(self):
        if self.key[K_RETURN] or self.key[K_SPACE]:
            self.switch_state(StateID.LOBBY)


class Catastrophe(State):
    def prepare_sprites(self):
        self.score = 0
        self.water_height = globals.GROUND_HEIGHT - 50

        self.background = Background()

        self.temp_ground = WorldObject(
            imagepath=utils.newPath(f"assets/img/bg/sand.png"),
            desc="ground",
            interactable=False, collidable=True
        )
        self.temp_ground.image = resizeImage(
            input_image=self.temp_ground.image,
            tile_size=(1, 1),
            target_size=(globals.SCREEN_WIDTH, 5)
        )
        self.temp_ground.image_rect = self.temp_ground.image.get_rect()
        self.temp_ground.image_size = self.temp_ground.image_rect.size
        self.temp_ground.rect = self.temp_ground.image.get_frect()
        self.temp_ground.rect.x, self.temp_ground.rect.y = 0, self.water_height
        # might want to make a new class for a resizable sprite

        self.collideables = pygame.sprite.GroupSingle()
        self.collideables.add(self.temp_ground)

        self.player = Player(
            pos=(0, self.water_height - 50),
            collideables=self.collideables
        )
        self.rod = Rod()
        self.textDisplay = Text(font=globals.bigFont, color=globals.WHITE, pos=(10, 10))

        self.trashSprites = pygame.sprite.Group()

        self.spawn_map = filehandling.makeMap((3, 3))
        self.start_pos = (globals.xBorder*20, self.water_height + 20)
        self.distance_between_trash = (
            (globals.SCREEN_WIDTH * len(self.spawn_map[0])) / 12,
            (globals.SCREEN_HEIGHT * len(self.spawn_map)) / 20
        )

        for row in range(len(self.spawn_map)):
            for col in range(len(self.spawn_map[0])):
                if self.spawn_map[row][col] != 0:
                    self.trashSprites.add(
                        Trash(
                            trashType=self.spawn_map[row][col],
                            coords=pygame.Vector2(
                                (row * self.distance_between_trash[0] + self.start_pos[0]),
                                (col * self.distance_between_trash[1] + self.start_pos[1])
                            ),
                            offset=5
                        )
                    )

        self.sprites.add(
            self.background,
            self.trashSprites,
            # self.collideables, # only show for debug purposes i guess
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
            self.textDisplay.shake(3, 0)
        else:
            self.textDisplay.color = globals.BLACK

        self.textDisplay.text = f"FPS: {round(globals.clock.get_fps())}\nSCORE: {self.score}\nDURABILITY: {self.rod.durability}"

        if not any(isinstance(sprite, Trash) and (not sprite.explosive) for sprite in self.trashSprites) or self.score < 0:
            self.switch_state(self.next_states[1])

        match self.rod.isFishing:
            case False:
                if self.key[K_LEFT] and self.player.rect.x >= globals.xBorder:
                    self.player.velocity.x = -50
                if self.key[K_RIGHT] and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder):
                    self.player.velocity.x = 50

                if self.key[K_DOWN]:
                    self.rod.displace((self.player.rect.right - 8, self.player.rect.top + 5))
                    print("fishing!")
                    self.rod.isFishing = True
                    self.rod.velocity.y = 50
                    self.sprites.add(self.rod)
                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
                    if isinstance(collided, Trash):
                        self.rod.durability -= 1
                        match collided.explosive:
                            case True:
                                self.score -= 1
                                self.sound_manager.play("explode")
                            case False:
                                self.score += 1
                                self.sound_manager.play("getTrash")
                        print(f"Session score: {self.score}, durability: {self.rod.durability}")
                        collided.kill()
                        self.rod.isFishing = False
                        self.rod.velocity.y = 0

                if self.rod.rect.y >= (globals.SCREEN_HEIGHT - self.rod.rect.height - globals.yBorder):
                    self.rod.isFishing = False
                    self.sound_manager.play("noTrash")
                else:
                    pygame.draw.line(self.screen, globals.DARKRED,
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)

        if self.key[K_ESCAPE]:
            self.switch_state(self.next_states[0])


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
            imagepath=utils.newPath(f"assets/img/bg/sand.png"),
            desc="ground",
            interactable=False, collidable=True
        )
        self.temp_ground.image = resizeImage(
            input_image=self.temp_ground.image,
            tile_size=(3, 20),
            target_size=(globals.SCREEN_WIDTH, 50)
        )
        self.temp_ground.rect = self.temp_ground.image.get_frect()
        self.temp_ground.rect.x, self.temp_ground.rect.y = 0, globals.GROUND_HEIGHT

        self.temp_platform = WorldObject(
            imagepath=utils.newPath(f"assets/img/bg/grass.png"),
            desc="platform",
            interactable=False, collidable=True
        )
        self.temp_platform.image = resizeImage(
            input_image=self.temp_platform.image,
            tile_size=(3, 20),
            target_size=(50, 50)
        )
        self.temp_platform.rect = self.temp_platform.image.get_frect()
        self.temp_platform.rect.x, self.temp_platform.rect.y = 150, 50

        self.collideables = pygame.sprite.Group()
        self.collideables.add(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(
            pos=(globals.SCREEN_HEIGHT//3, globals.GROUND_HEIGHT-50),
            collideables=self.collideables
        )

        self.interactables_map: dict[str, list] = {
            "Shop": [20, self.next_states[0], (55, 58), "explode"],
            "Play": [120, self.next_states[1], (35, 33), "getTrash"],
            "Score": [220, self.next_states[2], (50, 25), "noTrash"]
        }
        self.interactables = pygame.sprite.Group()
        for name, stuff in self.interactables_map.items():
            self.interactables.add(
                WorldObject(
                    imagepath=utils.newPath(f"assets/img/ui/{name}.png"),
                    coords=(stuff[0], (globals.GROUND_HEIGHT - stuff[2][1])),
                    size=stuff[2],
                    desc=name,
                    interactable=True,
                    collidable=True
                )
            )

        self.backgroundStuff_map = [(random.randint(1, 11)*20, (globals.GROUND_HEIGHT-61)) for _ in range(15)]
        self.backgroundStuff = pygame.sprite.Group()
        for coords in self.backgroundStuff_map:
            self.backgroundStuff.add(
                WorldObject(
                    imagepath=utils.newPath(f"assets/img/bg/tree.png"),
                    coords=pygame.Vector2(coords),
                    size=(23, 61),
                    desc="tree",
                    interactable=False,
                    collidable=False
                )
            )

        self.sprites.add(
            self.background,
            self.backgroundStuff,
            self.interactables,
            self.collideables,
            self.player,
        )

    def load_sounds(self):
        self.sound_manager.play("supadood", loop=-1)

    def logic(self):
        if (self.key[K_LEFT] or self.key[K_a]) and self.player.rect.x >= globals.xBorder:
            self.player.velocity.x = -100
        if (self.key[K_RIGHT] or self.key[K_d]) and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder):
            self.player.velocity.x = +100
        if (self.key[K_UP] or self.key[K_w]):
            self.player.jump()

        # will implement camera system later as a class/function (?)
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

        self.sprites.add(drawText(
            text=text,
            color=globals.WHITE,
            font=globals.smallFont,
            pos=(0, 0)
        ))

    def prepare_sounds(self) -> None:
        self.sounds = {
            "wake-up-call": "assets/music/pause.wav"
        }

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def load_sounds(self):
        self.sound_manager.play("wake-up-call")

    def logic(self):
        if self.key[K_ESCAPE]:
            self.switch_state(StateID.LOBBY)


class Shop(State):
    def prepare_sprites(self):
        text = "This is the shop, in future iterations of this project even this page will be completed!\nHang tight as we develop this project."
        text_sprite = drawText(
            text=text,
            color=globals.WHITE,
            font=globals.smallFont,
            pos=(0, 0)
        )
        self.sprites.add(text_sprite)

    def prepare_sounds(self) -> None:
        self.sounds = {
            "straight-fundamentals": "assets/music/straight-fundamentals.wav"
        }

    def load_sounds(self):
        self.sound_manager.play("straight-fundamentals")

    def prepare_next_states(self):
        self.is_reloadable = True
        self.next_states = [
            StateID.LOBBY
        ]

    def logic(self):
        if self.key[K_ESCAPE]:
            self.switch_state(self.next_states[0])
