import pygame
class SurfaceManager(object):
    """If an object contains multiple surface, this puts them together and has a draw function for drawing the resultant
    surface onto another surface"""

    def __init__(self, display, res, bgImage=None):
        self.surface = display
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.objects = []
        if bgImage != None:
            self.backgroundImage = pygame.image.load(bgImage).convert()
            self.backgroundImage = pygame.transform.scale(self.backgroundImage, (self.rect.width, self.rect.height)).convert() #Scales image to screen res
        else:
            self.backgroundImage = pygame.surface.Surface(res)

    #Getters and setters
    def setObjects(self, value):
        self.objects = value

    def getSurfaceResolution(self):
        return self.surfaceResolution

    #Special
    def draw(self):
        #Fill Background
        self.surface.blit(self.backgroundImage, self.rect)
        for object in self.objects:
            object.draw(self.surface)

        self.clock.tick(60)
       # print self.clock.get_fps()
        pygame.display.update()
