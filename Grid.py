from WarehouseKeeper import WarehouseKeeper
from Crate import Crate
from Tile import Tile
from Tile import Diamond
from Wall import Wall
from SpriteBase import MovableSprite
import pygame

class Grid(object):
    """Will hold grid positions for drawn grid, and hold what objects are in each grid square"""
    map1 = [["x","x","x","x","x","x","x","x"],
            ["x","x","x","D","x","x","x","x"],
            ["x","x","x","C","C","D","x","x"],
            ["x","D","T","C","P","x","x","x"],
            ["x","x","x","x","C","x","x","x"],
            ["x","x","x","x","D","x","x","x"],
            ["x","x","x","x","x","x","x","x"]]

    map2 = [["x","x","x","x","x","x","x"],
            ["x","T","T","T","D","x","x"],
            ["x","C","x","x","T","x","x"],
            ["x","T","T","P","T","T","x"],
            ["x","T","x","T","C","T","x"],
            ["x","D","T","T","x","x","x"],
            ["x","x","x","x","x","x","x"]]

    map3 = [["x","x","x","x","x","x","x","x"],
            ["x","T","T","x","D","D","D","x"],
            ["x","T","C","C","C","T","T","x"],
            ["x","T","T","P","T","T","T","x"],
            ["x","T","T","x","x","x","x","x"],
            ["x","T","T","x","x","x","x","x"],
            ["x","x","x","x","x","x","x","x"]]

    map4 = [["x","x","x","x","x","x","x","x","x","x","x"],
            ["x","x","x","x","x","x","x","D","T","T","x"],
            ["x","x","x","x","x","x","x","D","x","T","x"],
            ["x","x","x","x","x","x","x","D","x","T","x"],
            ["x","T","T","P","C","T","C","T","C","T","x"],
            ["x","T","x","T","x","T","x","T","x","x","x"],
            ["x","T","T","T","T","T","T","T","x","x","x"],
            ["x","x","x","x","x","x","x","x","x","x","x"]]

    map5 = [["x","x","x","x","x","x","x","x","x"],
            ["x","x","x","T","T","x","x","x","x"],
            ["x","T","T","T","T","T","C","P","x"],
            ["x","T","x","T","C","x","C","T","x"],
            ["x","T","D","D","D","x","T","T","x"],
            ["x","x","x","x","x","x","x","x","x"]]

    def __init__(self, map, screenres=(640,400)):
        #self.surface =
        self.SCREENRATIO = screenres[0]/screenres[1]
        self.rows = len(map)
        self.cols = len(map[0])
        self.surfaceResolution = screenres
        tileSizeX = screenres[0] / self.cols
        tileSizeY = screenres[1] / self.rows
        self.tileSize = (int(tileSizeX), int(tileSizeY))
        self.speed = (0.020833333333 * self.surfaceResolution[0], 0.020833333333 * self.surfaceResolution[1])
        self.gridPositions = []
        for i in range(0,self.rows):
            self.gridPositions.append([])
            for j in range(0,self.cols):
                self.gridPositions[i].append(j)
        self.populateGridPositions() #Populates positions list with coordinates

        if map != None:
            self.gridItems = self.generateGridFromMap(map)
        else:
            self.gridItems = None

    #Getters
    def getPosition(self, coor):
        return self.gridPositions[coor[0]][coor[1]]

    def getItems(self, row, col):
        return self.gridItems[row][col]

    def getPlayer(self): #Returns the one player that should be in the grid
        items = self.gridItems
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, WarehouseKeeper):
                            return k
        return False

    def getCrates(self): #Returns the list of crates.
        items = self.gridItems
        crates = []
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, Crate):
                            crates.append(k)
        return crates

    def getDiamonds(self): #Returns the list of diamonds.
        items = self.gridItems
        diamonds = []
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, Diamond):
                            diamonds.append(k)
        return diamonds

    def __getGridPositions__(self):
        return self.gridPostions

    def __getGridItems__(self):
        return self.gridItems

    def __getMovableSprites__(self): #Gets all the movable type sprites, used for drawing later
        items = self.gridItems
        movableSprites = []
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                for k in items[j][i]:
                    if isinstance(k, MovableSprite):
                        movableSprites.append(k)
        return movableSprites

    #Setters
    def __setGridPositions__(self,Value):
        self.gridPositions = Value

    def __setGridItems__(self, value):
        self.gridItems = value

    def __setPos__(self, row, col, value):
        self.gridPostions[row][col] = value

    def __setItems__(self, row, col, value):
        self.gridItems[row][col] = value

    #String
    def toString(self):
        return isinstance.__class__.__name__ + ": Grid " + str(self.Grid)

    #Special
    def draw(self, surface): #Loops through item multi-dim array and calls draw function on each
        movingSprites = [] #Holds moving sprites so they can be animated
        items = self.gridItems
        player = self.getPlayer()
        #Add player to movablesprite list
        if not player.comparePos(self.getPosition(player.getCoordinates())) or (player.getMoving() and player not in movingSprites):
            movingSprites.insert(0, player)
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                for sprite in items[j][i]:
                    if isinstance(sprite, Crate): #Adds crates to movableSprite list
                        if not sprite.comparePos(self.getPosition(sprite.getCoordinates())) or (sprite.getMoving() and sprite not in movingSprites):
                            movingSprites.append(sprite)
                        else:
                            sprite.draw(surface)
                    elif isinstance(sprite, Wall):
                        pass
                    else:
                        sprite.draw(surface)
        if movingSprites != []:
            self.move(movingSprites) #Animates moving sprites
        self.drawMovable(surface) #Draws movable objects

    def drawMovable(self, surface): #Draws movable sprites
        movableSprites = self.__getMovableSprites__()
        for sprite in movableSprites:
            sprite.draw(surface)

    def move(self, sprites): #Takes in movable sprites, moves them if they need to be
        for sprite in sprites:
            currentCoords = sprite.getCoordinates()
            targetPos = self.gridPositions[currentCoords[0]][currentCoords[1]]
            finishedMoving = sprite.move(targetPos)
            if finishedMoving:
                sprites.remove(sprite)
                self.addItem(sprite)

    def getItemByPos(self, pos):
        gridItems = self.gridItems
        for row in gridItems:
            for col in row:
                for sprite in col:
                    if sprite.getRect().collidepoint(pos):
                        return sprite
        return False

    def convertCoordsToDirection(self, coords):
        playerCoords = self.getPlayer().getCoordinates()
        if coords[0] == playerCoords[0] - 1:
            return "UP"
        elif coords[0] == playerCoords[0] + 1:
            return "DOWN"
        elif coords[1] == playerCoords[1] - 1:
            return "LEFT"
        elif coords[1] == playerCoords[1] + 1:
            return "RIGHT"
        else:
            return False

    def predictPlayerPossibleCoords(self):
        player = self.getPlayer()
        currentCoords = player.getCoordinates()
        coords = [(currentCoords[0]+1,currentCoords[1]), (currentCoords[0]-1,currentCoords[1]), (currentCoords[0], currentCoords[1]+1), (currentCoords[0], currentCoords[1]-1)]
        return coords

    def populateGridPositions(self): #Generates rect center positions based tileSize that was generated from the resolution
        xGap = (self.surfaceResolution[0] - (self.tileSize[0] * self.cols) ) / 2
        yGap = (self.surfaceResolution[1] - (self.tileSize[1] * self.rows) ) / 2
        startX = int(self.tileSize[0] / 2 + xGap) #Starting Center value for first square
        startY = int(self.tileSize[1] / 2 + yGap) #Starting Center value for first Square
        X = startX
        Y = startY
        for j in range(0, self.rows): #Loops through each row
            X = startX
            if j != 0:
                Y+=int(self.tileSize[1]) #Gap between each center
            for i in range(0, self.cols): #Goes through each position in self.rows

                if i != 0:
                    X+=int(self.tileSize[0]) #Gap between each center
                self.gridPositions[j][i] = (X,Y)

    def generateGridFromMap(self, map): #Takes in a a map, gets num rows and columns and then creates a list from the map with all the objects
        self.rows = len(map)
        self.cols = len(map[0])
        levelMap = map
        gridItems = []
        for i in range(0, self.rows):
            gridItems.append([])
            for j in range(0, self.cols):
                gridItems[i].append([])
                sprites = self.convertCharToObject(levelMap[i][j], (i,j))
                gridItems[i][j] = sprites
        self.setInitialPosition(gridItems)
        return gridItems

    def convertCharToObject(self, char, pos): #Used to generate a grid from a map, takes in characters and returns an object associated with that character
        if char == "x":
            return [Wall(pos, self.tileSize)]
        elif char == "D":
            return [Diamond(pos, self.tileSize)]
        elif char == "T":
            return [Tile(pos, self.tileSize)]
        elif char == "C":
            return [Tile(pos, self.tileSize), Crate(pos, self.tileSize)]
        elif char == "P":
            return [Tile(pos, self.tileSize),WarehouseKeeper(pos, self.tileSize)]

    def setInitialPosition(self, spriteList): #Sets initial positions for new sprites added from a map
        gridItems = spriteList
        for row in gridItems:
            for col in row:
                for sprite in col:
                    coords = sprite.getOriginalCoordinates()
                    sprite.reset(self.getPosition(coords))

    def addItem(self, item): #Adds a single item
        self.removeItem(item) #Removes item first before adding to a grid square
        coords = item.getCoordinates()
        self.gridItems[coords[0]][coords[1]].append(item)
        item.setPosition(self.gridPositions[coords[0]][coords[1]])

    def removeItem(self, item): #Removes a single item, usually used when re-adding another item so there aren't two copies in the grid
        items = self.gridItems
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                if item in items[j][i]:
                    self.gridItems[j][i].remove(item) #Removes item from 'grid'

    def crateMoving(self): #Checks if any of the crates are moving
        crates = self.getCrates()
        for crate in crates:
            if crate.getMoving():
                return True
        else:
            return False

    def reset(self): #Resets a grid back to its original state
        crates = self.getCrates()
        player = self.getPlayer()
        if crates != []:
            for crate in crates:
                self.removeItem(crate)
                coords = crate.getOriginalCoordinates()
                crate.reset(self.gridPositions[coords[0]][coords[1]])
                crate.toggleActive(False)
                self.addItem(crate)
        if player != None:
            self.removeItem(player)
            playerCoords = player.getOriginalCoordinates()
            player.reset(self.gridPositions[playerCoords[0]][playerCoords[1]])
            self.addItem(player)

    def restart(self):
        self.reset()




