import pygame

class Background(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = 0
    position.y  = 0
    currentSprite = pygame.image.load("assets/img/background/bg.png")
    currentSprite = pygame.transform.scale(currentSprite, (currentSprite.get_width()*2, currentSprite.get_height()*2))

class Islands(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = 0
    position.y  = 600/6
    velocity = .05
    currentSprite = pygame.image.load("assets/img/background/islands.png")
    currentSprite = pygame.transform.scale(currentSprite, (currentSprite.get_width()*2, currentSprite.get_height()*2))