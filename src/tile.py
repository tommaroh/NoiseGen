from src.base import Base
from src.map import WALL

class Tile(Base):
    def __init__(self, x, y, terrain=-1, items=None, creatures=None):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items = items
        self.creatures = creatures

    def isBlocked(self):
        if self.terrain == WALL:
            return True
        else:
            return False

    def __str__(self):
        return str(self.terrain)
