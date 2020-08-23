import pygame, sys
from Scene import Scene
from Grid import Grid
from Player import Player
from GridSquare import GridSquare
from GridSquare import GridSquareStar
from Wall import Wall
from Crate import Crate
from SpriteManager import SpriteManager

class Room(object):
    """Main game scene that will be drawn onto another scene that will contain UI elements"""

    def __init__(self, imagePath="", width=640, height=480):
        #Sets image, if no image generates a blank surface
        try:
            self.surface = pygame.image.load(imagePath)
        except:
            self.surface = pygame.Surface([width, height])
        #Sets up rect 
        self.rect = self.surface.get_rect()
        self.moves = 0
        self.grid = Grid()
        self.player = Player()
        #Squares
        self.tileManager = SpriteManager()
        #Star Squares
        self.diamondManager = SpriteManager()
        #Walls
        self.wallManager = SpriteManager()
        #Crates
        self.crateManager = SpriteManager()

        self.startLevel(0)

        self.surface.fill(Scene._Colours["red"])

    #Getters
    def getLevel(self):
        return self.level

    def getTotalMoves(self):
        return self.totalMoves

    def getMoves(self):
        return self.moves

    #Setters
    def setLevel(self, value):
        self.level = value

    def setTotalMoves(self, value):
        self.totalMoves = value

    def setMoves(self, value):
        self.moves = value

    #Moves
    def incrementMoves(self):
        self.totalMoves += 1
        self.moves += 1

    #Draw
    def draw(self, surface):
        self.tile

    #Setup
    def setup(self):
        self.grid.reset()
        self.player.setCoordinates((2,4))
        self.grid.addItem(self.player.getCoordinates(), self.player)

        self.tileManager.setup(GridSquare.generate(16), [(0,2),(0,3),(0,4),
                                                                         (1,2),(1,5),
                                                                         (2,2),(2,3),(2,4),(2,5),(2,6),
                                                                         (3,2),(3,4),(3,5),(3,6),
                                                                         (4,3),(4,4)]) 
        self.diamondManager.setup(GridSquareStar.generate(2),[(0,5),
                                                                              (4,2)])
        self.wallManager.setup(Wall.generate(3),[(1,3),(1,4),
                                                               (3,3)])
        self.crateManager.setup(Crate.generate(2),[(1,2),
                                                           (3,5)])

        self.grid.addItemsBySpriteManager(self.tileManager)
        self.grid.addItemsBySpriteManager(self.diamondManager)
        self.grid.addItemsBySpriteManager(self.wallManager)
        self.grid.addItemsBySpriteManager(self.crateManager)


    #Event Handlers
    def eventManager(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.keyPress(event)

    def keyPress(self, event):
        if event.key == 119: #W key
            self.playerMove("up")
        if event.key == 115: #S key
            self.playerMove("down")
        if event.key == 97: #A key
            self.playerMove("left")
        if event.key == 100: #D key
            self.playerMove("right")

    def quit(self):
        pygame.quit()
        sys.exit()

    #Special
    def fillSpaceWithWalls(self):
        currentGridItems = self.grid.getGridItems()
        rows = len(currentGridItems)
        collums = len(currentGridItems[0])
        for i in range(0,rows):
            for j in range(0,collums):
                if not currentGridItems[i][j]:
                    wall = Wall()
                    self.wallManager.add(wall, (i,j))

    #Used to predict where a sprite will be if it were to move a certain direction
    def predictCoordinates(self,currentCoordinates, direction):
        if direction.lower() == "up":
            possibleCoordinates = (currentCoordinates[0] - 1, currentCoordinates[1])
        elif direction.lower() == "down":
            possibleCoordinates = (currentCoordinates[0] + 1, currentCoordinates[1])
        elif direction.lower() == "left":
            possibleCoordinates = (currentCoordinates[0], currentCoordinates[1] - 1)
        elif direction.lower() == "right":
            possibleCoordinates = (currentCoordinates[0], currentCoordinates[1] + 1)

        return possibleCoordinates

    #Checks if player can move and handles events
    def playerMove(self, direction):
        currentCoordinates = self.player.getCoordinates() #Gets current coordinates
        possibleCoordinates = self.predictCoordinates(currentCoordinates,direction)
        isLevelOver = False
                        
        try: #Catches out of range exeption if player tries to move out of grid and there is no wall
            items = self.grid.getItems(possibleCoordinates[0], possibleCoordinates[1])
            print items
            if items and possibleCoordinates[0] >= 0 and possibleCoordinates[1] >= 0:
                for i in range(0, len(items)):
                    if items[i].__class__.__name__ == "Wall":
                        return #Returns if player hits a wall
                    elif items[i].__class__.__name__ == "Crate":
                        crateMoved = self.crateMove(items[i], direction)
                        isLevelOver = self.cratesCheck()
                        if not crateMoved:
                            return #returns if crate can't move
                        elif isLevelOver:
                            self.levelOver()
                    elif items[i].__class__.__name__ == "GridSquare":
                        pass
                #Player will only move if none of the above are met
                if not isLevelOver:
                    self.incrementMoves()
                    self.player.move(self.grid.getPosition(possibleCoordinates),possibleCoordinates)
                    self.grid.addItem(self.player.getCoordinates(), self.player)
                    return

        except:
            print "Exception"

    #Checks if crate can move and then returns true if player can push crate
    def crateMove(self, crate,direction):
        currentCoordinates = crate.getCoordinates()
        possibleCoordinates = self.predictCoordinates(currentCoordinates,direction)
                
        try: #Catches out of range exeption if player tries to move out of grid and there is no wall
            items = self.grid.getItems(possibleCoordinates[0], possibleCoordinates[1])
            if items and possibleCoordinates[0] >= 0 and possibleCoordinates[1] >= 0:
                for i in range(0, len(items)):
                    if items[i].__class__.__name__ == "Wall":
                        return False
                    elif items[i].__class__.__name__ == "Crate":
                        return False
                    else:
                        crate.move(self.grid.getPosition(possibleCoordinates),possibleCoordinates)
                        self.grid.addItem(crate.getCoordinates(), crate)
                        for i in range(0, len(items)):
                            if isinstance(items[i], GridSquareStar):
                                print "Grid star"
                                crate.image.fill((0,255,0))
                                return True
                            else:
                                crate.image.fill((128,0,0))
                                return True
                        return True #return true if it moved
            return False

        except:
            print "Exception"

    #Checks if all crates are on star squares
    def isGameOver(self):
        crates = self.crateManager.getSprites()
        items = self.grid.getGridItems()
        counter = 0
       # print items
        for i in range(0,len(crates)):
            crateCoord = crates[i].getCoordinates()
            tempRow = items[crateCoord[0]]
            tempCol = tempRow[crateCoord[1]]
            for j in tempCol:
                if isinstance(j, GridSquareStar):
                    counter += 1
        if counter == len(crates):
            return True
        else:
            return False

