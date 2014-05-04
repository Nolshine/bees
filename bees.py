#bees
from random import choice

import pygame
from pygame.locals import *

import world

#global parameters
TILE_SIZE = 32
WORLD_SIZE = (30, 17)
SCREEN_SIZE = (WORLD_SIZE[0]*TILE_SIZE, (WORLD_SIZE[1]+2)*TILE_SIZE)
GAME_AREA = (WORLD_SIZE[0]*TILE_SIZE, WORLD_SIZE[1]*TILE_SIZE)
MENU_AREA = (WORLD_SIZE[0]*TILE_SIZE, 2*TILE_SIZE)

#initialization
pygame.init()
#main window
screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
#game surface
game_bg = pygame.surface.Surface((GAME_AREA[0], GAME_AREA[1]))
game_fg = pygame.surface.Surface((GAME_AREA[0], GAME_AREA[1]))
#menu surface
menu_bar = screen.subsurface((0, WORLD_SIZE[1]*TILE_SIZE, WORLD_SIZE[0]*TILE_SIZE, 2*TILE_SIZE))

clock = pygame.time.Clock()

#engine objects
class Imager:
    def __init__(self):
        self.images = {}

    def load(self, name, image):
        if not (image in self.images):
            self.images[name] = pygame.image.load(image)
            return self.images[name]
        else:
            return self.images[name]

    def use(self, name):
        if name in self.images:
            return self.images[name]
        else:
            print "image not loaded"

#make an Imager object
#load tiles and sprites
loader = Imager()
loader.load("grass", "grass.png")
loader.load("dirt", "dirt.png")
loader.load("hive", "hive.png")
loader.load("flower", "flower.png")

#game objects
class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Building:
    def __init__(self, tilex, tiley, area):
        self.x = tilex
        self.y = tiley
        self.area = area #use a Rect

class Hive(Building):
    def __init__(self, tilex, tiley):
        global TILE_SIZE
        rect = pygame.Rect(tilex*TILE_SIZE, tiley*TILE_SIZE,
                           2*TILE_SIZE, 2*TILE_SIZE)
        Building.__init__(self, tilex, tiley, rect)
        self.sprite = "hive"

class Flower(Building):
    def __init__(self, tilex, tiley):
        global TILE_SIZE
        rect = pygame.Rect(tilex*TILE_SIZE, tiley*TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)
        Building.__init__(self, tilex, tiley, rect)
        self.sprite = "flower"

#game functions
def render_all():
    global screen
    global game_bg
    global game_fg
    global menu_bar
    global members
    global loader

    game_fg.blit(game_bg, (0, 0))
    for building in members["buildings"]:
        game_fg.blit(loader.use(building.sprite), building.area)
    screen.blit(game_fg, (0,0))
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
init_flowers = []

for row in range(WORLD_SIZE[1]):
    for col in range(WORLD_SIZE[0]):
        if worldmap[row][col] > 0:
            worldmap[row][col] = 1
            game_bg.blit(loader.use("grass"), (col*TILE_SIZE, row*TILE_SIZE))
            init_flowers.append((col, row))
        else:
            game_bg.blit(loader.use("dirt"), (col*TILE_SIZE, row*TILE_SIZE))
#get ready to store game units
members = {"buildings":[],"creatures":[]}
#hive goes as near the middle as possible
tilex = round((len(worldmap[row])-1)/2)
tiley = round((len(worldmap)-1)/2)
members["buildings"].append(Hive(tilex, tiley))
for i in range(10):
    location = choice(init_flowers)
    init_flowers.remove(location)
    members["buildings"].append(Flower(location[0], location[1]))
#put a couple of flowers down

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
