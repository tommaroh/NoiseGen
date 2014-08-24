import random
from src.coord import Coord

UNLOCKED = -1
OPEN = 0
WALL = 1

class TileMap():

    def __init__(self, level):

        self.squareSize = 3
        self.roomSize = 9
        self.roomsPerSide = 9 * level;
        self.level = level
        numTiles = self.roomsPerSide * self.roomSize

        self.xTiles = numTiles
        self.yTiles = numTiles

        print("Starting constructor")
        print("yTiles: %s" % self.yTiles)
        print("xTiles: %s" % self.xTiles)

        self.tilegrid = [[None for x in range(self.xTiles)] for y in range(self.yTiles)]
        self.roomgrid = [[None for x in range(self.roomsPerSide)] for y in range(self.roomsPerSide)]
        self.generateRooms()
        entranceQuadrant = random.randint(1, 4)
        self.entrance = self.generateObject(entranceQuadrant)
        exitQuadrant = random.randint(1, 4)
        while exitQuadrant == entranceQuadrant:
            exitQuadrant = random.randint(1, 4)
        self.exit = self.generateObject(exitQuadrant)
        self.textDraw()

    def getHeight(self):
        return self.xTiles;

    def getWidth(self):
        return self.xTiles;

    def getEntrance(self):
        return self.entrance

    def getRoomsPerX(self) :
        return self.roomsPerSide

    def getRoomsPerY(self):
        return self.roomsPerSide

    def isBlocked(self, x, y):
        if self.getTile(x, y) == WALL:
            return True
        else:
            return False

    def generateRooms(self):

        #print("------> Creating Level")

        for y in range(self.roomsPerSide):
            for x in range(self.roomsPerSide):

                xLevel = x * self.roomSize
                yLevel = y * self.roomSize

                print("room-grid @ %s, %s" % (x, y))
                print("level-grid @ %s, %s " % (xLevel, yLevel))

                room = Room(self, x, y)
                room.create()
                self.drawOnGrid(xLevel, yLevel, room)
                self.roomgrid[x][y] = room

        #print("<------ Finished Level Creation")

    def generateObject(self, quadrant):

        x_split = self.getWidth() / 2
        y_split = self.getHeight() / 2
        # 1  2
        # 3  4
        if quadrant == 1:
            x_start = 0
            y_start = 0
        if quadrant == 2:
            x_start = x_split
            y_start = 0
        if quadrant == 3:
            x_start = 0
            y_start = y_split
        if quadrant == 4:
            x_start = x_split
            y_start = y_split

        while True:
            x = random.randint(x_start, x_start + x_split)
            y = random.randint(y_start, y_start + y_split)
            if not self.isBlocked(x, y):
                location = Coord(x, y)
                return location

    def drawOnGrid(self, xOffset, yOffset, room):

        for y in range(self.roomSize):
            for x in range(self.roomSize):
                tileValue = room.getTile(x, y);
                #print("%s @ %s, %s -- %s, %s" % (tileValue, x, y, x+xOffset, y+yOffset))
                self.tilegrid[x + xOffset][y + yOffset] = tileValue

    def setTile(self, newValue, x, y):
        self.tilegrid[x][y] = newValue;

    def getTile(self, x, y):

        #print("Tile @: %s, %s" % (x, y))

        if (0 > x or x > self.xTiles or 0 > y or y > self.yTiles):
            return 0
        else:
            return self.tilegrid[x][y]

    def clearTiles(self):
        self.tilegrid = [[None] * self.yTiles] * self.xTiles

    def checkTile(self, x, y):
        if (self.tilegrid[x][y] == OPEN):
            return True
        else:
            return False

    def textDraw(self):

        for x in range(self.xTiles):
            values = []
            for y in range(self.yTiles):
                values.append(self.tilegrid[x][y])
            print(values)

    def getRoom(self, x, y):
        if (x < 0 or y < 0):
            return Room(self, 0, 0)
        elif (x > self.roomsPerSide or y > self.roomsPerSide):
            return None
        else:
            return self.roomgrid[x][y]

class Room():

    def __init__(self, map, xPos, yPos):
        self.xPos = xPos;
        self.yPos = yPos;
        self.roomSize = 9
        self.squareSize = 3
        self.roomsPerSide = 9 * map.level;
        self.map = map
        self.squaresPerSide = 3;

        self.tiles = [[None for x in range(self.roomSize)] for y in range(self.roomSize)]
        for x in range(self.roomSize):
            for y in range(self.roomSize):
                self.tiles[x][y] = UNLOCKED

    def getTile(self, x, y):
        return self.tiles[x][y];

    def create(self):

        #print("Creating Room @ %s, %s" % (self.xPos, self.yPos))

        leftNeighbor = self.map.getRoom(self.xPos - 1, self.yPos)
        topNeighbor = self.map.getRoom(self.xPos, self.yPos - 1)
        leftConnection = leftNeighbor.isConnected(2, 1)
        topConnection = topNeighbor.isConnected(1, 2)

        rightConnection = False
        bottomConnection = False

        case = random.randint(0, 2)

        if case == 0:
            rightConnection = True
        if case == 1:
            bottomConnection = True
        if case == 2:
            rightConnection = True
            bottomConnection = True

        bottomEdge = False;
        if (self.yPos == (self.roomsPerSide - 1)):
            bottomEdge = True;
            if not (leftConnection and topConnection):
                rightConnection = True

        rightEdge = False;
        if self.xPos == (self.roomsPerSide - 1):
            rightEdge = True
            if not (leftConnection and topConnection):
                bottomConnection = True

        #print("LeftConnect: %s" % leftConnection)
        #print("RightConnect: %s" % rightConnection)
        #print("TopConnect: %s" % topConnection)
        #print("BottomConnect: %s" % bottomConnection)

        for y in range(self.squaresPerSide):
            for x in range(self.squaresPerSide):

                if (x == 0) :
                    if (self.xPos == 0) :
                        #left edge?
                        self.wall(x, y)
                    elif (leftNeighbor.isConnected(2, y)):
                        # left connected?
                        self.open(x, y)
                        leftConnection = True;
                    else:
                        self.wall(x, y)
                elif (y == 0):
                    if (self.yPos == 0):
                        # top edge?
                        self.wall(x, y)
                    elif (topNeighbor.isConnected(x, 2)):
                        # top connected?
                        self.open(x, y)
                        topConnection = True;
                    else:
                        self.wall(x, y)
                elif (x == 2 and rightEdge):
                    # right edge?
                    self.wall(x, y)
                elif (y == 2 and bottomEdge):
                    # bottom edge?
                    self.wall(x, y)
                elif (x == 1 and y == 1):
                    # middle?
                    self.open(x, y)
                elif (x == 2 and y == 1):
                    # right connection
                    if (rightConnection):
                        self.open(x, y)
                    else:
                        self.wall(x, y)
                elif (x == 1 and y == 2):
                    # bottom connection
                    if (bottomConnection):
                        self.open(x, y)
                    else:
                        self.wall(x, y)

                else:

                    # if there is a connection neighboring the corner, choose to open
                    if (((x == 0 and y == 0) and (leftConnection or topConnection))
                            or ((x == 2 and y == 0) and (rightConnection or topConnection))
                            or ((x == 0 and y == 2) and (leftConnection or bottomConnection))
                            or ((x == 2 and y == 2) and (rightConnection or bottomConnection))):
                        if (random.randint(0, 1) == 1):
                            self.open(x, y)
                        else:
                            self.wall(x, y)

                    else:
                        #no neighbor connection
                        self.wall(x, y);

    def isConnected(self, x, y):

        if (x < 0 or y < 0):
            return False;

        if (x >= (self.roomSize) or y >= (self.roomSize)):
            return False;

        x = x * self.squareSize
        y = y * self.squareSize

        #print("TILE @ (%s, %s) : %s" % (x, y, self.tiles[x][y]))

        return self.tiles[x][y] == OPEN;

    def open(self, x, y):
        #print("Open @ %s, %s" % (x, y))
        self.fillSquare(OPEN, x, y);

    def wall(self, x, y):
        #print("Wall @ %s, %s" % (x, y))
        self.fillSquare(WALL, x, y)

    def fillSquare(self, value, x, y):
        xStart = x * self.squareSize
        yStart = y * self.squareSize

        #print("X: %s --> %s" % (xStart, xEnd))
        #print("Y: %s --> %s" % (yStart, yEnd))

        for j in range(3):
            for i in range(3):
                x = xStart + i
                y = yStart + j
                #print("Writing %s @ %s, %s" % (value, x, y))
                if (self.tiles[x][y] == UNLOCKED):
                    self.tiles[x][y] = value

    def debug(self):
        for x in range(self.roomSize):
            values = []
            for y in range(self.roomSize):
                values.append(self.tiles[x][y])
            print(values)

