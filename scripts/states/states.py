import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *
from scripts.filehandling import *

from scripts.states.basestate import State
from scripts.sprites.sprites import *


class Splash(State):
    def __init__(self, game):
        super().__init__(game, False, "At the splash screen")

        self.text = "The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start."

        self.logo = MenuLogo()

        self.sprites.add(
            self.logo,
            drawText(text=self.text, color=WHITE,
                     font=smallFont, screen=self.screen)
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
        self.player = Player()
        self.rod = Rod()
        self.textDisplay = Text(font=bigFont, color=WHITE, coords=(10, 10))

        self.trashSprites = pygame.sprite.Group()

        spawn_map = makeMap()

        for row in range(len(spawn_map)):
            for col in range(len(spawn_map[0])):
                if spawn_map[row][col] != 4:
                    self.trashSprites.add(Trash(spawn_map[row][col], (int(row * 25 + xBorder * 6), int(col * 25 + HEIGHT / 2)), xBorder * 2))

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
            self.textDisplay.color = DARKRED
            self.textDisplay.shake(3, 0)
        else:
            self.textDisplay.color = YELLOW

        self.textDisplay.text = f"SCORE: {self.score}"

        if not any(isinstance(sprite, Trash) and not sprite.explosive for sprite in self.trashSprites) or self.score < 0:
            self.game.state = Lobby(self.game)

        match self.rod.isFishing:
            case False:
                self.player.velocity = 0

                if self.key[K_LEFT] and self.player.rect.x >= xBorder:
                    self.player.velocity = -100

                if self.key[K_RIGHT] and self.player.rect.x <= (WIDTH - self.player.rect.width - xBorder):
                    self.player.velocity = 100

                self.player.rect.x += self.player.velocity * self.dt

                if self.key[K_DOWN]:
                    self.rod.rect.x = self.player.rect.right - 8
                    self.rod.rect.y = self.player.rect.top + 5
                    print("fishing!")
                    self.rod.isFishing = True
                    self.sprites.add(self.rod)
                elif self.sprites.has(self.rod):
                    self.sprites.remove(self.rod)

            case True:
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_mask):
                    if isinstance(collided, Trash):
                        match collided.explosive:
                            case True:
                                self.score -= 1
                                self.sound_manager.play("explode")
                            case False:
                                self.score += 1
                                self.sound_manager.play("getTrash")
                        print(f"Session score: {self.score}, durability: {self.rod.durable}")
                        collided.kill()
                        self.rod.isFishing = False

                if self.rod.rect.y >= (HEIGHT - self.rod.rect.height - yBorder):
                    self.rod.isFishing = False
                    self.sound_manager.play("noTrash")
                else:
                    self.rod.rect.y += self.rod.velocity * self.dt
                    pygame.draw.line(self.screen, (123, 63, 0),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)

        if self.key_just_pressed[K_ESCAPE]:
            self.game.state = Lobby(self.game)


class Lobby(State):
    player_offset = 0

    def __init__(self, game):
        super().__init__(game, False, "At the lobby...")

        self.background = Background()
        self.player = Player(pos=(HEIGHT/2 + self.player_offset, HEIGHT/3))

        self.mapInteractables = {
            "Shop": [20, Shop],
            "Play": [120, Catastrophe],
            "Score": [220, Scoreboard]
        }
        self.interactables = pygame.sprite.Group()
        for name, stuff in self.mapInteractables.items():
            self.interactables.add(
                WorldObject(
                    newPath(f"assets/img/ui/{name}.png"),
                    (stuff[0], 70),
                    name
                )
            )

        # self.mapOthers = [randint(-50, 50) for _ in range(5)]
        # self.otherStuff = pygame.sprite.Group()
        # for name, stuff in self.mapInteractables.items():
        #     self.interactables.add(
        #         WorldObject(newPath(f"assets/img/ui/{name}.png"), (stuff[0], 70), name)
        #     )


        self.sprites.add(
            self.background,
            self.interactables,
            # self.otherStuff,
            self.player
        )
        self.offset = 0

    def update(self):
        super().update()

        self.player.velocity = 0

        if self.key[K_LEFT] and self.player.rect.x >= xBorder:
            self.player.velocity -= 80
        elif self.key[K_RIGHT] and self.player.rect.x <= (WIDTH - xBorder - self.player.rect.width):
            self.player.velocity += 80

        # self.player.rect.x += self.player.velocity * self.dt
        self.offset = self.player.velocity * self.dt
        self.player_offset = self.player.rect.x - HEIGHT/2  # doesnt work correctly

        for t in self.interactables:
            t.rect.x -= self.offset

        # for t in self.otherStuff:
            # t.rect.x -= self.offset

        collided_sprite = pygame.sprite.spritecollideany(self.player, self.interactables, None)

        if isinstance(collided_sprite, WorldObject) and self.key_just_pressed[K_RETURN]:
            print("interacted with an interactable worldobject")

            # in each of these checks we could do something special like play a sound effect.
            if collided_sprite.desc == "Play":
                pass
            elif collided_sprite.desc == "Score":
                pass
            elif collided_sprite.desc == "Shop":
                pass

            self.game.state = self.mapInteractables[collided_sprite.desc][1](self.game)


class Scoreboard(State):
    def __init__(self, game):
        super().__init__(game, False, "Lookin\' at the scoreboard")

        self.text = str(getLocal())

        self.sprites.add(drawText(text=self.text, color=WHITE,
                         font=smallFont, screen=self.screen,
                         pos=(0, 0)))

    def update(self):
        super().update()

        if self.key_just_pressed[K_ESCAPE]:
            self.game.state = Lobby(self.game)


class Shop(State):
    def __init__(self, game):
        super().__init__(game, False, "Lookin\' for things to buy.. or not.")

        text = "This is the shop, in future iterations of this project even this page will be completed!\nHang tight as we develop this project."
        self.sprites.add(drawText(text=text, color=WHITE,
                         font=smallFont, screen=self.screen,
                         pos=(0, 0)))

    def update(self):
        super().update()

        if self.key_just_pressed[K_ESCAPE]:
            self.game.state = Lobby(self.game)
