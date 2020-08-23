from Text import Text
import pygame
class Button(object):
    def __init__(self,nonActivesrc, activesrc,hoversrc, center=(0,0)):
        self.nonActiveSurface = pygame.image.load(nonActivesrc)
        self.activeSurface = pygame.image.load(activesrc)
        self.hoverSurface = pygame.image.load(hoversrc)
        self.surface = self.nonActiveSurface
        self.rect = self.surface.get_rect()
        self.rect.center = center
        self.active = False
        self.hover = False

    #Getters
    def getSurface(self):
        return self.surface

    def getRect(self):
        return self.rect

    def getHover(self):
        return self.hover

    def __getActive__(self):
        return self.active

    #Setters
    def setSurface(self,value):
        self.surface = value

    def __setRect__(self,value):
        self.rect = value

    def __setActive__(self, value):
        self.active = value

    def __setHover__(self, value):
        self.hover = value
        
    #Special
    def draw(self, display):
        display.blit(self.surface, self.rect)

    def setPosition(self, pos):
        self.rect.center = pos

    def toggleActive(self, active=None):
        if active == None:
            self.active = not self.active
        else:
            self.__setActive__(active)
        if self.active:
            self.surface = self.activeSurface
        else:
            self.surface = self.nonActiveSurface

    def toggleHover(self, hover=None):
        if hover == None:
            self.hover = not self.hover
        else:
            self.__setHover__(hover)
        if self.hover:
            self.surface = self.hoverSurface
        else:
            self.surface = self.nonActiveSurface

    def scale(self, scale):
        self.rect = pygame.Rect(self.rect.x * scale[0], self.rect.y * scale[1], self.rect.width * scale[0], self.rect.height * scale[1])


