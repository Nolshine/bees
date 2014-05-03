from random import random
from random import choice



def smooth(world, location, num):
    #check if I'm in a corner or next to a wall:
    top, bottom, left, right = False, False, False, False
    ymax = len(world)-1
    xmax = len(world[0])-1
    if location[0] == 0:
        top = True
    elif location[0] == ymax:
        bottom = True
    if location[1] == 0:
        left = True
    elif location[1] == xmax:
        right = True

    if not top:
        if (not left) and world[location[0]-1][location[1]-1] < num-1:
            world[location[0]-1][location[1]-1] = num-1
        if world[location[0]-1][location[1]] < num-1:
            world[location[0]-1][location[1]] = num-1
        if (not right) and  world[location[0]-1][location[1]+1] < num-1:
            world[location[0]-1][location[1]+1] = num-1

    if (not left) and world[location[0]][location[1]-1] < num-1:
        world[location[0]][location[1]-1] = num-1
    if (not right) and world[location[0]][location[1]+1] < num-1:
        world[location[0]][location[1]+1] = num-1

    if not bottom:
        if (not left) and (world[location[0]+1][location[1]-1] < num-1):
            world[location[0]+1][location[1]-1] = num-1
        if world [location[0]+1][location[1]] < num-1:
            world [location[0]+1][location[1]] = num-1
        if (not right) and world[location[0]+1][location[1]+1] < num-1:
            world[location[0]+1][location[1]+1] = num-1

def rough(world):
    val = [-1, 1]
    for row in range(len(world)):
        for col in range(len(world[0])):
            yes = (random() > 0.49)
            if yes:
                world[row][col] += choice(val)
                if world[row][col] < 0:
                    world[row][col] = 0
                elif world[row][col] > 9:
                    world[row][col] = 9

def cutoff(world, threshold):
    for row in range(len(world)):
        for col in range(len(world[0])):
            if world[row][col] < threshold:
                world[row][col] = 0
            else:
                world[row][col] = 9
    

def generate(height, width):
    base = [(0, 0.97), (9, 1)]
    worldmap = []
    for row in range(height):
        worldmap.append([])
        for col in range(width):
            choice = random()
            for item in base:
                if choice <= item[1]:
                    worldmap[row].append(item[0])
                    break
    for i in range(9, 0, -1):
        for row in range(len(worldmap)):
            for col in range(len(worldmap[row])):
                if worldmap[row][col] == i:
                    smooth(worldmap, (row, col), i)

    rough(worldmap)

    cutoff(worldmap, 7)

    return worldmap
    
    
    

if __name__ == "__main__":
    
    tiles = {0:" ", 1:".", 2:",", 3:"+", 4:"n", 5:"x", 6:"%", 7:"X", 8:"@", 9:"#"} 
    worldmap = generate(40,60)
            


    for row in worldmap:
        printrow = ""
        for col in row:
            printrow += tiles[col]
    ##        printrow += str(col)
        print printrow
