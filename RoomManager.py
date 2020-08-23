import pygame

from EventHandlers import RoomManagerEventHandlers
from Grid import Grid
from Room import Room

class RoomManager(object):
    """Stores rooms, used to change room and draw current room"""

    def __init__(self,screenRes, rooms=None):
        self.roomResolution = screenRes
        if rooms == None:
            self.rooms = self.__gameSetup__() #Sets up game
        self.currentRoomIndex = 0
        self.currentRoom = self.rooms[self.currentRoomIndex]
        self.totalMoves = 0 #Holds the total moves made by all the rooms so far in the program #reference to game manager
        self.eventHandlers = RoomManagerEventHandlers(self)

    #Getters
    def getRoomNumber(self):#returns a value as a string indication what room is currently ruinning
        return str(self.currentRoomIndex + 1)

    def getMoves(self):
        moves = self.currentRoom.getMoves()
        return moves

    def getTotalMoves(self):
        return self.totalMoves

    def getCurrentRoom(self):
        return self.currentRoom

    def getLevel(self):
        return self.currentRoom.getLevel()

    def getEventHandlers(self):
        return self.eventHandlers

    def __getResolution(self):
        return self.roomResolution

    #Setters
    def setCurrentRoom(self, index):
        self.currentRoomIndex = index
        self.currentRoom = self.rooms[self.currentRoomIndex]

    def setMoves(self, value):
        self.currentRoom.setMoves(value)

    def __setResolution__(self, value):
        self.roomResolution = value

    def __setTotalMoves__(self, value):
        self.totalMoves = value

    def __setCurrentRoomIndex__(self, value):
        self.currentRoomIndex = value

    def __setEventHandlers__(self, value):
        self.eventHandlers = value

    #Special
    def draw(self, surface): #Draws current room
        self.currentRoom.draw(surface)

    #Increments total moves
    def incrementTotalMoves(self,value):
        self.totalMoves += value

    #Used to advance to the next room
    def nextRoom(self):
         self.currentRoomIndex += 1
         if self.currentRoomIndex == len(self.rooms):
             return False
         else:
             self.currentRoom = self.rooms[self.currentRoomIndex]
             return True

    def __convertScreenResolution__(self, screenRes): #Converts the full size res into the room res, which is the same but only 80% of the height of the screen
        return (screenRes[0], int(screenRes[1] * 0.80))

    def __gameSetup__(self): #Sets up all the rooms for the game
        #(6,[(0,3),(2,6),(3,3),(3,4),(3,5),(4,3)])

        rooms = [Room(1, Grid.map1,self.roomResolution), Room(2, Grid.map2, self.roomResolution), Room(3, Grid.map3, self.roomResolution), Room(4, Grid.map4, self.roomResolution), Room(5, Grid.map5, self.roomResolution)]
        return rooms












