import pygame
from os import getcwd


class Background(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = 0
    position.y = 0
    currentSprite = pygame.image.load(
        getcwd() + "\\assets\\img\\background\\bg.png").convert_alpha()
    currentSprite = pygame.transform.scale(
        currentSprite, (currentSprite.get_width(), currentSprite.get_height()))


class Islands(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = 0
    position.y = 600/10
    velocity = .05
    currentSprite = pygame.image.load(
        getcwd() + "\\assets\\img\\background\\islands.png").convert_alpha()
    currentSprite = pygame.transform.scale(
        currentSprite, (currentSprite.get_width(), currentSprite.get_height()))
