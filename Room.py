import pygame
from pygame.locals import *
from EventManager import EventManager
from EventHandlers import RoomEventHandlers
from SoundManager import SoundManager
from Crate import Crate
from Wall import Wall
from WarehouseKeeper import WarehouseKeeper
from Tile import Diamond
from Tile import Tile
from Grid import Grid

class Room(object):
    """These are the 'levels' of the game. There will be 5 in total"""

    def __init__(self,level,map,roomRes,imagePath=""):
        self.roomResolution = roomRes
        self.level = level
        self.moves = 0
        self.grid = Grid(map, roomRes)
        self.player = self.grid.getPlayer()
        self.eventHandlers = RoomEventHandlers(self)

    #Getters
    def getMoves(self):
        return self.moves

    def getLevel(self):
        return self.level

    def getEventHandlers(self):
        return self.eventHandlers

    def getGrid(self):
        return self.grid

    def __getResolution__(self):
        return self.roomResolution

    def __getPlayer__(self):
        return self.player

    #Setters
    def setMoves(self, value):
        self.moves = value

    def __setLevel__(self, value):
        self.level = value

    def __setEventHandlers__(self, value):
        self.eventHandlers = value

    def __setResolution__(self,value):
        self.roomResolution = value

    def __setGrid(self, value):
        self.grid = value

    def __setPlayer__(self, value):
        self.player = value

    #Draw
    def draw(self, surface):
         self.grid.draw(surface) #Draws all the sprites

    def clickPlayerMove(self, pos):
        possiblePlayerCoords = self.grid.predictPlayerPossibleCoords()
        clickedItem = self.grid.getItemByPos(pos)
        if clickedItem:
            clickedItemCoords = clickedItem.getCoordinates()
            for coords in possiblePlayerCoords:
                if clickedItemCoords == coords:
                    direction = self.grid.convertCoordsToDirection(coords)
                    if direction:
                        self.playerMove(direction)
                    return

    #This is what is called when a WASD is pressed, checks if player, or player and crate can move
    def playerMove(self, direction):
        playerMove = self.__spriteMoved__(direction)
        if playerMove:
            self.__incrementMoves__()
            pygame.event.post(EventManager.Events["Player Move"]) #If the player moves, call player move event to update count
            roomOver = self.__isRoomOver__()
            if roomOver:
                pygame.event.post(EventManager.Events["Room Over"])

    #Used to predict where a sprite will be if it were to move a certain direction
    def __predictCoordinates__(self,currentCoordinates, direction):
        if direction.lower() == "up":
            possibleCoordinates = (currentCoordinates[0] - 1, currentCoordinates[1])
        elif direction.lower() == "down":
            possibleCoordinates = (currentCoordinates[0] + 1, currentCoordinates[1])
        elif direction.lower() == "left":
            possibleCoordinates = (currentCoordinates[0], currentCoordinates[1] - 1)
        elif direction.lower() == "right":
            possibleCoordinates = (currentCoordinates[0], currentCoordinates[1] + 1)

        return possibleCoordinates

    #Takes in a sprite, checks if hits a wall. Moves sprite depending on type
    def __spriteMoved__(self, direction):
        if not self.player.getMoving() and not self.grid.crateMoving():
            #Predicts next possible position based on direction
            currentCoordinates = self.player.getCoordinates() #Gets current coordinates
            possibleCoordinates = self.__predictCoordinates__(currentCoordinates,direction)
            roomOver= False
            canMove = None
           # try: #Catches out of range exeption if player tries to move out of grid and there is no wall
            if possibleCoordinates[0] >= 0 and possibleCoordinates[0] < self.grid.rows and possibleCoordinates[1] >= 0 and possibleCoordinates[1] < self.grid.cols:
                items = self.grid.getItems(possibleCoordinates[0], possibleCoordinates[1])
                if any(isinstance(x, Wall) for x in items):
                    return False
                elif any(isinstance(x, Crate) for x in items):
                    crate = None
                    for possibleCrate in items:
                        if isinstance(possibleCrate, Crate):
                            crate = possibleCrate
                            break
                    crateCurrentCoordinates = crate.getCoordinates()
                    cratePossibleCoordinates = self.__predictCoordinates__(crateCurrentCoordinates, direction)
                    if cratePossibleCoordinates[0] >= 0 and cratePossibleCoordinates[0] < self.grid.rows and cratePossibleCoordinates[1] >= 0 and cratePossibleCoordinates[1] < self.grid.cols:
                        items = self.grid.getItems(cratePossibleCoordinates[0], cratePossibleCoordinates[1])
                        if any(isinstance(x, Wall) for x in items) or any(isinstance(x, Crate) for x in items):
                            return False
                        elif any(isinstance(x, Diamond) for x in items):
                            crate.toggleActive(True)
                        else:
                            crate.toggleActive(False)
                        self.player.setCoordinates(possibleCoordinates)
                        crate.setCoordinates(cratePossibleCoordinates)
                        return True

                else:
                    self.player.setCoordinates(possibleCoordinates)
                    return True
            else:
                return False

    def __incrementMoves__(self): #Increments moves for the room
        self.moves += 1

    def __isRoomOver__(self): #Checks for room over, compares crate positions to diamond positions
        crates = self.grid.getCrates()
        diamonds = self.grid.getDiamonds()
        counter = 0
        #Compares the coordinates of each crate to each diamond in a room, adds to a counter if they are in the same position
        for i in range(0, len(crates)):
            for j in range(0, len(diamonds)):
                if crates[i].getCoordinates() == diamonds[j].getCoordinates():
                    counter += 1
        #If all crates are on diamonds, room over return true
        if counter == len(crates):
            return True
        else:
            return False







