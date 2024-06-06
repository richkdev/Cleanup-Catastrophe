from scripts.sprites.sheet import Cutter, cut_sprite_sheet, Animation
import pygame


screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

img = Cutter("assets/img/sprites/player_idletest.png")
img2 = Cutter("assets/img/sprites/player_runtest.png")

anim1 = Animation()
anim1.add_animation("idle", cut_sprite_sheet("assets/img/sprites/player_idletest.png"))
anim1.add_animation("run", cut_sprite_sheet("assets/img/sprites/player_runtest.png"))
anim1.set_action("run")
action = "idle"

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            action = "idle" if action == "run" else "run"
            anim1.set_action(action)

    anim1.update()

    img.draw(screen, (10, 10))
    img2.draw(screen, (100, 10))

    anim1.render(screen, (200, 10))

    pygame.display.flip()
    clock.tick(60)
