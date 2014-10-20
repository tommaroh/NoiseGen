import math
import pygame
from noise import snoise2, snoise3
import random
import time

height = 600
width = 800

#height = 5000
#width = 5000

x_resolution = 800
y_resolution = 600

octaves = 5
freq = 100.0 * octaves
persistence = float(0.5)
lacunarity = float(2.2)


'''
octaves = 5-7
freq = 100.0 * octaves
persistence = float(0.5)
lacunarity = float(2) - 2.5
'''

def get_map():

    max = 0
    min = 10
    z = random.randint(0, 10000)
    print("Seed: %s" % z)
    map = []
    for y in range(height):
        row = []
        for x in range(width):
            #noise_value = snoise2(x / freq, y / freq, octaves, persistence, lacunarity)
            noise_value = snoise2(x / freq, y / freq, octaves, persistence, lacunarity, base=z)
            row.append(noise_value)
            if noise_value > max:
                max = noise_value
            if noise_value < min:
                min = noise_value
        map.append(row)
    print("Max: %s" % max)
    print("Min: %s" % min)
    return map

def run():


    pygame.init()
    screen = pygame.display.set_mode((x_resolution, y_resolution), pygame.HWSURFACE)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    pygame.display.flip()
    for i in range(10):
        map  = get_map()
        draw(screen, map)

def draw(screen, map):


    x_jump = width / x_resolution
    y_jump = height / y_resolution

    y_index = 0
    y = 0

    red = 0
    blue = 0
    green = 0

    while y_index < height:
        x = 0
        x_index = 0
        while x_index < width:
            tile = map[y][x]
            if tile <= 0:
                color = (0, 0, 255 - (abs(tile) * 255))
            else:
                base = tile * 255
                green = base
                color = (red, green, blue)
            screen.fill(color, rect=(x, y, 1, 1))
            x_index += x_jump
            x += 1
        y_index += y_jump
        y += 1

    pygame.display.flip()
    time.sleep(3)

if __name__ == "__main__":
    run()


'''

if tile <= 100:
    red = base / 2
    green = base / 2
else tile <= 200:
    red = 50 - ((base - 100) / 2)
    green = 50 + ((base - 100) * 2)
else:
    red = 0
    green = 255 - base

'''