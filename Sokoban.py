#Alistair Quinn
#Sokoban v1.0 - 27/11/2016
#Sokoban submission for Object Oriented Programming Course

import pygame,sys,os
os.environ['SDL_VIDEO_CENTERED'] = '1' #This (hopefully) centres the window, by suggesting to the os to put it here
from Text import Text
from Button import Button
from SurfaceManager import SurfaceManager
from EventManager import EventManager
from EventManager import SokobanEventManager
from EventManager import GameEventManager
from EventManager import IntroEventManager
from EventManager import ScoreEventManager
from EventManager import ChooseResolutionEventManager
from RoomManager import RoomManager
from UIManager import SokobanUIManager
from UIManager import IntroUIManager
from UIManager import ScoreUIManager
from UIManager import ChooseResolutionUIManager
from EventHandlers import SokobanEventHandlers
from EventHandlers import GameEventHandlers
from SoundManager import SoundManager
from Room import Room
from Grid import Grid
from WarehouseKeeper import WarehouseKeeper
from Crate import Crate
from Wall import Wall
from Tile import Tile
from Tile import Diamond

pygame.init()

#TOP LEVEL CLASS
class Game(object):
    """Manages the game, sets the res and creates instances of all the scenes. Starts the music"""
    def __init__(self):
        #Display setup
        self.resolution = () #This is filled by ChooseResolution scene(further down this page)
        self.display = pygame.display.set_mode((400,400))
        self.fullScreen = False
        #Scene management
        self.scenes = {"ChooseRes": ChooseResolution()} 
        self.currentScene = self.scenes["ChooseRes"]
        self.currentSceneKey = "ChooseRes"
        self.soundManager = SoundManager() #Plays the musics and used to call sounds in the game
        self.eventHandlers = GameEventHandlers(self) #Stores event handlers that work with an event manager. So that an event manager does not have direct control of any of the scenes or game
        self.eventManager = GameEventManager(self.eventHandlers, self.soundManager.eventHandlers) #Handles game wide events, like music volume and fullscreen toggle
        self.main() #Main game loop

    def main(self):
        while True:
            events = pygame.event.get()
            self.run(events)

    def run(self, events):
        #Handles current scene first
        self.currentScene.run(self.display, events)
        #Events
        self.eventManager.run(events)

    def nextScene(self):
        #Swaps between the scenes, uses res from chooseRes to instantiate the scenes needed for the game at the correct scale(based on resolution chosen)
        if self.currentSceneKey == "ChooseRes":
            self.resolution = self.currentScene.uiManager.getResolution()
            self.display = pygame.display.set_mode(self.resolution)
            self.scenes["Intro"] = Intro(self.resolution)
            self.scenes["Sokoban"] = Sokoban(self.resolution)
            self.scenes["Score"] = Score(self.resolution)
            self.currentScene = self.scenes["Intro"]
            self.currentSceneKey = "Intro"
        elif self.currentSceneKey == "Intro":
            self.currentScene = self.scenes["Sokoban"]
            pygame.event.post(EventManager.Events["Restart"])
            self.currentSceneKey = "Sokoban"
        elif self.currentSceneKey == "Sokoban":
            self.currentScene = self.scenes["Score"]
            self.currentSceneKey = "Score"
            self.currentScene.uiManager.setScore(self.scenes["Sokoban"].getTotalScore())
        elif self.currentSceneKey == "Score":
            self.currentScene = self.scenes["Intro"]
            self.currentSceneKey = "Intro"

#TEMPLATE
class Scene(object):
    """A scene is like a level, or one section of the program. There will be an intro scene, the sokoban scene and an ending scene displaying the users score. This is a TEMPLATE class"""
    def __init__(self, screenRes =(640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager() #Handles the drawing of a scene, managers that have draw functions are added at the bottom of init using .setObjects()
        self.uiManager = UIManager() #UI managers keep all the buttons and text together, and position them 
        self.eventHandlers = EventHandlers() #Event Handlers
        self.eventManager = EventManager() #Manages event handlers
        self.surfaceManager.setObjects() #Sets objects that need drawn

    #events are handled and draw managers draw to main display
    def run(self, surface, events):
        #Events
        self.eventManager.run(events)
        #Draw
        self.surfaceManager.draw()

class ChooseResolution(Scene):
    def __init__(self, screenRes = (400,400)):
        self.surface = pygame.display.set_mode(screenRes)
        self.running = True
        self.surfaceManager = SurfaceManager(screenRes, "Assets/northpole.jpg") 
        self.uiManager = ChooseResolutionUIManager({"Instruction": Text("Please Choose a Resolution", (0,140,0), 50, 50)}, {"720": Button("720P",(32,32,32), (0,140,0), 400,440,screenRes[0]*0.2,screenRes[1]*0.1), "480": Button("480",(32,32,32), (0,140,0), 400,440,screenRes[0]*0.2,screenRes[1]*0.1)}, screenRes)
        self.eventManager = ChooseResolutionEventManager(self.uiManager.eventHandlers)
        self.surfaceManager.setObjects([self.uiManager])

class Intro(Scene):
    def __init__(self, screenRes = (640, 480)):
        self.surface = pygame.display.set_mode(screenRes)
        self.running = True
        self.surfaceManager = SurfaceManager(screenRes, "Assets/intro.jpg")
        self.uiManager = IntroUIManager({}, {"Start": Button("Start",(32,32,32), (0,140,0), 400,440,screenRes[0]*0.2,screenRes[1]*0.1)}, screenRes)
        self.eventManager = IntroEventManager(self.uiManager.eventHandlers)
        self.surfaceManager.setObjects([self.uiManager])
    
    def run(self, surface, events):
        #Events
        self.eventManager.run(events)
        #Draw
        self.surfaceManager.draw()

class Sokoban(Scene):
    """Main class of game that creates all 
    the other classes and stores the pygame display"""

    def __init__(self, screenRes = (640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(screenRes, "Assets/northpole.jpg")
        self.roomManager = RoomManager(screenRes) #Sokoban needs an extra manager for all the levels that contain sprites
        self.uiManager = SokobanUIManager({"room":Text("Room: 1", (0,255,0), 30,440),"totalMoves": Text("Total Moves: 0", (0,255,0),130,440),"moves":Text("Moves: 0",(0,255,0),230,440)}, {"Reset": Button("Reset",(32,32,32), (0,140,0), 400,440,screenRes[0]*0.1, screenRes[1]*0.05)}, screenRes)
        self.eventHandlers = SokobanEventHandlers(self)
        self.eventManager = SokobanEventManager(self.eventHandlers, self.roomManager.eventHandlers, self.roomManager.currentRoom.eventHandlers, self.uiManager.eventHandlers)
        self.surfaceManager.setObjects([self.roomManager, self.uiManager])

    def getTotalScore(self): 
        return self.roomManager.getTotalMoves()

class Score(Scene):
    """Main class of game that creates all 
    the other classes and stores the pygame display"""

    def __init__(self, screenRes = (640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(screenRes, "Assets/northpole.jpg")
        self.roomManager = RoomManager(screenRes)
        self.uiManager = ScoreUIManager({"Total Moves": Text("Total Moves: 0", (0,255,0),130,440)}, {"Restart": Button("Restart",(32,32,32), (0,140,0), 560,440,130,40) }, screenRes)
        self.eventManager = ScoreEventManager(self.uiManager.eventHandlers)
        self.surfaceManager.setObjects([self.uiManager])
    

game = Game()



