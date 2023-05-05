import pygame
from random import randint

class generate:    
    def Sprite():
        return "assets/img/trash/trash" + str(randint(1, 3)) + ".png"
    def Pos():
        return 600/randint(2, 5)

class Trash(pygame.sprite.Sprite):
    position = pygame.Vector2()
    position.x = generate.Pos()
    position.y = 600*.8
    rightSprite = pygame.image.load(generate.Sprite())
    rightSprite = pygame.transform.scale(rightSprite, (rightSprite.get_width()*3, rightSprite.get_height()*3))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
    visible = True
    if visible:
        currentSprite.set_alpha(255)
    elif visible == False:
        currentSprite.set_alpha(0)