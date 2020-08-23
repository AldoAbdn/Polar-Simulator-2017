import pygame
class Screen(object):
    """Holds the display and draw objects onto it"""

    def __init__(self, screenRes,drawableObjects=None):
        self.screenResolution = screenRes
        self.surface = pygame.display.set_mode(self.screenResolution)
        self.rect = self.surface.get_rect()
        self.objects = drawableObjects
        self.backgroundImage = pygame.image.load("Assets/northpole.jpg").convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (self.rect.width, self.rect.height)).convert() #Scales image to screen res

    def draw(self):
        #Fill Background
        self.surface.blit(self.backgroundImage, self.rect)
        for object in self.objects:
            object.draw(self.surface)
        pygame.display.update()

    def setObjects(self, value):
        self.objects = value

    def getScreenResolution(self):
        return self.screenResolution




