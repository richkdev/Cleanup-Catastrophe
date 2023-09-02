#! /usr/bin/env python3

# https://pyinstaller.org/en/stable/spec-files.html
# https://pyinstaller.org/en/stable/usage.html#cmdoption-splash


from pygame.locals import *  # type: ignore (fuck off pylint)
import pygame

from os import chdir, path, getcwd
chdir(path.dirname(path.abspath(__file__)))  # kinda important to add ngl
print(__file__, getcwd())


game_ver = "v.ALPHA.1.0.0"
pygame.display.set_caption("CLEANUP CATASTROPHE! [" + game_ver + "]")


width = height = 300
flags = SHOWN | RESIZABLE | SCALED | HWSURFACE | DOUBLEBUF | OPENGL #| FULLSCREEN

screen = pygame.display.set_mode((width, height), flags, vsync=1)
screen.fill((0, 0, 0))


from scripts.vars import Variables
from scripts.player import Player, FishRod, fish
from scripts.background import Background, Islands
from scripts.trash import Trash

# issue during exporting (bloody hell)
icon = pygame.image.load(getcwd() + "\\icon.ico")
pygame.display.set_icon(icon)

dt = pygame.time.Clock().tick(30)

run = False
# global t # for weird.glsl

from scripts.discordRPC import checkRPC
from scripts.GLcontext import *

def main():
    print(pygame.display.Info())

    run = True
    # t = 0 # for weird.glsl

    while run:
        key = pygame.key.get_pressed()

        match FishRod.isFishing:
            case False:
                if key[K_LEFT]:
                    Player.position.x -= Player.velocity * dt
                    Islands.position.x += Islands.velocity * dt
                    Player.currentSprite = Player.leftSprite
                elif key[K_RIGHT]:
                    Player.position.x += Player.velocity * dt
                    Islands.position.x -= Islands.velocity * dt
                    Player.currentSprite = Player.rightSprite
                elif key[K_DOWN]:
                    fish()
                    print(FishRod.isFishing, FishRod.position)

            case True:  # "pass" is temporary
                if FishRod.isFishing == False and FishRod.fishProcessComplete == False:
                    pass
                elif FishRod.isFishing == False and FishRod.fishProcessComplete:
                    pass
                elif FishRod.isFishing and FishRod.fishProcessComplete == False:
                    pass
                elif FishRod.isFishing and FishRod.fishProcessComplete:
                    pass

        if Player.position.x > (width - Player.currentSprite.get_width() - width * 0.02):
            Player.position.x = (
                width - Player.currentSprite.get_width() - width * 0.02)
        elif Player.position.x < (width * 0.02):
            Player.position.x = (width * 0.02)

        if Islands.position.x > (width * 0.1):
            Islands.position.x = (width * 0.1)
        elif Islands.position.x < -(width * 0.1):
            Islands.position.x = -(width * 0.1)

        # generate trash buggy - CHECK SCRAPPED VERSION - GENERATION STILL SUCKS THO

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("GAME STOP")
                pygame.quit()
                run = False
                raise SystemExit

        # t += 1 # for weird.glsl

        frame_tex = surf_to_texture(screen)
        frame_tex.use(0)
        program['tex'] = 0
        # program['time'] = t # for weird.glsl
        render_object.render(mode=moderngl.TRIANGLE_STRIP) # type: ignore

        # allSprites = pygame.sprite.Group()
        # allSprites.add(Player, FishRod, Islands, Trash)
        # screen.blit(allSprites)

        screen.blit(Background.currentSprite,
                    (Background.position.x, Background.position.y))
        screen.blit(Islands.currentSprite,
                    (Islands.position.x, Islands.position.y))
        screen.blit(Trash.currentSprite,
                    (Trash.position.x, Trash.position.y))
        screen.blit(Player.currentSprite,
                    (Player.position.x, Player.position.y))
        screen.blit(FishRod.currentSprite,
                    (FishRod.position.x, FishRod.position.y))

        frame_tex.release()
        pygame.display.flip()

        ctx.clear(0) # clear framebuffer


def setup():
    print("GAME START")

    Variables.trashCollected.total = 0
    Variables.coins = 0

    checkRPC()
    main()


if __name__ == "__main__":
    setup()
