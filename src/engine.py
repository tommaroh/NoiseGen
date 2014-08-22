import math
import random

import pygame
from pygame import locals

import time
import utils
from src.player import Player
from src.coord import Coord
from src.world import World
from src.coordinator import Coordinator
from src.tilemap import OPEN, WALL

DEBUG = False

def make_world(level):
    print("Init World")
    map = World(81, 81, level)
    return map

def make_player(world):
    print("Init Player")

    '''
    position = Coord(8, 6)
    player = Player(position)
    print("Position: %s" % position)
    return player
    '''
    while True:
        x = random.randint(0, world.width)
        y = random.randint(0, world.height)
        if world.get_tile(x, y) == OPEN:
            position = Coord(4, 4)
            player = Player(position)
            print("Position: %s" % position)
            return player

class Engine():
    def __init__(self):
        self._running = True
        self._screen = None
        self.world = None
        self._player = None
        self.runner = None
        self._green = None
        self._brown = None
        self._grey = None
        self._player_sprite = None

    def init(self):

        # init Screen
        pygame.init()
        self._screen = pygame.display.set_mode((1024, 768), pygame.HWSURFACE)
        pygame.display.set_caption('Pocket Quest')

        # init settings
        pygame.key.set_repeat(250, 100)

        # fill background
        self.background = pygame.Surface(self._screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        pygame.display.flip()

        # load textures
        self._green, rect = utils.load_png("green.png")
        self._brown, rect = utils.load_png("brown.png")
        self._grey, rect = utils.load_png("grey.png")
        # self._player_sprite, rect = utils.load_png('tree.png')

        # init world
        self.world = make_world(1)
        self._player = make_player(self.world)
        self.runner = Coordinator(self.world, self._player)

        # make sprite groups
        self.allgroup = pygame.sprite.Group(self._player)
        # self.playergroup = pygame.sprite.Group()
        # Player.groups = self.allgroup, self.playergroup

    def on_event(self, event):

        if event.type == locals.QUIT:
            self._running = False
        elif event.type == locals.KEYDOWN:
            # print("Keydown")
            if event.key == locals.K_RIGHT:
                self.runner.move_player(1, 0)
                # self._player.move_right()
            if event.key == locals.K_LEFT:
                self.runner.move_player(-1, 0)
                # self._player.move_left()
            if event.key == locals.K_UP:
                self.runner.move_player(0, -1)
                # self._player.move_up()
            if event.key == locals.K_DOWN:
                self.runner.move_player(0, 1)
                # self._player.move_down()

    def on_loop(self):
        pass

    def on_render(self):

        screen_width = 16
        screen_height = 12

        map_width = self.world.width
        map_height = self.world.height

        y_start = self._player.position.y - 6
        y_end = self._player.position.y + 6

        #print("x: %s -> %s (%s)" % (x_start, x_end, x_end - x_start))
        #print("y: %s -> %s (%s)" % (y_start, y_end, y_end - y_start))

        self._screen.fill((0, 0, 0))
        screen_y = 0
        if (y_start < 0):
            screen_y = 64 * abs(y_start)
            y_start = 0
        if (y_end > map_height):
            y_end = map_height
        for row in self.world.get_world()[y_start:y_end]:
            x_start = self._player.position.x - 8
            x_end = self._player.position.x + 8
            screen_x = 0
            if (x_start < 0):
                screen_x = 64 * abs(x_start)
                x_start = 0
            if (x_end > map_width):
                x_end = map_width
            #print("tiles: %s" % len(row[x_start:x_end]))
            for tile in row[x_start:x_end]:
                if tile.terrain == OPEN:
                    image = self._green
                if tile.terrain == WALL:
                    image = self._brown
                self._screen.blit(image, (screen_x, screen_y))
                screen_x += 64
            screen_y += 64
        #print("Screen: %s x %s" % (screen_x, screen_y))

        # self.allgroup.clear(self._screen, self.background)
        self.allgroup.update()
        self.allgroup.draw(self._screen)
        pygame.display.flip()

        # self._screen.blit(self.background, self._player.rect, self._player.rect)
        # self._player.update()
        # self._player.draw(self._screen)
        # pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def run(self):

        self._running = True
        # event loop!
        while (self._running):
            # set clock to 60 fps
            clock = pygame.time.Clock()
            if DEBUG:
                clock.tick(1)
            else:
                clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

