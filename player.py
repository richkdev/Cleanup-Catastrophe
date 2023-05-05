import pygame

from vars import Variables

clock = pygame.time.Clock()
dt = clock.tick(30)

class Player(pygame.sprite.Sprite):
    position = pygame.Vector2()
    position.x = 600/4
    position.y  = 600/4
    velocity = .1
    rightSprite = pygame.image.load("assets/img/user/player.png")
    rightSprite = pygame.transform.scale(rightSprite, (rightSprite.get_width()*3, rightSprite.get_height()*3))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
    visible = True
    if visible:
        currentSprite.set_alpha(255)
    elif visible == False:
        currentSprite.set_alpha(0)

class FishRod(pygame.sprite.Sprite):
    position = pygame.Vector2()
    position.x = Player.position.x + Player.currentSprite.get_width()/1.5
    position.y = Player.position.y
    isFishing = False
    fishProcessComplete = False
    velocity = .2
    currentSprite = pygame.image.load("assets/img/user/fishrod.png")
    currentSprite = pygame.transform.scale(currentSprite, (currentSprite.get_width()*2, currentSprite.get_height()*2))
    visible = False
    if visible:
        currentSprite.set_alpha(255)
    elif visible == False:
        currentSprite.set_alpha(0)

def fish(a, b, c):
    if a.isFishing == False:
        a.isFishing = True
    elif a.isFishing:
        a.isFishing = not a.isFishing

    if b.currentSprite == b.rightSprite:
        a.position.x = b.position.x + b.currentSprite.get_width()/1.5
    elif b.currentSprite == b.leftSprite:
        a.position.x = b.position.x - b.currentSprite.get_width()/7.5

    print("fished!", a.isFishing, a.visible, b.visible, a.position, b.position)

    def fishAnim(a, b, c):
        while a.fishProcessComplete == False:
            a.position.y += a.velocity * dt

            if a.position.y != (600 - a.currentSprite.get_height()):
                if pygame.sprite.spritecollide(a, c, True):
                    a.fishProcessComplete == True
                    return True
            elif a.position.y >= (600 - a.currentSprite.get_height()):
                a.isFishing = False
                return False
            
            a.fishProcessComplete = True
            
            if a.fishProcessComplete == True:
                if a.position.y != b.position.y:
                    a.position.y -= a.velocity * dt
                elif a.position.y == b.position.y:
                    a.visible = False

    if fishAnim(a, b, c) == True:
        Variables.trashCollected.ever += 1
        Variables.trashCollected.total += 1
        print(Variables.trashCollected.ever, Variables.trashCollected.total)
    elif fishAnim(a, b, c) == False:
        a.isFishing = not a.isFishing
        a.fishProcessComplete = True

# https://stackoverflow.com/questions/70998501/pygame-draw-multiple-duplicate-sprites-same-class/71036733#71036733