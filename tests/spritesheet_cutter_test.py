import pygame
from scripts.settings import *
from scripts.sprites.sheet import cutSheet, Sheet

screen = pygame.display.set_mode((300, 200))
clock = pygame.time.Clock()

anim1 = Sheet()
anim1.add_animation("idle", cutSheet(newPath("assets/img/sprites/paul_run.png"), pygame.math.Vector2(31, 43)))
anim1.set_action(action="idle")

while True:
    screen.fill((255, 255, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    anim1.update()
    screen.blit(anim1.draw(), (10, 10))

    pygame.display.flip()
    clock.tick(30)
