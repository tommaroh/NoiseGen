import pygame
from pygame.rect import Rect

import utils

class Player(pygame.sprite.Sprite):

    def __init__(self, position, x_resolution, y_resolution):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.image, self.rect = utils.load_png('player.png')
        self.area = screen.get_rect()
        self.position = position
        '''
        self.rect = Rect(self.position.x * 64,
                        self.position.y * 64,
                         self.position.x * 64 + 64,
                         self.position.y * 64 + 64)
        '''
        screen_x = x_resolution / 2
        screen_y = y_resolution / 2
        self.rect = Rect(screen_x,
                         screen_y,
                         screen_x + 64,
                         screen_y + 64)
        print("Rect: %s" % self.rect)
