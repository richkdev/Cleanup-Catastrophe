import pygame, asyncio, moderngl
from pygame.locals import * # type: ignore

from scripts.settings import *

pygame.display.set_caption(f"Cleanup Catastrophe! {version}")
pygame.display.set_icon(pygame.image.load("icon.ico"))

from scripts.highscoreSaver import saveLocal, displayLocal

flags = SHOWN | RESIZABLE | SCALED | HWSURFACE | DOUBLEBUF #| FULLSCREEN

if not emscripten:
    flags += OPENGLBLIT
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, depth=1, display=0, vsync=1)
    from scripts.GLcontext import surf_to_texture, render_object, ctx
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, depth=1, display=0, vsync=1)

class Game():
    def __init__(self):
        self.run = True
        self.score = 0
        self.state = 0

        print(settings)
        print("GAME START")

        asyncio.run(self.main())

    async def main(self):
        from scripts.player import Player, FishRod
        from scripts.trash import Trash
        from scripts.menu import Background, Islands

        visibleSprites = pygame.sprite.Group()
        trashSprites = pygame.sprite.Group()

        for i in range(20):
            trashSprites.add(Trash())
            i+=1
        
        background = Background()
        islands = Islands()
        player = Player()
        rod = FishRod()
        
        rodGroup = pygame.sprite.GroupSingle(rod)

        visibleSprites.add(
            background,
            islands,
            trashSprites,
            player
        )

        while self.run:
            key = pygame.key.get_pressed()
            dt = clock.tick(FPS)/1000

            if not emscripten:
                frame_tex = surf_to_texture(screen)
                frame_tex.use(0)
                render_object.render(mode=moderngl.TRIANGLE_STRIP)

                frame_tex.release()
                pygame.display.flip()
                ctx.clear(0)
            else:
                pygame.display.flip()

            visibleSprites.update()
            visibleSprites.draw(screen)

            match rod.isFishing:
                case False:
                    if key[K_LEFT] and player.rect.x >= xBorder:
                        player.rect.x -= player.velocity*dt
                        islands.rect.x += islands.velocity* dt
                    elif key[K_RIGHT] and player.rect.x <= (WIDTH - player.rect.width - xBorder):
                        player.rect.x += player.velocity*dt
                        islands.rect.x -= islands.velocity*dt
                    elif key[K_DOWN]:
                        rod.rect.x = player.rect.right-8
                        rod.rect.y = player.rect.top
                        print("fishing!")
                        rod.isFishing = True
                        visibleSprites.add(rod)
                case True:
                    if pygame.sprite.groupcollide(rodGroup, trashSprites, False, True):
                        self.score += 1
                        rod.isFishing = False
                        visibleSprites.remove(rod)
                    elif rod.rect.y >= (HEIGHT - rod.rect.height - yBorder):
                        rod.rect.y = (HEIGHT - rod.rect.height - yBorder)
                        rod.isFishing = False
                        visibleSprites.remove(rod)
                    else:
                        rod.rect.y += rod.velocity*dt
                        pygame.draw.line(screen, (123, 63, 0), (rod.rect.x + rod.rect.width/2,
                                         player.rect.y), (rod.rect.x + rod.rect.width/2, rod.rect.y), 1)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.run = False
                    break

            await asyncio.sleep(0)

        print("GAME STOP")

        saveLocal(input("PLAYER NAME: "), self.score)
        print(f"SESSION SCORE\t: {self.score}\nHIGHSCORES\t:")
        displayLocal()

game = Game()
