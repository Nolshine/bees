#bees
import pygame
from pygame.locals import *

import world

#global parameters
WORLD_SIZE = (37, 25)
SCREEN_SIZE = (WORLD_SIZE[0]*16, (WORLD_SIZE[1]+3)*16)
GAME_AREA = (WORLD_SIZE[0]*16, WORLD_SIZE[1]*16)
MENU_AREA = (WORLD_SIZE[0]*16, 3*16)

#initialization
pygame.init()
#main window
screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
#game surface
game_bg = screen.subsurface((0, 0, GAME_AREA[0], GAME_AREA[1]))
game_fg = screen.subsurface((0, 0, GAME_AREA[0], GAME_AREA[1]))
#menu surface
menu_bar = screen.subsurface((0, WORLD_SIZE[1]*16, WORLD_SIZE[0]*16, 3*16))

clock = pygame.time.Clock()

#game objects
class Thing:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

#game functions
def render_all():
    global screen
    global game_bg
    global game_fg
    global menu_bar

    screen.fill((0,0,0))
    menu_bar.fill((255,255,255))
        

#testing
##for row in range(WORLD_SIZE[1]):
##    printrow = ""
##    for col in range(WORLD_SIZE[0]):
##        if worldmap[row][col] == 1:
##            printrow += "#"
##        else:
##            printrow += " "
##    print printrow

#game init
going = True

worldmap = world.generate(WORLD_SIZE[1], WORLD_SIZE[0])
for row in range(WORLD_SIZE[1]):
    for col in range(WORLD_SIZE[0]):
        if worldmap[row][col] > 0:
            worldmap[row][col] = 1
            
#main loop
try:
    while going:
        time_passed = clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                print "exit"
                going = False
            elif event.type == QUIT:
                print "exit"
                going = False
        render_all()
        pygame.display.update()
        if not going:
            break
    pygame.quit()
except KeyboardInterrupt:
    pygame.quit()
    print 'something happened'
