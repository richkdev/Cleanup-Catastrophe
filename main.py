#!/usr/bin/env pythonw

import pygame
from pygame.locals import *
from sys import exit

from os import system

from vars import Variables
from player import Player, FishRod, fish
from background import Background, Islands
from trash import generate, Trash

game_ver = "v.ALPHA.0.5.0"
pygame.display.set_caption("CLEANUP CATASTROPHE! [" + game_ver + "]")

width = height = 600
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))

icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
dt = clock.tick(30)

run = False

def main():
    run = True

    while run:
        key = pygame.key.get_pressed()

        # if FishRod.isFishing == False:
        if key[K_LEFT]:
            Player.position.x -= Player.velocity * dt
            Islands.position.x += Islands.velocity * dt
            Player.currentSprite = Player.leftSprite
        elif key[K_RIGHT]:
            Player.position.x += Player.velocity * dt
            Islands.position.x -= Islands.velocity * dt
            Player.currentSprite = Player.rightSprite
        elif key[K_DOWN] or key[MOUSEBUTTONDOWN]:
            collideTrash = pygame.sprite.Group()
            collideTrash.add(Trash())
            fish(FishRod, Player, collideTrash)
        
        elif FishRod.isFishing:
            if FishRod.fishProcessComplete == False:
                FishRod.visible = 0
            elif FishRod.fishProcessComplete:
                FishRod.isFishing = False
                FishRod.visible = True
            
        if Player.position.x > (width - Player.currentSprite.get_width() - width * 0.02):
            Player.position.x = (width - Player.currentSprite.get_width() - width * 0.02)
        elif Player.position.x < (width * 0.02):
            Player.position.x = (width * 0.02)

        if Islands.position.x > (width * 0.1):
            Islands.position.x = (width * 0.1)
        elif Islands.position.x < -(width * 0.1):
            Islands.position.x = -(width * 0.1)

        screen.blit(Background.currentSprite, (Background.position.x, Background.position.y))
        screen.blit(Islands.currentSprite, (Islands.position.x, Islands.position.y))
        screen.blit(Trash.currentSprite, (Trash.position.x, Trash.position.y))
        screen.blit(Player.currentSprite, (Player.position.x, Player.position.y))
        screen.blit(FishRod.currentSprite, (FishRod.position.x, FishRod.position.y))

        #generate trash buggy aaaaaaaaaa

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("GAME STOP")
                pygame.quit()
                exit()

        trashGroup = pygame.sprite.Group()

#        allSprites = pygame.sprite.Group(Player, FishRod, Islands, trashGroup)

        pygame.display.flip()

def setup():
    system("cls||clear")
    print("GAME START")

    Variables.trashCollected.total = 0
    Variables.coins = 0

    main()

if __name__ == "__main__": setup()