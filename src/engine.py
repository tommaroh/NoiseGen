import pygame
from pygame import locals

import utils
from src.player import Player
from src.coordinator import Coordinator
from src.map import OPEN, WALL, Map

DEBUG = False

def make_world(level):
    print("Init World")
    return Map(level)

def make_player(map, x_resolution, y_resolution):
    print("Init Player")
    position = map.getEntrance()
    player = Player(position, x_resolution, y_resolution)
    print("Position: %s" % position)
    return player

class Engine():
    def __init__(self):
        self._running = True
        self._screen = None
        self.map = None
        self._player = None
        self.runner = None
        self._green = None
        self._brown = None
        self._grey = None
        self._error = None
        self.x_resolution = 1024
        self.y_resolution = 768
        self._player_sprite = None

    def init(self):

        # init Screen
        pygame.init()
        self._screen = pygame.display.set_mode((self.x_resolution, self.y_resolution), pygame.HWSURFACE)
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
        self._error, rect = utils.load_png("tree.png")
        # self._player_sprite, rect = utils.load_png('tree.png')

        # init world
        self.map = make_world(1)
        self._player = make_player(self.map, self.x_resolution, self.y_resolution)
        self.runner = Coordinator(self.map, self._player)

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

        # 16x12 @ 1024x768
        screen_width = self.x_resolution / 64
        screen_height = self.y_resolution / 64

        x_buffer = screen_width / 2
        y_buffer = screen_height / 2

        map_width = self.map.width
        map_height = self.map.height

        x_start = self._player.position.x - x_buffer
        x_end = self._player.position.x + x_buffer

        # print("x: %s -> %s (%s)" % (x_start, x_end, x_end - x_start))
        # print("y: %s -> %s (%s)" % (y_start, y_end, y_end - y_start))

        self._screen.fill((0, 0, 0))
        screen_x = 0
        if (x_start < 0):
            screen_x = 64 * abs(x_start)
            x_start = 0
        if (x_end > map_width):
            x_end = map_width
        for row in self.map.getTiles()[x_start:x_end]:
            y_start = self._player.position.y - y_buffer
            y_end = self._player.position.y + y_buffer
            screen_y = 0
            if (y_start < 0):
                screen_y = 64 * abs(y_start)
                y_start = 0
            if (y_end > map_width):
                y_end = map_width
            #print("tiles: %s" % len(row[x_start:x_end]))
            image = self._error
            for tile in row[y_start:y_end]:
                if tile.terrain == OPEN:
                    image = self._green
                if tile.terrain == WALL:
                    image = self._brown
                self._screen.blit(image, (screen_x, screen_y))
                screen_y += 64
            screen_x += 64
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

