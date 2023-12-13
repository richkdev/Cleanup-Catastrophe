#! /usr/bin/env python3

import asyncio
from pygame.locals import * # type: ignore
import pygame

game_ver = "v.ALPHA.1.0.0"
pygame.display.set_caption("CLEANUP CATASTROPHE! [" + game_ver + "]")


width = height = 300
flags = SHOWN | RESIZABLE | SCALED | HWSURFACE | DOUBLEBUF #| OPENGL | FULLSCREEN

screen = pygame.display.set_mode((width, height), flags, vsync=1)
screen.fill((0, 0, 0))


from scripts.vars import Variables
from scripts.player import Player, FishRod, fish
from scripts.background import Background, Islands
from scripts.trash import Trash

icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)

dt = pygame.time.Clock().tick(30)

run = False

# from scripts.discordRPC import checkRPC
# from scripts.GLcontext import *

async def main():
    print(pygame.display.Info())

    run = True

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

            case True:  # will be fixed later
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

        pygame.display.flip()
        await asyncio.sleep(0)


def setup():
    print("GAME START")

    Variables.trashCollected.total = 0
    Variables.coins = 0

    asyncio.run(main())


if __name__ == "__main__":
    setup()
