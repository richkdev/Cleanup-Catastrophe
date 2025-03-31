import pygame
from pygame.locals import *  # type: ignore

from scripts import globals, utils
from scripts.filehandling import *

from scripts.states.basestate import State
from scripts.sprites.sprites import *


class Splash(State):
    def __init__(self, game):
        super().__init__(game, False, "At the splash screen")

        self.introText = drawText(text="press ENTER key to begin", color=globals.WHITE,
                     font=globals.smallFont, screen=self.screen)
        self.logo = MenuLogo()

        self.sprites.add(
            self.logo,
            self.introText
        )

        if self.game.music_sound_id:
            self.sound_manager.stop_sound(self.game.music_sound_id)
        self.game.music_sound_id = self.sound_manager.play("cleanup-time")

    def update(self):
        super().update()

        if self.key[K_RETURN]:
            self.game.state = Lobby(self.game)


class Catastrophe(State):
    def __init__(self, game):
        super().__init__(game, True, "CATASTROPHE")

        self.score = 0

        self.background = Background()
        self.player = Player(pos=(globals.SCREEN_WIDTH//3, globals.SCREEN_HEIGHT//3), collideables=pygame.sprite.Group())
        self.rod = Rod()
        self.textDisplay = Text(font=globals.bigFont, color=globals.WHITE, coords=(10, 10))

        self.trashSprites = pygame.sprite.Group()

        spawn_map = loadMap()

        for row in range(len(spawn_map)):
            for col in range(len(spawn_map[0])):
                if spawn_map[row][col] != 0:
                    self.trashSprites.add(
                        Trash(
                            trashType=spawn_map[row][col],
                            coords=pygame.Vector2(
                                (row * 25 + globals.xBorder*2),
                                (col * 25 + globals.SCREEN_HEIGHT//2)
                            ),
                            offset=20
                        )
                    )

        self.sprites.add(
            self.background,
            self.trashSprites,
            self.player,
            self.textDisplay,
            self.rod
        )

    def update(self):
        super().update()

        if self.score <= 0:
            self.textDisplay.color = globals.DARKRED
            self.textDisplay.shake(3, 0)
        else:
            self.textDisplay.color = globals.YELLOW

        self.textDisplay.text = f"FPS: {round(globals.clock.get_fps())}\nSCORE: {self.score}"

        if not any(isinstance(sprite, Trash) and (not sprite.explosive) for sprite in self.trashSprites) or self.score < 0:
            self.game.state = Lobby(self.game)

        match self.rod.isFishing:
            case False:
                if self.key[K_LEFT] and self.player.rect.x >= globals.xBorder:
                    self.player.velocity.x = -50
                if self.key[K_RIGHT] and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder):
                    self.player.velocity.x = +50

                if self.key[K_DOWN]:
                    self.rod.rect.x = self.player.rect.right - 8
                    self.rod.rect.y = self.player.rect.top + 5
                    print("fishing!")
                    self.rod.isFishing = True
                    self.sprites.add(self.rod)
                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
                    if isinstance(collided, Trash):
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

                if self.rod.rect.y >= (globals.SCREEN_HEIGHT - self.rod.rect.height - globals.yBorder):
                    self.rod.isFishing = False
                    self.sound_manager.play("noTrash")
                else:
                    self.rod.rect.y += self.rod.velocity.y * self.dt
                    pygame.draw.line(self.screen, globals.DARKRED,
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)

        # if self.key[K_ESCAPE]:
        #     self.game.state = Lobby(self.game)


class Lobby(State):
    def __init__(self, game):
        super().__init__(game, False, "At the lobby...")

        self.background = Background()

        self.temp_ground = WorldObject(
            imagepath=utils.newPath(f"assets/img/ui/Play.png"),
            desc="ground",
            interactable=False, collidable=True
        )
        self.temp_ground.image = resizeImage(
            input_image=self.temp_ground.image,
            tile_size=(34, 13),
            target_size=(globals.SCREEN_WIDTH, 50)
        )
        self.temp_ground.rect = self.temp_ground.image.get_frect()
        self.temp_ground.rect.x, self.temp_ground.rect.y = 0, globals.GROUND_HEIGHT

        self.temp_platform = WorldObject(
            imagepath=utils.newPath(f"assets/img/ui/Shop.png"),
            desc="platform",
            interactable=False, collidable=True
        )
        self.temp_platform.image = resizeImage(
            input_image=self.temp_platform.image,
            tile_size=(34, 13),
            target_size=(50, 50)
        )
        self.temp_platform.rect = self.temp_platform.image.get_frect()
        self.temp_platform.rect.x, self.temp_platform.rect.y = 100, 50

        self.collideables = pygame.sprite.Group()
        self.collideables.add(
            self.temp_ground,
            self.temp_platform
        )

        self.player = Player(pos=(int(globals.SCREEN_HEIGHT//3), int(globals.GROUND_HEIGHT-100)), collideables=self.collideables)

        self.interactables_map = {
            "Shop": [20, Shop, (34, 13)],
            "Play": [120, Catastrophe, (34, 13)],
            "Score": [220, Scoreboard, (34, 13)]
        }
        self.interactables = pygame.sprite.Group()
        for name, stuff in self.interactables_map.items():
            self.interactables.add(
                WorldObject(
                    imagepath=utils.newPath(f"assets/img/ui/{name}.png"),
                    coords=pygame.Vector2(stuff[0], (globals.GROUND_HEIGHT-25)), size=stuff[2], desc=name,
                    interactable=True, collidable=False
                )
            )

        self.backgroundStuff_map = [(randint(1, 11)*20, (globals.GROUND_HEIGHT-61)) for _ in range(5)]
        self.backgroundStuff = pygame.sprite.Group()
        for coords in self.backgroundStuff_map:
            self.backgroundStuff.add(
                WorldObject(
                    imagepath=utils.newPath(f"assets/img/bg/tree.png"),
                    coords=pygame.Vector2(coords), size=pygame.Vector2(23, 61), desc="tree",
                    interactable=False, collidable=False
                )
            )

        self.sprites.add(
            self.background,
            self.backgroundStuff,
            self.interactables,
            self.collideables,
            self.player,
        )

    def update(self):
        super().update()

        if self.key[K_LEFT] and self.player.rect.x >= globals.xBorder and not self.player.collisions['left']:
            self.player.velocity.x = -100
        if self.key[K_RIGHT] and self.player.rect.x <= (globals.SCREEN_WIDTH - self.player.rect.width - globals.xBorder) and not self.player.collisions['right']:
            self.player.velocity.x = +100
        if self.key[K_UP]:
            self.player.jump()

        # will implement camera system later as a class/function (?)
        collided_sprite = pygame.sprite.spritecollideany(self.player, self.interactables, None)

        if isinstance(collided_sprite, WorldObject) and collided_sprite.interactable and self.key[K_RETURN]:
            print("interacted with an interactable worldobject")

            # in each of these checks we could do something special like play a sound effect.
            # it's kinda hardcoded rn but i'll change it later
            if collided_sprite.desc == "Play":
                self.sound_manager.play("explode")
            elif collided_sprite.desc == "Score":
                self.sound_manager.play("getTrash")
            elif collided_sprite.desc == "Shop":
                self.sound_manager.play("noTrash")

            self.game.state = self.interactables_map[collided_sprite.desc][1](self.game)


class Scoreboard(State):
    def __init__(self, game):
        super().__init__(game, False, "Lookin\' at the scoreboard")

        highscores = getLocal()
        text = ""

        for i in highscores:
            text += f"{(i['name'])}: {i['score']}\n"

        self.sprites.add(drawText(text=text, color=globals.WHITE,
                         font=globals.smallFont, screen=self.screen,
                         pos=(0, 0)))
    
        msgbox = pygame.display.message_box(title="WIP", message='rahhh', message_type='info', buttons=('OK',))
        print(msgbox.imag)

    def update(self):
        super().update()

        if self.key[K_ESCAPE]:
            self.game.state = Lobby(self.game)


class Shop(State):
    def __init__(self, game):
        super().__init__(game, False, "Lookin\' for things to buy.. or not.")

        text = "This is the shop, in future iterations of this project even this page will be completed!\nHang tight as we develop this project."
        self.sprites.add(drawText(text=text, color=globals.WHITE,
                         font=globals.smallFont, screen=self.screen,
                         pos=(0, 0)))

    def update(self):
        super().update()

        if self.key[K_ESCAPE]:
            self.game.state = Lobby(self.game)
