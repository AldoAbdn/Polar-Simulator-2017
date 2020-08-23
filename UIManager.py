import pygame
from EventManager import EventManager
from EventHandlers import SokobanUIManagerEventHandlers
from EventHandlers import IntroUIManagerEventHandlers
from EventHandlers import ScoreUIManagerEventHandlers
from EventHandlers import ChooseResolutionUIManagerEventHandlers
from EventHandlers import PauseUIManagerEventHandlers

class UIManager(object):
    """Used to store buttons and text, includes click functions"""

    def __init__(self, text, buttons, res):
        self.text = text
        self.buttons = buttons
        self.resolution = res
        self.rect = pygame.rect.Rect((0,0),(res))
        self.eventHandlers = None

    #Getters
    def getResolution(self):
        return self.resolution

    def getButtons(self):
        return self.buttons

    def getEventHandlers(self):
        return self.eventHandlers

    def getText(self):
        return self.text

    def __getSurface__(self):
        return self.surface

    def __getRect__(self):
        return self.rect

    #Setters
    def setResolution(self, value):
        self.resolution = value

    def __setButtons__(self, value):
        self.buttons = value

    def __setText__(self, value):
        self.text = value

    def __setSurface__(self, value):
        self.surface = value

    def __setRect__(self, value):
        self.rect = value

    def __setEventHandlers(self, value):
        self.eventHandlers = value

    #Special
    def draw(self, surface):
        for key in self.text:
            self.text[key].draw(surface)
        for key in self.buttons:
            self.buttons[key].draw(surface)

    def scale(self, newRes):
        xScale = newRes[0] / self.resolution[0]
        yScale = newRes[1] / self.resolution[1]
        scale = (xScale, yScale)
        self.surface = pygame.transform.scale(self.surface, self.rect.width * xScale, self.rect.height * yScale)
        for key in self.text:
            self.text[key].scale(scale)
        for key in self.buttons:
           self.buttons[key].scale(scale)

class PauseUIManager(UIManager):
    """Used to store buttons and text, includes click functions"""

    def __init__(self,text, buttons, res):
        UIManager.__init__(self, text, buttons, res)
        self.eventHandlers = PauseUIManagerEventHandlers(self)
        self.buttons["Unpause"].setPosition((res[0] * 0.90, res[1] * 0.075))
        self.buttons["Reset"].setPosition((res[0] / 2, res[1] * 0.2))
        self.buttons["Fullscreen"].setPosition((res[0] / 2, res[1] * 0.4))
        self.buttons["Restart"].setPosition((res[0] / 2, res[1] * 0.6))
        self.buttons["Quit"].setPosition((res[0] / 2, res[1] * 0.8))

class ChooseResolutionUIManager(UIManager):
    """Used to store buttons and text, includes click functions"""

    def __init__(self,text, buttons, res):
        UIManager.__init__(self, text, buttons, res)
        self.eventHandlers = ChooseResolutionUIManagerEventHandlers(self)
        pygame.display.set_caption("Sokoban")
        self.buttons["720"].setPosition((res[0] / 2, res[1] * 0.4))
        self.buttons["480"].setPosition((res[0] / 2, res[1] * 0.6))

class IntroUIManager(UIManager):
    """Used to store buttons and text, includes click functions"""

    def __init__(self,text, buttons, res):
        UIManager.__init__(self, text, buttons, res)
        self.eventHandlers = IntroUIManagerEventHandlers(self)
        self.buttons["Start"].setPosition((res[0] / 2, res[1] * 0.75))
        self.buttons["Quit"].setPosition((res[0]/2,res[1] * 0.90))

class SokobanUIManager(UIManager):
    """Used to store buttons and text, includes click functions"""

    def __init__(self, text, buttons, res):
        UIManager.__init__(self, text, buttons, res)
        self.eventHandlers = SokobanUIManagerEventHandlers(self)
        self.rect = pygame.rect.Rect((0,0),(res[0], res[1]/7))
        self.buttons["Pause"].setPosition((self.rect.width * 0.90, res[1] * 0.075))
        self.gap = self.rect.width * 0.17
        self.initialXPos = self.rect.width*0.07
        self.text["room"].setPosition((self.initialXPos, self.rect.height*0.50))
        self.text["totalMoves"].setPosition((self.initialXPos + self.gap, self.rect.height*0.50))
        self.text["moves"].setPosition((self.initialXPos + self.gap * 2, self.rect.height*0.50))

class ScoreUIManager(UIManager):
    """Used to store buttons and text, includes click functions"""

    def __init__(self,text, buttons, res):
        UIManager.__init__(self, text, buttons, res)
        self.eventHandlers = ScoreUIManagerEventHandlers(self)
        self.buttons["Restart"].setPosition((res[0] / 2, res[1] * 0.75))
        self.text["Total Moves"].setFontSize(40)
        self.text["Total Moves"].setPosition((res[0]/2, res[1] * 0.25))

    def setScore(self, score):
        self.text["Total Moves"].updateText("Total Moves: " + str(score), True) #Used to set final display score at end of game





