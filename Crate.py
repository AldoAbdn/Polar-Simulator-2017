import pygame, sys
from SpriteBase import MovableSprite


class Crate(MovableSprite):
    """Crate that player will 'push' """
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        MovableSprite.__init__(self, coordinates,tileSize,"Assets/Crate.png")
        self.active = False#Tracks if a crate is one a diamond or not. Crate is active if on a square
        self.surfaceNotActive = pygame.image.load("Assets/Crate.png")
        self.surfaceActive = pygame.image.load("Assets/CrateActive.png")
        self.surfaceActive = pygame.transform.scale(self.surfaceActive, (self.rect.width, self.rect.height))
        self.scale(tileSize)

    #Override
    def scale(self, tileSize):
        #If i don't do this, on restart images go back to original size
        self.surfaceActive = pygame.transform.scale(self.surfaceActive,(int(tileSize[0]), int(tileSize[1])))
        self.surfaceNotActive = pygame.transform.scale(self.surfaceNotActive, (int(tileSize[0]), int(tileSize[1])))
        if self.active:
            self.surface = self.surfaceActive
        else:
            self.surface = self.surfaceNotActive
        self.rect = self.surface.get_rect()

    def getActive(self):
        return self.active

    def toggleActive(self, active=None):
        if active == None:
            self.active = not self.active 
        else:
            self.active = active
        if self.active:
            self.surface = self.surfaceActive
        else:
            self.surface = self.surfaceNotActive

##TESTING
#def test():
#    print "crate test"
#    display = pygame.display.set_mode((640,460))
#    sprite = Crate()
#    sprite.setPosition((40,40))
#    print sprite.rect.width, sprite.rect.height, sprite.rect.center
#    while True:
#        display.blit(sprite.getSurface(), sprite.getRect())
#        events = pygame.event.get()
#        for event in events:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#        pygame.display.update()
#test()


