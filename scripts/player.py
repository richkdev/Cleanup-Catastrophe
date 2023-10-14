import pygame

from .vars import Variables


class Player(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = 600/4
    position.y = 600/6
    velocity = .1
    rightSprite = pygame.image.load("assets/img/user/player.png").convert_alpha()
    rightSprite = pygame.transform.scale(
        rightSprite, (rightSprite.get_width(), rightSprite.get_height()))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
    dirty = 1
    visible = 1
    rect = currentSprite.get_rect()


class FishRod(pygame.sprite.DirtySprite):
    position = pygame.Vector2()
    position.x = Player.position.x + Player.currentSprite.get_width()/1.5
    position.y = Player.position.y
    isFishing = False
    fishProcessComplete = False
    velocity = 10
    currentSprite = pygame.image.load("assets/img/user/fishrod.png").convert_alpha()
    currentSprite = pygame.transform.scale(
        currentSprite, (currentSprite.get_width(), currentSprite.get_height()))
    dirty = 1
    visible = 1
    rect = currentSprite.get_rect()


def fish():
    # todo: make it a checker function!

    if Player.currentSprite == Player.rightSprite:
        FishRod.position.x = Player.position.x + Player.currentSprite.get_width()/1.5
    elif Player.currentSprite == Player.leftSprite:
        FishRod.position.x = Player.position.x - Player.currentSprite.get_width()/7.5

    def fishAnim():  # issue: fishAnim statements only gets called once?
        print("fishAnim() called.")

        while True:
            print("in loop!")

            if FishRod.fishProcessComplete == False:
                print(FishRod.position, FishRod.visible)
                # FishRod.position.y += FishRod.velocity # TEMPORARILY DISABLED
                print(FishRod.position, FishRod.visible)

                if FishRod.position.y != (600 - FishRod.currentSprite.get_height()):
                    FishRod.fishProcessComplete = True
                    print(FishRod.position, FishRod.visible)
                    return True
                elif FishRod.position.y >= (600 - FishRod.currentSprite.get_height()):
                    FishRod.isFishing = False
                    return False

            elif FishRod.fishProcessComplete == True:
                # if FishRod.position.y != Player.position.y:
                #     FishRod.position.y -= FishRod.velocity
                # elif FishRod.position.y == Player.position.y:
                #     FishRod.visible = 0
                print("dddd")
                return False

    print("fished!", FishRod.isFishing, FishRod.visible, Player.visible, FishRod.position,
          Player.position, Variables.trashCollected.ever, FishRod.fishProcessComplete)

    # maybe add a while loop here to continue? looping
    if FishRod.isFishing:
        if fishAnim() == True:
            Variables.trashCollected.ever += 1
            Variables.trashCollected.total += 1
            print(Variables.trashCollected.ever,
                  Variables.trashCollected.total)
            print(FishRod.position, FishRod.visible)
        elif fishAnim() == False:
            FishRod.isFishing = not FishRod.isFishing
            FishRod.fishProcessComplete = False

# https://stackoverflow.com/questions/70998501/pygame-draw-multiple-duplicate-sprites-same-class/71036733#71036733
