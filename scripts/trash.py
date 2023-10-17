import pygame
from random import randint

class generate:
    def Sprite():
        return "assets/img/trash/trash" + str(randint(1, 3)) + ".png"

    def Pos():
        return 600/randint(2, 5)


class Trash(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = generate.Pos()
    position.y = 600*.8
    rightSprite = pygame.image.load(generate.Sprite()).convert_alpha()
    rightSprite = pygame.transform.scale(
        rightSprite, (rightSprite.get_width(), rightSprite.get_height()))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
    dirty = 1
    visible = 1
    rect = pygame.rect.Rect(
        position.x, position.y, currentSprite.get_width(), currentSprite.get_height())
