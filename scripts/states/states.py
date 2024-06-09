import pygame
from pygame.locals import *  # type: ignore

from scripts.settings import *
from scripts.filehandling import *

from scripts.states.basestate import State
from scripts.sprites.sprites import *

class Splash(State):
    def __init__(self, game):
        super().__init__(game)

        self.text = "The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start."

        self.logo = MenuLogo()

        self.sprites.add(
            self.logo,
            drawText(text=self.text, color=WHITE, font=smallFont, screen=self.screen)
        )

        self.game.sound_manager.play("cleanup-time")

    def update(self):
        super().update()

        if self.key[K_RETURN]:
            self.game.state = Catastrophe(self.game)


class Catastrophe(State):
    def __init__(self, game):
        super().__init__(game)

        self.score = 0

        self.background = Background()
        self.islands = Islands()
        self.player = Player()
        self.rod = Rod()
        self.textDisplay = Text(font=bigFont, color=WHITE, coords=(10, 10))

        self.trashSprites = pygame.sprite.Group()

        spawn_map = makeMap()

        for row in range(len(spawn_map)):
            for col in range(len(spawn_map[0])):
                if spawn_map[row][col] != 4:
                    self.trashSprites.add(Trash(spawn_map[row][col], ((row * 30 + xBorder * 5), (col * 30 + HEIGHT / 2)), xBorder * 3))

        self.sprites.add(
            self.background,
            self.islands,
            self.trashSprites,
            self.player,
            self.textDisplay,
            self.rod
        )

    def update(self):
        super().update()

        if self.score <= 0:
            self.textDisplay.color = DARKRED
            self.textDisplay.shake()
        else:
            self.textDisplay.color = YELLOW

        self.textDisplay.text = f"SCORE: {self.score}"

        if (not any(isinstance(sprite, Trash) and not sprite.explosive for sprite in self.trashSprites) or self.score < 0):
            self.game.state = Splash(self.game)

        match self.rod.isFishing:
            case False:
                if self.key[K_LEFT] and self.player.rect.x >= xBorder:
                    self.player.rect.x -= self.player.velocity * self.dt
                    self.islands.rect.x += self.islands.velocity * self.dt

                if self.key[K_RIGHT] and self.player.rect.x <= (WIDTH - self.player.rect.width - xBorder):
                    self.player.rect.x += self.player.velocity * self.dt
                    self.islands.rect.x -= self.islands.velocity * self.dt

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
                                # self.explode.play()
                                self.game.sound_manager.play("explode")
                            case False:
                                self.score += 1
                                # self.getTrash.play()
                                self.game.sound_manager.play("getTrash")

                        print(self.score)
                        collided.kill()
                        self.rod.isFishing = False

                if self.rod.rect.y >= (HEIGHT - self.rod.rect.height - yBorder):
                    self.rod.isFishing = False
                    # self.noTrash.play()
                    self.game.sound_manager.play("noTrash")
                else:
                    self.rod.rect.y += self.rod.velocity * self.dt
                    pygame.draw.line(self.screen, (123, 63, 0),
                                     (self.rod.rect.x + self.rod.rect.width /
                                      2, self.player.rect.y),
                                     (self.rod.rect.x + self.rod.rect.width / 2, self.rod.rect.y), 1)


class Scoreboard(State):
    def __init__(self, game):
        super().__init__(game)

        self.title = Text(font=bigFont, color=WHITE, size=10, coords=(10, 10))
        self.title.text = str(getLocal())
        self.sprites.add(self.title)

    def update(self):
        super().update()
