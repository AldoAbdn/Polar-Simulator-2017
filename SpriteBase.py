import pygame, sys
import threading
pygame.init()

class SpriteBase(object):
    """Base sprite class that all visible sprite objects will inherit from(squares, player)"""
    def __init__(self, coordinates=(0,0),tileSize=(80,80),imagePath=None):
        if imagePath != None:
            #Sets image, if no image generates a blank surface
            self.surface = pygame.image.load(imagePath).convert_alpha()
            self.surface = pygame.transform.scale(self.surface, tileSize).convert_alpha()
            #Sets up rect
            self.rect = self.surface.get_rect()
        else:
            self.rect = pygame.rect.Rect((0,0),(tileSize))
        #Holds current grid coordinates
        self.coordinates = coordinates #(x,y)
        self.originalCoordinates = coordinates

    #Getters
    def getCoordinates(self):
        return self.coordinates

    def getPosition(self):
        return self.rect.center

    def getOriginalCoordinates(self):
        return self.originalCoordinates

    def __getSurface__(self):
        return self.surface

    def getRect(self):
        return self.rect

    #Setters
    def setOriginalCoordinates(self, value):
        self.originalCoordinates = value

    def setPosition(self, pos):
        self.rect.center = pos

    def setCoordinates(self, value):
        self.coordinates = value

    def __setSurface__(self, value):
        self.Surface = value

    def __setRect__(self, value):
        self.rect = value

    #Special
    def draw(self, surface):
        surface.blit(self.surface,self.rect)

    def scale(self, tileSize): #Scales surface to resolution
        self.surface = pygame.transform.scale(self.surface,(int(tileSize[0]), int(tileSize[1])))
        self.rect = self.surface.get_rect()

    def reset(self, pos):
        self.setCoordinates(self.originalCoordinates)
        self.setPosition(pos)


#Used for player and crate, extra functions for positioning
class MovableSprite(SpriteBase):
    def __init__(self, coordinates = (0,0), tileSize = (80,80), imagePath = None):
        SpriteBase.__init__(self, coordinates, tileSize, imagePath)
        self.moving = False

    def getMoving(self):
       return self.moving

    def setMoving(self, value):
        self.moving = value

    def move(self, newPosition, speed=(10,10)):
        currentCoords = self.getCoordinates()
        currentPosition = self.getPosition()
        position = newPosition
        if position != currentPosition:
            self.setMoving(True)
            if position[0] > currentPosition[0]:
                newPos = (currentPosition[0] + speed[0], currentPosition[1])
                if newPos[0] >= position[0]:
                    self.setPosition(position)
                else:
                    self.setPosition(newPos)
            elif position[0] < currentPosition[0]:
                newPos = (currentPosition[0] - speed[0], currentPosition[1])
                if newPos[0] <= position[0]:
                    self.setPosition(position)
                else:
                    self.setPosition(newPos)
            elif position[1] > currentPosition[1]:
                newPos = (currentPosition[0], currentPosition[1] + speed[1])
                if newPos[1] >= position[1]:
                    self.setPosition(position)
                else:
                    self.setPosition(newPos)
            elif position[1] < currentPosition[1]:
                newPos = (currentPosition[0], currentPosition[1] - speed[1])
                if newPos[1] <= position[1]:
                    self.setPosition(position)
                else:
                    self.setPosition(newPos)
            return False #Not done moving
        else:
            self.setMoving(False)
            return True #Finished moving

    def comparePos(self, newPos): #compares a position with the sprites current position, returns true if they match
        if self.getPosition() == newPos:
            return True
        else:
            return False

#TESTING
#def test1():
#    DISPLAY = pygame.display.set_mode((640,460))
#    sprite = SpriteBase("Assets/Player.png")
#    sprite.setPosition((40,40))
#    print sprite.rect.width, sprite.rect.height, sprite.rect.center
#    while True:
#        DISPLAY.blit(sprite.getSurface(), sprite.getRect())
#        #
#        events = pygame.event.get()
#        for event in events:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#        pygame.display.update()
#test1()

#def test2():
#    DISPLAY = pygame.display.set_mode((640,460))
#    sprite = SpriteBase("Assets/Player.png")
#    sprite.setPosition((40,40))
#    print sprite.rect.width, sprite.rect.height, sprite.rect.center
#    while True:
#        DISPLAY.fill((0,0,0))
#        DISPLAY.blit(sprite.getSurface(), sprite.getRect())
#        events = pygame.event.get()
#        for event in events:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#            elif event.type == pygame.KEYDOWN:
#                sprite.move((120,40),(0,0))
#        pygame.display.update()
#test2()
