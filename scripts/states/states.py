import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *
from scripts.filehandling import *

from scripts.states.basestate import State
from scripts.sprites.sprites import *


class Splash(State):
    def __init__(self, game):
        super().__init__(game, False, "At the splash screen")

        self.introText = drawText(text="press ENTER key to begin", color=WHITE,
                     font=smallFont, screen=self.screen)
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
        self.player = Player()
        self.rod = Rod()
        self.textDisplay = Text(font=bigFont, color=WHITE, coords=Vector2(10, 10))

        self.trashSprites = pygame.sprite.Group()

        spawn_map = loadMap()

        for row in range(len(spawn_map)):
            for col in range(len(spawn_map[0])):
                if spawn_map[row][col] != 0:
                    self.trashSprites.add(
                        Trash(
                            trashType=spawn_map[row][col],
                            coords=Vector2(
                                (row * 25 + xBorder*2),
                                (col * 25 + HEIGHT//2)
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
            self.textDisplay.color = DARKRED
            self.textDisplay.shake(3, 0)
        else:
            self.textDisplay.color = YELLOW

        self.textDisplay.text = f"FPS: {round(clock.get_fps())}\nSCORE: {self.score}"

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
                for collided in pygame.sprite.spritecollide(self.rod, self.trashSprites, True, pygame.sprite.collide_rect):
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
                    pygame.draw.line(self.screen, DARKRED,
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)

        # if self.key[K_ESCAPE]:
        #     self.game.state = Lobby(self.game)


class Lobby(State):
    player_offset = -40

    def __init__(self, game):
        super().__init__(game, False, "At the lobby...")

        self.background = Background()
        self.player = Player(pos=(HEIGHT/2 + self.player_offset, HEIGHT/3))

        self.interactables_map = {
            "Shop": [20, Shop],
            "Play": [120, Catastrophe],
            "Score": [220, Scoreboard]
        }
        self.interactables = pygame.sprite.Group()
        for name, stuff in self.interactables_map.items():
            self.interactables.add(
                WorldObject(
                    imagepath=newPath(f"assets/img/ui/{name}.png"),
                    coords=(stuff[0], 70), desc=name, interactable=True
                )
            )

        self.backgroundStuff_map = [((WIDTH//2 + randint(-200, 200)), (HEIGHT//3 + randint(-10, 10))) for _ in range(5)]
        self.backgroundStuff = pygame.sprite.Group()
        for coords in self.backgroundStuff_map:
            self.backgroundStuff.add(
                WorldObject(
                    imagepath=newPath(f"assets/img/bg/tree.png"),
                    coords=coords, desc="tree", interactable=False
                )
            )

        self.sprites.add(
            self.background,
            self.interactables,
            self.backgroundStuff,
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

        self.player.rect.x += self.player.velocity * self.dt
        self.background.rect.x += self.background.velocity * self.dt

        self.offset = self.player.velocity * self.dt
        self.player_offset = self.player.rect.x - HEIGHT/2  # doesnt work correctly

        for t in self.interactables:
            t.rect.x -= self.offset

        for t in self.backgroundStuff:
            t.rect.x -= self.offset

        collided_sprite = pygame.sprite.spritecollideany(self.player, self.interactables, None)

        if isinstance(collided_sprite, WorldObject) and collided_sprite.interactable and self.key[K_RETURN]:
            print("interacted with an interactable worldobject")

            # in each of these checks we could do something special like play a sound effect.
            if collided_sprite.desc == "Play":
                pass
            elif collided_sprite.desc == "Score":
                pass
            elif collided_sprite.desc == "Shop":
                pass

            self.game.state = self.interactables_map[collided_sprite.desc][1](self.game)


class Scoreboard(State):
    def __init__(self, game):
        super().__init__(game, False, "Lookin\' at the scoreboard")

        highscores = getLocal()
        text = ""

        for i in highscores:
            text += f"{(i['name'])}: {i['score']}\n"

        self.sprites.add(drawText(text=text, color=WHITE,
                         font=smallFont, screen=self.screen,
                         pos=(0, 0)))

    def update(self):
        super().update()

        if self.key[K_ESCAPE]:
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

        if self.key[K_ESCAPE]:
            self.game.state = Lobby(self.game)
