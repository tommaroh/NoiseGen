from src.tilemap import TileMap

class World():

    def __init__(self, width, height, level):

        self.world = [] #2D array of Tiles
        self.tilemap = None #ref to TileMap
        self.width = width
        self.height = height
        self.level = level
        self.generate()

    def generate(self):

        self.tilemap = TileMap(self.level)

        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(x, y, self.tilemap.tilegrid[x][y], [], [])
                row.append(tile)
            self.world.append(row)

    def get_world(self):
        return self.world

    def get_tiles(self):
        return self.tilemap.tilegrid

    def get_tile(self, x, y):
        return self.tilemap.getTile(x, y)

class Tile():

    def __init__(self, x, y, terrain, items, creatures):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items = items
        self.creatures = creatures





