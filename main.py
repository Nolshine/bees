from random import choice, random

import pygame
from pygame.locals import *

from image_manager import ImageManager
from engine import Engine
from buildings import Hive, Flower
from creatures import Bee
from ui import Button
import world
from globals import *

# init
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)

game_bg = pygame.surface.Surface(GAME_AREA)
game_fg = pygame.surface.Surface(GAME_AREA)
menu_bar = pygame.surface.Surface(MENU_AREA)

clock = pygame.time.Clock()

image_manager = ImageManager()
image_names = [
    "button",
    "button_hl",
    "grass",
    "dirt",
    "hive",
    "flower",
    "bee",
]
image_manager.load_from_names(image_names)
engine = Engine( # Creatures, buildings and buttons populated after initiliazation
    screen,
    game_fg,
    game_bg,
    menu_bar,
    image_manager,
    # creatures,
    # buildings,
    # buttons,
)

# TODO: World generation should probably be handled in a class
# generating the world
worldmap = world.generate(WORLD_WIDTH, WORLD_HEIGHT)
init_flower_locations = []

# calculate viable flower locations
for col in range(WORLD_WIDTH):
    for row in range(WORLD_HEIGHT):
        if worldmap[row][col] > 0.0:
            worldmap[row][col] = 1.0
            init_flower_locations.append((col, row))

# render grass and dirt tiles to background
engine.render_background(worldmap)

# create buttons
engine.buttons.append(Button(
    pygame.Rect(5, MENU_AREA[1]/2-16, 96, 32), "Birth bees"
))

# put hive in the middle of the map
tilex = round((len(worldmap[row]) - 1) / 2)
tiley = round((len(worldmap) - 1)/2)
hive = Hive(tilex, tiley)
engine.buildings.append(hive)

# TESTING: create a bee and make it travel from the corner to the hive
engine.creatures.append(Bee(0, 0, hive.area.center))

# Generate 10 flowers, while avoiding the hive
for location in init_flower_locations:
    x, y = (location[0] * TILE_SIZE, location[1] * TILE_SIZE)
    if hive.area.collidepoint(x, y):
        init_flower_locations.remove(location)
for i in range(10):
    location = choice(init_flower_locations)
    engine.buildings.append(Flower(location[0], location[1]))
    

# game data
food_in_hive = 10
bees_in_hive = 0
queen_health = 100

game_running = True

while game_running:
    time_passed = clock.tick(60)

    going = engine.handle_events()
    engine.update_creatures()
    pygame.display.set_caption("Queen health: " + str(queen_health) + "% | Food: " + str(food_in_hive) + " | Bees: " +
                                   str(bees_in_hive) + " available in hive.")
    engine.render_all()
    pygame.display.update()

    if not going:
        break

pygame.quit()