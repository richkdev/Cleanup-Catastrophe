from scripts.states.states import *

state_stack = []
state_stack.append(Splash)

class Manager(object):
    self.screen = 


# import pygame
# from pygame import *

# WIN_WIDTH = 1120 - 320
# WIN_HEIGHT = 960 - 320
# HALF_WIDTH = int(WIN_WIDTH / 2)
# HALF_HEIGHT = int(WIN_HEIGHT / 2)

# DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
# DEPTH = 0
# FLAGS = 0
# CAMERA_SLACK = 30

# levels = {0: {'level': [
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                         E  ",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "               PPPPP        PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPP           P",
#                     "                            PPPP           P",
#                     "                            PPPP     PPPPPPP",
#                     "                      PPPPPPPPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "       PPPP                 PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "PPPPP                       PPPP     PPPPPPP",
#                     "PPP                         PPPP     PPPPPPP",
#                     "PPP                         PPPP     PPPPPPP",
#                     "PPP                         PPPP     PPPPPPP",
#                     "PPP         PPPPP           PPPP     PPPPPPP",
#                     "PPP                                     PPPP",
#                     "PPP                                     PPPP",
#                     "PPP                                     PPPP",
#                     "PPP                       PPPPPPPPPPPPPPPPPP",
#                     "PPP                       PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",],
#              'enemies': [(9, 38)]},
#              1: {'level': [
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                            ",
#                     "                                         E  ",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "               PPPPP        PPPPPPPPPPPPPPPP",
#                     "                            PPPPPPPPPPPPPPPP",
#                     "                            PPPP           P",
#                     "                            PPPP           P",
#                     "                            PPPP     PPPPPPP",
#                     "                      PPPPPPPPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "       PPPP                 PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "                            PPPP     PPPPPPP",
#                     "PPPPP                       PPPP     PPPPPPP",
#                     "PPP                  PPPPPPPPPPP     PPPPPPP",
#                     "PPP                         PPPP     PPPPPPP",
#                     "PPP                         PPPP     PPPPPPP",
#                     "PPP             PPPPPPPP    PPPP     PPPPPPP",
#                     "PPP                                     PPPP",
#                     "PPP                                     PPPP",
#                     "PPP          PPPPP                      PPPP",
#                     "PPP          P            PPPPPPPPPPPPPPPPPP",
#                     "PPP          P    PPPPPPPPPPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
#                     "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",],
#              'enemies': [(9, 38), (18, 38), (15, 15)]}}

# class State(object):
#     def __init__(self):
#         pass

#     def render(self, screen):
#         raise NotImplementedError

#     def update(self):
#         raise NotImplementedError

#     def handle_events(self, events):
#         raise NotImplementedError

# class GameState(State):
#     def __init__(self, levelno):
#         super(GameState, self).__init__()
#         self.bg = Surface((32,32))
#         self.bg.convert()
#         self.bg.fill(Color("#0094FF"))
#         up = left = right = False
#         self.entities = pygame.sprite.Group()
#         self.player = Player(5, 40)
#         self.player.state = self
#         self.platforms = []

#         self.levelno = levelno

#         levelinfo = levels[levelno]
#         self.enemies = [Enemy(*pos) for pos in levelinfo['enemies']]

#         level = levelinfo['level']
#         total_level_width = len(level[0]) * 32
#         total_level_height = len(level) * 32

#         # build the level
#         x = 0
#         y = 0
#         for row in level:
#             for col in row:
#                 if col == "P":
#                     p = Platform(x, y)
#                     self.platforms.append(p)
#                     self.entities.add(p)
#                 if col == "E":
#                     e = ExitBlock(x, y)
#                     self.platforms.append(e)
#                     self.entities.add(e)
#                 x += 32
#             y += 32
#             x = 0

#         self.camera = Camera(complex_camera, total_level_width, total_level_height)
#         self.entities.add(self.player)
#         for e in self.enemies:
#             self.entities.add(e)

#     def render(self, screen):
#         for y in range(20):
#             for x in range(25):
#                 screen.blit(self.bg, (x * 32, y * 32))

#         for e in self.entities:
#             screen.blit(e.image, self.camera.apply(e))

#     def update(self):
#         pressed = pygame.key.get_pressed()
#         up, left, right = [pressed[key] for key in (K_UP, K_LEFT, K_RIGHT)]
#         self.player.update(up, left, right, self.platforms)

#         for e in self.enemies:
#             e.update(self.platforms)

#         self.camera.update(self.player)

#     def exit(self):
#         if self.levelno+1 in levels:
#             self.manager.go_to(GameState(self.levelno+1))
#         else:
#             self.manager.go_to(CustomState("You win!"))

#     def die(self):
#         self.manager.go_to(CustomState("You lose!"))

#     def handle_events(self, events):
#         for e in events:
#             if e.type == KEYDOWN and e.key == K_ESCAPE:
#                 self.manager.go_to(TitleState())

# class CustomState(object):

#     def __init__(self, text):
#         self.text = text
#         super(CustomState, self).__init__()
#         self.font = pygame.font.SysFont('Arial', 56)

#     def render(self, screen):
#         # ugly! 
#         screen.fill((0, 200, 0))
#         text1 = self.font.render(self.text, True, (255, 255, 255))
#         screen.blit(text1, (200, 50))

#     def update(self):
#         pass

#     def handle_events(self, events):
#         for e in events:
#             if e.type == KEYDOWN:
#                 self.manager.go_to(TitleState())

# class TitleState(object):

#     def __init__(self):
#         super(TitleState, self).__init__()
#         self.font = pygame.font.SysFont('Arial', 56)
#         self.sfont = pygame.font.SysFont('Arial', 32)

#     def render(self, screen):
#         # ugly! 
#         screen.fill((0, 200, 0))
#         text1 = self.font.render('Crazy Game', True, (255, 255, 255))
#         text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
#         screen.blit(text1, (200, 50))
#         screen.blit(text2, (200, 350))

#     def update(self):
#         pass

#     def handle_events(self, events):
#         for e in events:
#             if e.type == KEYDOWN and e.key == K_SPACE:
#                 self.manager.go_to(GameState(0))

# class StateMananger(object):
#     def __init__(self):
#         self.go_to(TitleState())

#     def go_to(self, state):
#         self.state = state
#         self.state.manager = self

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
#     pygame.display.set_caption("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
#     timer = pygame.time.Clock()
#     running = True

#     manager = StateMananger()

#     while running:
#         timer.tick(60)

#         if pygame.event.get(QUIT):
#             running = False
#             return
#         manager.state.handle_events(pygame.event.get())
#         manager.state.update()
#         manager.state.render(screen)
#         pygame.display.flip()

# class Camera(object):
#     def __init__(self, camera_func, width, height):
#         self.camera_func = camera_func
#         self.state = Rect(0, 0, width, height)

#     def apply(self, target):
#         try:
#             return target.rect.move(self.state.topleft)
#         except AttributeError:
#             return map(sum, zip(target, self.state.topleft))

#     def update(self, target):
#         self.state = self.camera_func(self.state, target.rect)

# def complex_camera(camera, target_rect):
#     l, t, _, _ = target_rect
#     _, _, w, h = camera
#     l, t, _, _ = -l + HALF_WIDTH, -t +HALF_HEIGHT, w, h

#     l = min(0, l)                           # stop scrolling left
#     l = max(-(camera.width - WIN_WIDTH), l)   # stop scrolling right
#     t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling bottom

#     return Rect(l, t, w, h)

# class Entity(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)

# class Player(Entity):
#     def __init__(self, x, y):
#         Entity.__init__(self)
#         self.xvel = 0
#         self.yvel = 0
#         self.onGround = False
#         self.image = Surface((32,32))
#         self.image.fill(Color("#0000FF"))
#         self.image.convert()
#         self.rect = Rect(x*32, y*32, 32, 32)

#     def update(self, up, left, right, platforms):
#         if self.rect.top > 1440 or self.rect.top < 0:
#             self.state.die()
#         if self.rect.left > 1408 or self.rect.right < 0:
#             self.state.die()
#         if up:
#             if self.onGround:
#                 self.yvel = 0
#                 self.yvel -= 10 # only jump if on the ground
#         if left:
#             self.xvel = -10
#         if right:
#             self.xvel = 10
#         if not self.onGround:
#             self.yvel += 0.3 # only accelerate with gravity if in the air
#             if self.yvel > 80: self.yvel = 80 # max falling speed
#         if not(left or right):
#             self.xvel = 0

#         self.rect.left += self.xvel # increment in x direction
#         if self.collide(self.xvel, 0, platforms): # do x-axis collisions
#             self.rect.top += self.yvel # increment in y direction
#             self.onGround = False; # assuming we're in the air
#             self.collide(0, self.yvel, platforms) # do y-axis collisions

#     def collide(self, xvel, yvel, platforms):
#         for p in platforms:
#             if pygame.sprite.collide_rect(self, p):
#                 if isinstance(p, ExitBlock):
#                     self.state.exit()
#                     return False
#                 if xvel > 0: self.rect.right = p.rect.left
#                 if xvel < 0: self.rect.left = p.rect.right
#                 if yvel > 0:
#                     self.rect.bottom = p.rect.top
#                     self.onGround = True
#                 if yvel < 0:
#                     self.rect.top = p.rect.bottom
#         return True

# class Enemy(Entity):
#     def __init__(self, x, y):
#         Entity.__init__(self)
#         self.yVel = 0
#         self.xVel = 2 # start moving immediately
#         self.image = Surface((32,32))
#         self.image.fill(Color("#00FF00"))
#         self.image.convert()
#         self.rect = Rect(x*32, y*32, 32, 32)
#         self.onGround = False

#     def update(self, platforms):
#         if not self.onGround:
#             self.yVel += 0.3

#         # no need for right_dis to be a member of the class,
#         # since we know we are moving right if self.xVel > 0
#         right_dis = self.xVel > 0

#         # create a point at our left (or right) feet 
#         # to check if we reached the end of the platform
#         m = (1, 1) if right_dis else (-1, 1)
#         p = self.rect.bottomright if right_dis else self.rect.bottomleft
#         fp = map(sum, zip(m, p))

#         # if there's no platform in front of us, change the direction
#         collide = any(p for p in platforms if p.rect.collidepoint((fp)))
#         if not collide:
#             self.xVel *= -1

#         self.rect.left += self.xVel # increment in x direction
#         self.collide(self.xVel, 0, platforms) # do x-axis collisions
#         self.rect.top += self.yVel # increment in y direction
#         self.onGround = False; # assuming we're in the air
#         self.collide(0, self.yVel, platforms) # do y-axis collisions

#     def collide(self, xVel, yVel, platforms):
#         for p in platforms:
#             if pygame.sprite.collide_rect(self, p):
#                 if xVel > 0: 
#                     self.rect.right = p.rect.left
#                     self.xVel *= -1 # hit wall, so change direction
#                 if xVel < 0: 
#                     self.rect.left = p.rect.right
#                     self.xVel *= -1 # hit wall, so change direction
#                 if yVel > 0:
#                     self.rect.bottom = p.rect.top
#                     self.onGround = True
#                 if yVel < 0:
#                     self.rect.top = p.rect.bottom

# class Platform(Entity):
#     def __init__(self, x, y):
#         Entity.__init__(self)
#         #self.image = Surface([32, 32], pygame.SRCALPHA, 32) #makes blocks invisible for much better artwork
#         self.image = Surface((32,32)) #makes blocks visible for building levels
#         self.image.convert()
#         self.rect = Rect(x, y, 32, 32)

#     def update(self):
#         pass

# class ExitBlock(Platform):
#     def __init__(self, x, y):
#         Platform.__init__(self, x, y)
#         self.image = Surface((32,32)) #makes blocks visible for building levels
#         self.image.convert()
#         self.rect = Rect(x, y, 32, 32)




# if __name__ == "__main__":
#     main()
