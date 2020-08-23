import pygame
class Text(object):
    def __init__(self, text, fontSize=12, fontColour = (128,128,128),centre=(0,0)):
        self.text = text
        self.colour = fontColour
        self.fontSize = fontSize
        self.font = pygame.font.SysFont("Arial Black", self.fontSize)
        self.surface = self.font.render(self.text, True, self.colour)
        self.rect = self.surface.get_rect()
        self.rect.center = centre

    #Getters
    def getSurface(self):
        return self.surface

    def getRect(self):
        return self.rect

    def __getText__(self):
        return self.text

    def __getFont__(self):
        return self.font

    def __getFontSize__(self):
        return self.fontSize

    def __getColour__(self):
        return self.colour

    #Setters
    def setFontSize(self, value):
        self.fontSize = value
        self.font = pygame.font.SysFont("Arial Black", self.fontSize)
        self.__updateSurface__()
        self.__updateRect__()

    def setColour(self, value):
        self.colour = value
        self.__updateSurface__()

    def __setText__(self, text):
        self.text = text

    #Special Methods
    def draw(self, display):
        display.blit(self.surface, self.rect)

    def scale(self, scale): #Scales text
        self.rect.center = (self.rect.x * scale[0], self.rect.y * scale[1])

    def setPosition(self, pos):
        self.rect.center = pos

    def updateText(self, text, updateRect = False): #Used to change text once a text object has been instantiated
        self.__setText__(text)
        self.__updateSurface__()
        if updateRect:
            self.__updateRect__()
        pygame.display.update()

    def __updateSurface__(self): #Used to rerender text in the text value needs to be changed
        self.surface = self.font.render(self.text, True, self.colour)

    def __updateRect__(self):
        center = self.rect.center
        self.rect = self.surface.get_rect()
        self.rect.center = center




