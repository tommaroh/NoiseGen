
from src.tilemap import OPEN, WALL
class Coordinator():

    def __init__(self, map, player):

        self.map = map
        self.player = player

    def move_player(self, x, y):
        old_x = self.player.position.x
        old_y = self.player.position.y
        new_x = old_x + x
        new_y = old_y + y

        tile = self.map.get_tile(new_x, new_y)
        if tile == WALL:
            return
        else:
            if (0 <= new_x) and (new_x < self.map.width):
                #print("X: %s" % new_x)
                self.player.position.x = new_x
            else:
                print("Blocked By Boundary")

            if (0 <= new_y) and (new_y < self.map.height):
                #print("Y: %s" % new_y)
                self.player.position.y = new_y
            else:
                print("Blocked By Boundary")
