import pygame
from noise import snoise2, pnoise2
import random
import time
import sys

height = 600
width = 800

x_resolution = 800
y_resolution = 600

class Tile():

    '''
    Represents an individual square in the world.
    '''

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.water = 0
        self.height = None

    def __str__(self):
        return "%s, %s" % (self.x, self.y)

class Map():

    '''
    Class to hold a 2 dimensional list of tiles, representing the map.
    '''
    def __init__(self, tiles):
        self.tiles = tiles
        self.width = len(tiles[0])
        self.height = len(tiles)
        print("Init Map @ %s x %s" % (self.width, self.height))

    def get(self, x, y):
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return self.tiles[y][x]

    def get_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                yield self.tiles[y][x]

def get_noise_map(octaves, persistence, lacunarity):
    '''
    This builds a Map object generated using the given noise parameters.
    octaves (int): higher number gives fewer, more dominant features
    persistence (float): higher number makes the features more broken up
    lacunarity (float): higher number generates more detail and makes the map more spiney 
    '''

    freq = 100.0 * octaves

    z = random.randint(0, 10000)
    print("Base Seed: %s" % z)
    map = []
    for y in range(height):
        row = []
        for x in range(width):
            noise_value = snoise2(x / freq, y / freq, octaves, persistence, lacunarity, base=z)
            row.append(noise_value)
        map.append(row)
    return map

def build_map():

    # get a "base" map with big features and very little detail.
    base = get_noise_map(5, 1.5, 1)
    # get a noisier map with few big features but a lot of little detail.
    terrain = get_terrain_map(5, 0.5, 3.0)
    map = []
    # scale the high detail map down and overlay it on top of the base map.
    for y in range(height):
        row = []
        for x in range(width):
            new_val = base[y][x] * 0.5 + terrain[y][x] * 0.5
            tile = Tile(x, y, new_val)
            row.append(tile)
        map.append(row)
    return Map(map)

def normalize_map(map):

    #normalize the map values
    max_val = 0
    min_val = 0
    # figure out the current max and min height values of the map
    for tile in map.get_tiles():
        if tile.value > max_val:
            max_val = tile.value
        if tile.value < min_val:
            min_val = tile.value
    
    pos_factor = 1 / max_val
    neg_factor = 1 / abs(min_val)
    #scale the map such that the highest value is at 1 and the lowest value is at -1
    for tile in map.get_tiles():
        if tile.value >= 0:
            tile.value = min(1, pos_factor * tile.value)
        else:
            tile.value = max(-1, neg_factor * tile.value)

    # rainfall function still needs some work.
    #rainfall(map)
    return map

def rainfall(map):

    # let it rain
    longest = 0
    iterations = 10000
    rivers = []
    for i in range(iterations):
        if i % (iterations / 10) == 0:
            print(str(i / (iterations/10)))
        x = random.randint(0, map.width - 1)
        y = random.randint(0, map.height - 1)
        count = runoff(map, x, y, 0)
        rivers.append(count)
        if count > longest:
            longest = count
    print("Longest River: %s" % longest)
    average = float(sum(rivers))/len(rivers) if len(rivers) > 0 else float('nan')
    print("Average River: %s" % average)

def runoff(map, x, y, count, momentum=None):

    count += 1
    if count == (sys.getrecursionlimit() - 10):
        return count
    #print("Runoff: %s" % count)
    tile = map.get(x, y)
    neighbors = find_lowest_neighbor(map, x, y, momentum)
    if not neighbors:
        #print("No low neighbors")
        return count
    for neighbor in neighbors:
        difference = tile.value - neighbor.value
        amount = difference / 2
        tile.value -= amount
        tile.water += 1
        if neighbor.value <= 0:
            #print("Runoff To Water")
            neighbor.value += amount
            return count
        momentum = ""
        if neighbor.y > tile.y:
            momentum += "North"
        if neighbor.y < tile.y:
            momentum += "South"
        if neighbor.x > tile.x:
            momentum += "East"
        if neighbor.x < tile.x:
            momentum += "West"
        if count > 9000:
            print("Tile: %s" % tile)
            print("Neighbor: %s" % neighbor)
            print("Momentum: %s" % momentum)
        return runoff(map, neighbor.x, neighbor.y, count, momentum)

def find_lowest_neighbor(map, x, y, momentum=None):
    '''
    Given some x,y coordinate, find it's neighbor with the lowest height.
    '''

    tile = map.get(x, y)
    candidates = []
    x_mod = [-1, 0, +1]
    y_mod = [-1, 0, +1]
    momentum = momentum or ''
    if "North" in momentum:
        y_mod = [0, 1]
    if "South" in momentum:
        y_mod = [-1, 0]
    if "East" in momentum:
        x_mod = [0, 1]
    if "West" in momentum:
        x_mod = [-1, 0]
    for i in x_mod:
        for j in y_mod:
            neighbor = map.get(x + i, y + j)
            if neighbor and neighbor != tile:
                if neighbor.value <= tile.value:
                    candidates.append(neighbor)
    if candidates:
        return candidates
    else:
        return None

def draw(screen, map):

    x_jump = width / x_resolution
    y_jump = height / y_resolution

    y_index = 0
    y = 0

    max_water = 0
    max_value = 0
    for tile in map.get_tiles():
        if tile.water > max_water:
            max_water = tile.water

    print("Max Water: %s" % max_water)
    water_scale = float(255) / max_water

    while y_index < height:
        x = 0
        x_index = 0
        while x_index < width:

            red = 0
            blue = 0
            green = 0

            value = map.get(x, y).value
            #water = map.get(x, y).water
            if value <= 0:
                # underwater, color blue
                blue = 255 - (abs(value) * 255)
                color = (0, 0, blue)
            else:
                # land, color green
                #red = water * water_scale
                green = value * 255
                color = (0, green, 0)
            try:
                screen.fill(color, rect=(x, y, 1, 1))
            except:
                print("Bad Tile: %s,%s - %s" % (x_index, y_index, (str(color))))
            x_index += x_jump
            x += 1
        y_index += y_jump
        y += 1

    pygame.display.flip()
    time.sleep(5)

def run():

    pygame.init()
    screen = pygame.display.set_mode((x_resolution, y_resolution), pygame.HWSURFACE)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    pygame.display.flip()
    for i in range(3):
        print("--------------")
        map = build_map()
        map = normalize_map(map)
        draw(screen, map)

if __name__ == "__main__":
    run()
