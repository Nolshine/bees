#bees
from math import sqrt
from random import choice, random

import pygame
from pygame.locals import *

import world

#global parameters
TILE_SIZE = 32
WORLD_SIZE = (30, 17)
MENU_HEIGHT = 2
SCREEN_SIZE = (WORLD_SIZE[0]*TILE_SIZE, (WORLD_SIZE[1]+MENU_HEIGHT)*TILE_SIZE)
GAME_AREA = (WORLD_SIZE[0]*TILE_SIZE, WORLD_SIZE[1]*TILE_SIZE)
MENU_AREA = (WORLD_SIZE[0]*TILE_SIZE, MENU_HEIGHT*TILE_SIZE)
MAX_BEES = 200

#initialization
pygame.init()
#main window
screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
#game surface
game_bg = pygame.surface.Surface((GAME_AREA[0], GAME_AREA[1]))
game_fg = pygame.surface.Surface((GAME_AREA[0], GAME_AREA[1]))
#menu surface
menu_bar = pygame.surface.Surface((WORLD_SIZE[0]*TILE_SIZE,
                                  MENU_HEIGHT*TILE_SIZE))

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

class Button:
    def __init__(self, area, text, function=None):
        self.area = area #use a rect
        self.text = text
        self.function = function

#make an Imager object
#load tiles and sprites
loader = Imager()
loader.load("button", "button.png")
loader.load("button_hl", "button_hl.png")
loader.load("grass", "grass.png")
loader.load("dirt", "dirt.png")
loader.load("hive", "hive.png")
loader.load("flower", "flower.png")
loader.load("bee", "bee.png")

#game objects
class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Bee(Creature):
    def __init__(self, x, y, dest):
        Creature.__init__(self, x, y)
        self.sprite = "bee"
        self.area = pygame.Rect(self.x-2, self.y-2, 4, 4)
        self.nectar = 0
        self.velocity = 0.0
        self.dest = dest

    def move_to_dest(self):
        #calculate the vector to the target
        dx = self.dest[0] - self.x
        dy = self.dest[1] - self.y
        dist = sqrt(dx**2 + dy**2)
        
        #use the magnitude to normalize the x/y components of the vector
        dx /= dist
        dy /= dist
        
        #move using velocity factor, and update the area variable
        dx *= self.velocity
        dy *= self.velocity
        self.move(dx, dy)
        self.area.x = self.x-2
        self.area.y = self.y-2

    def update(self):
        if self.x != self.dest[0] and self.y != self.dest[1]:
            if self.velocity < 2:
                self.velocity += 0.01
            self.move_to_dest()

class Building:
    def __init__(self, tilex, tiley, area):
        self.x = tilex
        self.y = tiley
        self.area = area #use a Rect

class Hive(Building):
    def __init__(self, tilex, tiley):
        global TILE_SIZE
        area = pygame.Rect(tilex*TILE_SIZE, tiley*TILE_SIZE,
                           2*TILE_SIZE, 2*TILE_SIZE)
        Building.__init__(self, tilex, tiley, area)
        self.sprite = "hive"

class Flower(Building):
    def __init__(self, tilex, tiley):
        global TILE_SIZE
        area = pygame.Rect(tilex*TILE_SIZE, tiley*TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)
        Building.__init__(self, tilex, tiley, area)
        self.sprite = "flower"
        self.nectar = int(round(random()*15))

    def take_nectar(self, value):
        after = self.nectar - value
        if after < 0:
            self.nectar = 0
            return value + after
        else:
            return value

#game functions
def render_all():
    global screen
    global game_bg
    global game_fg
    global menu_bar
    global members
    global buttons
    global loader

    game_fg.blit(game_bg, (0, 0))
    if members["buildings"] != []:
        for building in members["buildings"]:
            game_fg.blit(loader.use(building.sprite), building.area)
    if members["creatures"] != []:
        for creature in members["creatures"]:
            game_fg.blit(loader.use(creature.sprite), creature.area)
            
    screen.blit(game_fg, (0,0))
    menu_bar.fill((0,0,0))
    for button in buttons:
        render_button(button)
    screen.blit(menu_bar, (0, GAME_AREA[1]))

def render_button(button):
    global menu_bar

    #render button background
    image = loader.use("button")
    image = pygame.transform.smoothscale(image, (button.area.width, button.area.height))
    menu_bar.blit(image, button.area)
    
    #checking for mouseover:
    #get absolute mouse position on screen
    mouse_pos = pygame.mouse.get_pos()
    #calculate mosue position relative to the top of the menu bar
    #by subtracting GAME_AREA's y values
    pos = [mouse_pos[0], mouse_pos[1]-GAME_AREA[1]]
    #check collision against button's area using the relative position
    if button.area.collidepoint(pos):
        #if there's collision, the mouse is over the button, so we highlight
        #it using the button_hl sprite
        image = loader.use("button_hl")
        image = pygame.transform.smoothscale(
            image,
            (button.area.width, button.area.height)
            )
        menu_bar.blit(image, button.area)

    #now I'll render the text on top, in black
    font = pygame.font.Font(None, 22)
    text = font.render(button.text, 0, (0, 0, 0))
    textpos = text.get_rect()
    textpos.center = button.area.center
    menu_bar.blit(text, textpos)
        

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

#generate a map and prepare to store viable flower locations
worldmap = world.generate(WORLD_SIZE[1], WORLD_SIZE[0])
init_flower_locations = []

#convet map values, prepare world sprite and add grassy tiles to
#viable flower locations list.
for row in range(WORLD_SIZE[1]):
    for col in range(WORLD_SIZE[0]):
        if worldmap[row][col] > 0:
            worldmap[row][col] = 1
            game_bg.blit(loader.use("grass"), (col*TILE_SIZE, row*TILE_SIZE))
            init_flower_locations.append((col, row))
        else:
            game_bg.blit(loader.use("dirt"), (col*TILE_SIZE, row*TILE_SIZE))

#create buttons
buttons = []
buttons.append(Button(pygame.Rect(5, MENU_AREA[1]/2-16, 96, 32), "Birth bees"))
            
#get ready to store game units
members = {"buildings":[],"creatures":[]}

#hive goes as near the middle as possible
tilex = round((len(worldmap[row])-1)/2)
tiley = round((len(worldmap)-1)/2)
hive = Hive(tilex, tiley)
members["buildings"].append(hive)

#put a bee for testing and make it go from one end of the map to the other
members["creatures"].append(Bee(0, 0, (hive.area.center)))

#put 10 flowers down
for i in range(10):
    if init_flower_locations == []:
        break
    location = choice(init_flower_locations)
    while True:
        if hive.area.collidepoint((location[0]*TILE_SIZE, location[1]*TILE_SIZE)):
            init_flower_locations.remove(location)
            location = choice(init_flower_locations)
            print "rejected hive/flower conflict"
        else:
            break
    init_flower_locations.remove(location)
    members["buildings"].append(Flower(location[0], location[1]))
    
#initialize some game session data.
food_in_hive = 10
bees_in_hive = 0
queen_health = 100

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

        if members["creatures"] != []:
            for creature in members["creatures"]:
                creature.update()
                
        pygame.display.set_caption("Queen health: " + str(queen_health) + "% | Food: " + str(food_in_hive) + " | Bees: " +
                                   str(bees_in_hive) + " available in hive.")
        render_all()
        
        pygame.display.update()
        
        if not going:
            break
        
    pygame.quit()
except KeyboardInterrupt:
    pygame.quit()
    print 'something happened'
