#Alistair Quinn
#Sokoban v1.0 - 27/11/2016
#Puzzle game involving pushing boxes onto coloured blocks to complete rooms
#This file contains the top level and main scenes that make up the game

#SOURCES
#All buttons were created using www.dabuttonfactory.com
#Menu icon is from: https://www.iconfinder.com/icons/134216/hamburger_lines_menu_icon by Timothy Miller and has a creative commons liscence(available from url)
#Background image is from http://www.3dsceneries.com (watermark on bottom left of image)
#Music is a heavily edited 8bit version of Pacific Rim theme, original source can be found here: https://www.youtube.com/watch?v=hWHlOIKr_oY
#All other assets were created by me

import pygame,sys,os, threading
os.environ['SDL_VIDEO_CENTERED'] = '1' #This (hopefully) centres the window, by suggesting to the os to put it here
os.environ["PYGAME_FREETYPE"] = '1'

pygame.init()

#TOP LEVEL CLASS
class Game(object):
    """Manages the game, sets the res and creates instances of all the scenes. Starts the music"""
    def __init__(self):
        #Display setup
        self.resolution = (400,400) #This is filled by ChooseResolution scene(further down this page)
        self.display = pygame.display.set_mode((400,400))
        self.fullScreen = None #This is set to false later, this is to stop fullscreening choose res scene
        #Scene management
        self.scenes = {"ChooseRes": ChooseResolution(self.display)}
        self.currentScene = self.scenes["ChooseRes"]
        self.currentSceneKey = "ChooseRes"
        self.soundManager = SoundManager() #Plays the musics and used to call sounds in the game
        self.eventHandlers = GameEventHandlers(self) #Stores event handlers that work with an event manager. So that an event manager does not have direct control of any of the scenes or game
        self.eventManager = GameEventManager(self.eventHandlers, self.soundManager.eventHandlers) #Handles game wide events, like music volume and fullscreen toggle
        pygame.event.set_allowed([pygame.QUIT,pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN,EventManager.PLAYERMOVE, EventManager.RESET, EventManager.RESTART, EventManager.ROOMOVER, EventManager.SCENEOVER, EventManager.TRACKOVER])
        self.__main__() #Main game loop

    #Getters
    def getResolution(self):
        return self.resolution

    def getFullscreen(self):
        return self.fullScreen

    def getScene(self, scene):
        return self.scenes[scene]

    def getCurrentSceneKey(self):
        return self.currentSceneKey

    def getCurrentScene(self):
        return self.currentScene

    def __getDisplay__(self):
        return self.display

    def __getScenes__(self):
        return self.scenes

    def __getSoundManager__(self):
        return self.soundManager

    def __getEventHandlers__(self):
        return self.eventHandlers

    def __getEventManager__(self):
        return self.eventManager

    #Setters
    def setDisplay(self, value):
        self.display = value

    def __setResolution__(self, value):
        self.resolution = value

    def __setFullscreen__(self, value):
        self.fullScreen = value

    def __setScenes__(self, value):
        self.scenes = value

    def __setCurrentScene__(self, value):
        self.currentScene = value

    def __setCurrentSceneKey__(self, value):
        self.currentSceneKey = value

    def __setSoundManager__(self, value):
        self.soundManager = value

    def __setEventHandlers__(self, value):
        self.eventHandlers = value

    def __setEventManager__(self, value):
        self.eventManager = value

    #Special
    def nextScene(self):
        #Swaps between the scenes, uses res from chooseRes to instantiate the scenes needed for the game at the correct scale(based on resolution chosen)
        if self.currentSceneKey == "ChooseRes":
            self.resolution = self.currentScene.uiManager.getResolution()
            self.__setFullscreen__(False)
            self.display = pygame.display.set_mode(self.resolution, pygame.DOUBLEBUF)
            self.pause = False
            self.scenes["Intro"] = Intro(self.display,self.resolution)
            self.scenes["Sokoban"] = Sokoban(self.display,self.resolution)
            self.scenes["Score"] = Score(self.display, self.resolution)
            self.scenes["Pause"] = Pause(self.display, self.resolution)
            pygame.event.post(EventManager.Events["Reset"])
            self.setScene("Intro")
        elif self.currentSceneKey == "Pause":
            pygame.event.post(EventManager.Events["Restart"])
            pygame.event.post(EventManager.Events["Reset"])
            self.setScene("Intro")
        elif self.currentSceneKey == "Intro":
            pygame.event.post(EventManager.Events["Restart"])
            pygame.event.post(EventManager.Events["Reset"])
            self.setScene("Sokoban")
        elif self.currentSceneKey == "Sokoban":
            pygame.event.post(EventManager.Events["Reset"])
            self.setScene("Score")
            self.currentScene.uiManager.setScore(self.scenes["Sokoban"].getTotalScore())
        elif self.currentSceneKey == "Score":
            pygame.event.post(EventManager.Events["Reset"])
            self.setScene("Intro")


    def toggleFullscreen(self):
        if self.getFullscreen() == None:
            return
        self.__setFullscreen__(not self.getFullscreen())
        if self.getFullscreen():
            self.setDisplay(pygame.display.set_mode(self.getResolution(), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE))
        else:
            self.setDisplay(pygame.display.set_mode(self.getResolution()))

    def setScene(self, value):
        self.currentScene = self.scenes[value]
        self.currentSceneKey = value

    def pauseToggle(self):
        self.pause = not self.pause
        if self.currentSceneKey == "Sokoban" or self.currentSceneKey == "Pause":
            if self.pause:
                self.getScene("Pause").reset()
                self.setScene("Pause")
            else:
                self.setScene("Sokoban")

    def __main__(self):
        while True:
            events = pygame.event.get()
            self.__run__(events)

    def __run__(self, events):
        #Handles current scene first
        self.currentScene.run(self.display, events)
        #Events
        self.eventManager.run(events)

#SCENES
#TEMPLATE 
class Scene(object):
    """A scene is like a level, or one section of the program. There will be an intro scene, the sokoban scene and an ending scene displaying the users score. This is a TEMPLATE class"""
    def __init__(self, display,screenRes =(640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(display, screenRes) #Handles the drawing of a scene, managers that have draw functions are added at the bottom of init using .setObjects()
        self.uiManager = UIManager() #UI managers keep all the buttons and text together, and position them
        self.eventHandlers = EventHandlers() #Event Handlers
        self.eventManager = EventManager() #Manages event handlers
        self.surfaceManager.setObjects() #Sets objects that need drawn

    #Getters
    def __getRunning__(self):
        return self.running

    def __getSurfaceManager__(self):
        return self.surfaceManager

    def __getUiManager__(self):
        return self.uiManager

    def __getEventHandlers__(self):
        return self.eventHandlers

    def __getEventManager__(self):
        return self.eventManager

    def __getSurfaceManager__(self):
        return self.surfaceManager

    #Setters
    def __setRunning__(self, value):
        self.running = value

    def __setSurfaceManager__(self, value):
        self.surfaceManager = value

    def __setUiManager__(self, value):
        self.uiManager = value

    def __setEventHandlers__(self, value):
        self.eventHandlers = value

    def __setEventManager__(self, value):
        self.eventManager = value

    def __setSurfaceManager__(self, value):
        self.surfaceManager = value

    #events are handled and draw managers draw to main display
    def run(self, surface, events):
        #Events
        self.eventManager.run(events)
        #Draw
        self.surfaceManager.draw()

class Pause(Scene): #Pause screen only available during sokoban
    def __init__(self,display, screenRes = (400,400)):
        self.running = True
        self.surfaceManager = SurfaceManager(display,screenRes, "Assets/Pause.png")
        self.uiManager = PauseUIManager({}, {"Unpause": Button("Assets/pauseButton.png","Assets/pauseButton.png","Assets/pauseButton.png",(screenRes[0]*0.2,screenRes[1]*0.1)),"Reset": Button("Assets/resetButton.png","Assets/resetButtonActive.png","Assets/resetButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1)),"Fullscreen": Button("Assets/fullscreenButton.png","Assets/fullscreenButtonActive.png","Assets/fullscreenButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1)),"Restart": Button("Assets/RestartButton.png","Assets/RestartButtonActive.png","Assets/RestartButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1)), "Quit": Button("Assets/QuitButton.png", "Assets/QuitButtonActive.png","Assets/QuitButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1))}, screenRes)
        self.eventManager = PauseEventManager(self.uiManager.getEventHandlers())
        self.surfaceManager.setObjects([self.uiManager])

    def reset(self):
        self.eventManager.reset()

class ChooseResolution(Scene): #Lets user choose between two resolutions
    def __init__(self,display, screenRes = (400,400)):
        self.running = True
        self.surfaceManager = SurfaceManager(display,screenRes, "Assets/resolution.jpg")
        self.uiManager = ChooseResolutionUIManager({}, {"720": Button("Assets/720Button.png","Assets/720ButtonActive.png","Assets/720ButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1)), "480": Button("Assets/480Button.png", "Assets/480ButtonActive.png","Assets/480ButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1))}, screenRes)
        self.eventManager = ChooseResolutionEventManager(self.uiManager.getEventHandlers())
        self.surfaceManager.setObjects([self.uiManager])

class Intro(Scene): #Gives user choise to start or quit
    def __init__(self,display, screenRes = (640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(display,screenRes, "Assets/intro.jpg")
        self.uiManager = IntroUIManager({}, {"Start": Button("Assets/startButton.png","Assets/startButtonActive.png", "Assets/startButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1)), "Quit": Button("Assets/quitButton.png","Assets/quitButtonActive.png","Assets/quitButtonHover.png",(screenRes[0]*0.2,screenRes[1]*0.1))}, screenRes)
        self.eventManager = IntroEventManager(self.uiManager.getEventHandlers())
        self.surfaceManager.setObjects([self.uiManager])


class Sokoban(Scene): #Actual game
    def __init__(self, display,screenRes = (640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(display,screenRes, "Assets/northpole.jpg")
        self.roomManager = RoomManager(screenRes) #Sokoban needs an extra manager for all the levels that contain spriGaSotes
        self.uiManager = SokobanUIManager({"room":Text("Room: 1", 12,(0,255,0),(30,440)),"totalMoves": Text("Total Moves: 0", 12,(0,255,0),(130,440)),"moves":Text("Moves: 0",12,(0,255,0),(230,440))}, {"Pause": Button("Assets/pauseButton.png","Assets/pauseButton.png","Assets/pauseButton.png",(screenRes[0]*0.2,screenRes[1]*0.1))}, screenRes)
        self.eventHandlers = SokobanEventHandlers(self)
        self.eventManager = SokobanEventManager(self.eventHandlers, self.roomManager.eventHandlers, self.roomManager.currentRoom.eventHandlers, self.uiManager.getEventHandlers())
        self.surfaceManager.setObjects([self.roomManager, self.uiManager])

    def getTotalScore(self):
        return self.roomManager.getTotalMoves()

    def getEventManager(self):
        return self.eventManager

class Score(Scene): #Displays the users score
    def __init__(self, display,screenRes = (640, 480)):
        self.running = True
        self.surfaceManager = SurfaceManager(display,screenRes, "Assets/northpole.jpg")
        self.uiManager = ScoreUIManager({"Total Moves": Text("Total Moves: 0", 18,(0,255,0),(130,440))}, {"Restart": Button("Assets/restartButton.png","Assets/restartButtonActive.png","Assets/restartButtonHover.png",(130,40)) }, screenRes)
        self.eventManager = ScoreEventManager(self.uiManager.eventHandlers)
        self.surfaceManager.setObjects([self.uiManager])

#SOUND MANAGER
class SoundManager(object):
    """Used to play music and sounds in the game in the game"""
    Sounds = {"Push":pygame.mixer.Sound("Assets/push.ogg")}

    def __init__(self, tracks=["Assets/gunReload.ogg","Assets/music.ogg"]):
        self.tracks = tracks #Track list
        self.volume = 1
        self.previousVolume = 1
        self.currentTrack = self.tracks[0]
        self.currentTrackIndex = 0
        self.eventHandlers = SoundManagerEventHandlers(self)
        pygame.mixer.music.set_endevent(EventManager.TRACKOVER)
        self.play()

    #Getters
    def getVolume(self):
        return self.volume

    def getCurrentTrackIndex(self):
        return self.currentTrackIndex

    def getTracks(self):
        return self.tracks

    def __getPreviousVolume__(self):
        return self.previousVolume

    def __getCurrentTrack__(self):
        return self.currentTrack

    def __getEventHandlers__(self):
        return self.eventHandlers

    #Class methods
    @classmethod  
    def playSound(self, sound): #Used to play single sounds in the game
        SoundManager.Sounds[sound].play()

    #Setters
    def setCurrentTrack(self, index):
        self.currentTrackIndex = index
        self.currentTrack = self.tracks[self.currentTrackIndex]
        self.play()

    def setVolume(self, value):
        if value > 1 or value < 0:
            return
        self.volume = value
        pygame.mixer.music.set_volume(self.volume)

    def __setPreviousVolume__(self, value):
        self.previousVolume = value

    def __setCurrentTrackIndex__(self, value):
        self.currentTrackIndex = value

    def __setTracks__(self, value):
        self.tracks = value

    def __setEventHandlers__(self, value):
        self.eventHandlers = value

    #Special
    def play(self):
        pygame.mixer.music.load(self.currentTrack)
        pygame.mixer.music.play()

    def incrementVolume(self, value):
        self.setVolume(self.volume + value)

    def toggleMute(self):
        if self.volume == 0:
            self.setVolume(self.previousVolume)
        else:
            self.previousVolume = self.getVolume()
            self.setVolume(0)

    def nextTrack(self):
        self.currentTrackIndex += 1
        if self.currentTrackIndex == len(self.tracks):
            self.setCurrentTrack(0)
        else:
            self.setCurrentTrack(self.currentTrackIndex)

#SURFACE MANAGER
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

#UIMANAGER
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

#BUTTONS AND TEXT
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

#EVENT MANAGER
class EventManager(object):
    """Handles events in the game, posts custom events to pygame events que"""
    #Events in the game
    SCENEOVER = pygame.USEREVENT + 1
    ROOMOVER = pygame.USEREVENT + 2
    PLAYERMOVE = pygame.USEREVENT + 3
    RESET = pygame.USEREVENT + 4
    RESTART = pygame.USEREVENT + 5
    TRACKOVER = pygame.USEREVENT + 6
    FULLSCREEN = pygame.USEREVENT + 7
    PAUSE = pygame.USEREVENT + 8
    Events = {"Scene Over":pygame.event.Event(SCENEOVER), "Room Over": pygame.event.Event(ROOMOVER), "Player Move": pygame.event.Event(PLAYERMOVE), "Reset":pygame.event.Event(RESET), "Restart":pygame.event.Event(RESTART), "Track Over":pygame.event.Event(TRACKOVER), "Fullscreen":pygame.event.Event(FULLSCREEN), "Pause":pygame.event.Event(PAUSE)}

    def __init__(self):
        self.running = True

    #Getters
    def __getRunning__(self):
        return self.running

    #Setters
    def __setRunning__(self, value):
        self.running = value

    #Checks events, runs event handlers
    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == EventManager.PLAYERMOVE:
                pass
            elif event.type == EventManager.ROOMOVER:
                pass
            elif event.type == EventManager.SCENEOVER:
                pass
            elif event.type == EventManager.RESET:
                pass
            elif event.type == EventManager.RESTART:
                pass

    @classmethod
    def checkQuit(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#Handles events like volume and toggle fullscreen
class GameEventManager(EventManager):
    def __init__(self, gameEventHandlers, soundManagerEventHandlers):
        EventManager.__init__(self)
        self.gameEventHandlers = gameEventHandlers
        self.soundManagerEventHandlers = soundManagerEventHandlers

    #Getters
    def __getGameEventHandlers__(self):
        return self.gameEventHandlers

    def __getSoundManagerEventHandlers__(self):
        return self.soundManagerEventHandlers

    #Setters
    def __setGameEventHandlers__(self, value):
        self.setGameEventHandlers = value

    def __setSoundManagerEventHandlers__(self):
        self.soundManagerEventHandlers = value

    #Goes through list of events, event is handled by an event handler
    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.gameEventHandlers.quit()
            if event.type == pygame.KEYDOWN: #When a scene ends
                self.gameEventHandlers.keyPress(event)
                self.soundManagerEventHandlers.keyPress(event)
                continue
            if event.type == EventManager.SCENEOVER:
                self.gameEventHandlers.sceneOver()
                continue
            if event.type == EventManager.TRACKOVER: #When a song has stoped playing
                self.soundManagerEventHandlers.trackOver()
                continue
            if event.type == EventManager.FULLSCREEN:
                self.gameEventHandlers.fullscreen()
                continue
            if event.type == EventManager.RESET:
                self.gameEventHandlers.reset()
                continue
            if event.type == EventManager.PAUSE:
                self.gameEventHandlers.pause()


class PauseEventManager(EventManager):
    def __init__(self, pauseEventHandlers):
        EventManager.__init__(self)
        self.pauseEventHandlers = pauseEventHandlers

    #Getters
    def __getPauseEventHandlers__(self):
        return self.pauseEventHandlers

    #Setters
    def __setPauseEventHandlers__(self, value):
        self.pauseEventHandlers = value

    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def reset(self):
        self.pauseEventHandlers.reset()

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.pauseEventHandlers.click(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.pauseEventHandlers.hover(pos)

#This is used to see which of the two resolutoin buttons was pressed
class ChooseResolutionEventManager(EventManager):
    def __init__(self, chooseResolutionEventHandlers):
        EventManager.__init__(self)
        self.chooseResolutionEventHandlers = chooseResolutionEventHandlers

    #Getters
    def __getChooseResolutionEventHandlers__(self):
        return self.chooseResolutionEventHandlers

    #Setters
    def __setChooseResolutionEventHandlers__(self, value):
        self.chooseResolutionEventHandlers = value

    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.chooseResolutionEventHandlers.click(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.chooseResolutionEventHandlers.hover(pos)

#Detects when user clicks start
class IntroEventManager(EventManager):
    def __init__(self, introEventHandlers):
        EventManager.__init__(self)
        self.introEventHandlers = introEventHandlers

    #Getters
    def __getIntroEventHandlers__(self):
        return self.introEventHandlers

    #Setters
    def __setIntroEventHandlers__(self, value):
        self.introEventHandlers = value

    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.introEventHandlers.click(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.introEventHandlers.hover(pos)
            elif event.type == EventManager.RESET:
                self.introEventHandlers.reset()

#Handles all the events to run sokoban game, like when a user moves or when a player moves and text needs to be updated
class SokobanEventManager(EventManager):
    """Handles events in the game, posts custom events to events que"""

    def __init__(self, gameEventHandlers, roomManagerEventHandlers, currentRoomEventHandlers, uiManagerEventHandlers):
        EventManager.__init__(self)
        self.gameEventHandlers = gameEventHandlers
        self.roomManagerEventHandlers = roomManagerEventHandlers
        self.uiManagerEventHandlers = uiManagerEventHandlers
        self.currentRoomEventHandlers = currentRoomEventHandlers

    #Getters
    def __getGameEventHandlers__(self):
        return self.gameEventHandlers

    def __getRoomManagerEventHandlers__(self):
        return self.roomManagerEventHandlers

    def __getUiManagerEventHandlers__(self):
        return self.uiManagerEventHandlers

    def __getCurrentRoomEventHandlers__(self):
        return self.currentRoomEventHandlers

    #Setters
    def setCurrentRoomEventHandlers(self, value):
        self.currentRoomEventHandlers = value

    def __setGameEventHandlers__(self, value):
        self.gameEventHandlers = value

    def __setRoomManagerEventHandlers__(self, value):
        self.roomManagerEventHandlers = value

    def __setUiManagerEventHandlers__(self, value):
        self.uiManagerEventHandlers = value

    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)
        #room, totMoves, moves = self.roomManagerEventHandlers.update() #Gets all the values needed to update the display
        #self.uiManagerEventHandlers.update(room, totMoves, moves) #Updates the display with the new values

    def reset(self):
        self.uiManagerEventHandlers.reset(self.roomManagerEventHandlers.reset())
        self.currentRoomEventHandlers.reset()

    def __checkEvents__(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.currentRoomEventHandlers.keyPress(event) #Moves player
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.uiManagerEventHandlers.click(pos) #Checks for pause button press
                self.currentRoomEventHandlers.click(pos)
                continue
            elif event.type == EventManager.PLAYERMOVE: #When a player is ok to move this fires
                self.uiManagerEventHandlers.playerMove(self.roomManagerEventHandlers.playerMove())
                continue
            elif event.type == EventManager.ROOMOVER: #When a level ends
                self.currentRoomEventHandlers.roomOver()
                temp = self.roomManagerEventHandlers.roomOver()
                self.setCurrentRoomEventHandlers(temp[0]) #Room managers room over returns the new room
                self.uiManagerEventHandlers.roomOver(temp[1])
                continue
            elif event.type == EventManager.RESET: #Resets a room
                self.reset()
                continue
            elif event.type == EventManager.RESTART:
                self.setCurrentRoomEventHandlers(self.roomManagerEventHandlers.restart()) #When the game needs restarted
                self.uiManagerEventHandlers.restart()
                continue

class ScoreEventManager(EventManager):
    def __init__(self, scoreEventHandlers):
        EventManager.__init__(self)
        self.scoreEventHandlers = scoreEventHandlers

    #Getters
    def __getScoreEventHandlers__(self):
        return self.scoreEventHandlers

    #Setters
    def __setScoreEventHandlers__(self, value):
        self.scoreEventHandlers = value

    def run(self, events):
        if events == []:
            return
        else:
            self.__checkEvents__(events)

    def __checkEvents__(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: #This checks if user clicks restart button
                pos = pygame.mouse.get_pos()
                self.scoreEventHandlers.click(pos)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.scoreEventHandlers.hover(pos)
            elif event.type == EventManager.RESET:
                self.scoreEventHandlers.reset()

#EVENT HANDLERS
class EventHandlers(object):
    """Container to hold eventHandlers, used by an event manager. Contains a reference to the object it is the event handler of"""

    def __init__(self, object):
        self.object = object

    #Getters
    def __getObject__(self):
        return self.object

    #Setters
    def __setObject__(self, value):
        self.object = value

    #Specialob
    def quit(self):
        return False

    def keyPress(self, event=None):
        return False

    def click(self, pos =None):
        return False

    def hover(self, pos=None):
        return False

    def playerMoved(self):
        return False

    def roomOver(self):
        return False

    def sceneOver(self):
        return False

    def reset(self):
        return False

    def restart(self):
        return False

    def update(self):
        return False

    def pause(self):
        return False

    def fullscreen(self):
        return False

    def trackOver(self):
        return False

class GameEventHandlers(EventHandlers):
    """Top level class event handlers"""
    def __init__(self, game):
        EventHandlers.__init__(self, game)

    def keyPress(self,event):
        if event.key == pygame.K_f: #Toggles fullscreen mode
            self.object.toggleFullscreen()
        elif event.key == pygame.K_ESCAPE:
            self.object.pauseToggle()

    def fullscreen(self):
        self.object.toggleFullscreen()

    def sceneOver(self): #When the scene over event is fired, this navigates between the scenes
        self.object.nextScene()

    def reset(self):
        if self.object.getCurrentSceneKey() == "Pause": #If paused, delegates reset to sokoban event manager as its the room that needs reset not the pause menu
            eventManager = self.object.getScene("Sokoban").getEventManager()
            eventManager.reset() #This resets current room
            self.object.pauseToggle() #Un pauses game so user can see effect

    def pause(self):
        self.object.pauseToggle()

    def quit(self): #Exits game
        pygame.quit()
        sys.exit()

class SoundManagerEventHandlers(EventHandlers):
    """Event handlers for sound manager, used to mute and change volume of music, to move onto the next track when one finishes"""
    def __init__(self, soundManager):
        EventHandlers.__init__(self,soundManager)

    def keyPress(self, event): #Controls volume of music
        if event.key == pygame.K_PAGEUP:
            self.object.incrementVolume(0.1)
        elif event.key == pygame.K_PAGEDOWN:
            self.object.incrementVolume(-0.1)
        elif event.key == pygame.K_m:
            self.object.toggleMute()

    def trackOver(self): #Plays the next track when a song ends
        if self.object.getCurrentTrackIndex() == len(self.object.getTracks()):
            self.object.setCurrentTrack(0)
        else:
            self.object.nextTrack()

class SokobanEventHandlers(EventHandlers):
    def __init__(self, Sokoban):
        EventHandlers.__init__(self,Sokoban)

    def roomOver(self): #When a level is over, changes level, when all levels are done room manager fires scene over event
        roomManager = self.object.getRoomManager()
        room = roomManager.getCurrentRoom()
        eventManager = self.object.getEventManager()
        eventManager.setCurrentRoomEventHandlers(room.getEventHandlers())

class RoomManagerEventHandlers(EventHandlers):
    def __init__(self, roomManager):
        EventHandlers.__init__(self,roomManager)

    def playerMove(self): #Updates the moves displayed onscreen when the player moves
        self.object.incrementTotalMoves(1)
        return (self.object.getMoves(), self.object.getTotalMoves())

    def roomOver(self): #Switches rooms
        isGameOver = not self.object.nextRoom()
        if isGameOver:
            pygame.event.post(EventManager.Events["Scene Over"])
        return (self.object.getCurrentRoom().getEventHandlers(), self.object.getLevel()) #Returns the currents room event handlers

    def reset(self):
        moves = self.object.getMoves()
        self.object.totalMoves -= moves
        return (self.object.getTotalMoves())

    def restart(self):
        self.object.totalMoves = 0
        for room in self.object.rooms:
            roomEventHandlers = room.getEventHandlers()
            roomEventHandlers.reset()
            room.setMoves(0)
        self.object.setCurrentRoom(0)
        return self.object.getCurrentRoom().getEventHandlers()

class RoomEventHandlers(EventHandlers):
    def __init__(self, room):
        EventHandlers.__init__(self,room)

    def keyPress(self, event): #Makes players move and push crates
        if event.key == pygame.K_w: #W key
            self.object.playerMove("UP")
        elif event.key == pygame.K_s: #S key
            self.object.playerMove("DOWN")
        elif event.key == pygame.K_a: #A key
            self.object.playerMove("LEFT")
        elif event.key == pygame.K_d: #D key
            self.object.playerMove("RIGHT")
        elif event.key == pygame.K_r:
            pygame.event.post(EventManager.Events["Reset"])

    def click(self, pos):
        self.object.clickPlayerMove(pos)

    def reset(self): #Resets a level is the user gets stuck and pushes reset button
        self.object.setMoves(0)
        grid = self.object.getGrid()
        grid.reset()

    def roomOver(self): #When a room is over reset
        self.reset()

class PauseUIManagerEventHandlers(EventHandlers):
    def __init__(self, uimanager):
        EventHandlers.__init__(self,uimanager)

    def click(self, pos): #User can select start or quit the game
        buttons = self.object.getButtons()
        if buttons["Unpause"].getRect().collidepoint(pos):
            buttons["Unpause"].toggleActive(True)
            pygame.event.post(EventManager.Events["Pause"])
        elif buttons["Restart"].getRect().collidepoint(pos):
            buttons["Restart"].toggleActive(True)
            t = threading.Timer(1,lambda:pygame.event.post(EventManager.Events["Scene Over"])).start()
        elif buttons["Reset"].getRect().collidepoint(pos):
            buttons["Reset"].toggleActive(True)
            pygame.event.post(EventManager.Events["Reset"])
        elif buttons["Fullscreen"].getRect().collidepoint(pos):
            buttons["Fullscreen"].toggleActive(True)
            pygame.event.post(EventManager.Events["Fullscreen"])
        elif buttons["Quit"].getRect().collidepoint(pos):
            buttons["Quit"].toggleActive(True)
            pygame.quit()
            sys.exit()

    def hover(self, pos): #used to change button image when button moused over
        buttons = self.object.getButtons()
        if buttons["Restart"].getRect().collidepoint(pos):
            buttons["Restart"].toggleHover(True)
        elif buttons["Reset"].getRect().collidepoint(pos):
            buttons["Reset"].toggleHover(True)
        elif buttons["Fullscreen"].getRect().collidepoint(pos):
            buttons["Fullscreen"].toggleHover(True)
        elif buttons["Quit"].getRect().collidepoint(pos):
            buttons["Quit"].toggleHover(True)
        else:
            if not buttons["Restart"].getHover() and not buttons["Reset"].getHover() and not buttons["Fullscreen"] and not buttons["Quit"].getHover():
                return
            if buttons["Restart"].getHover():
                buttons["Restart"].toggleHover(False)
            if buttons["Reset"].getHover():
                buttons["Reset"].toggleHover(False)
            if buttons["Fullscreen"].getHover():
                buttons["Fullscreen"].toggleHover(False)
            if buttons["Quit"].getHover():
                buttons["Quit"].toggleHover(False)

    def reset(self):
        buttons = self.object.getButtons()
        buttons["Restart"].toggleActive(False)
        buttons["Reset"].toggleActive(False)
        buttons["Fullscreen"].toggleActive(False)

class ChooseResolutionUIManagerEventHandlers(EventHandlers):
    def __init__(self, uimanager):
        EventHandlers.__init__(self,uimanager)

    def click(self, pos): #User clicks one of two buttons to pick resolution for the game window
        buttons = self.object.getButtons()
        if buttons["720"].getRect().collidepoint(pos):
            self.object.setResolution((1280,720))
            buttons["720"].toggleActive(True)
            t = threading.Timer(1,lambda:pygame.event.post(EventManager.Events["Scene Over"])).start()
        elif buttons["480"].getRect().collidepoint(pos):
            self.object.setResolution((640,480))
            buttons["480"].toggleActive(True)
            t = threading.Timer(1,lambda:pygame.event.post(EventManager.Events["Scene Over"])).start()

    def hover(self, pos): #used to change button image when button moused over
        buttons = self.object.getButtons()
        if buttons["720"].getRect().collidepoint(pos):
            buttons["720"].toggleHover(True)
        elif buttons["480"].getRect().collidepoint(pos):
            buttons["480"].toggleHover(True)
        else:
            if not buttons["720"].getHover() and not buttons["480"].getHover():
                return
            if buttons["720"].getHover():
                buttons["720"].toggleHover(False)
            if buttons["480"].getHover():
                buttons["480"].toggleHover(False)

    def reset(self):
        buttons = self.object.getButtons()
        buttons["720"].toggleActive(False)
        buttons["480"].toggleActive(False)

class IntroUIManagerEventHandlers(EventHandlers):
    def __init__(self, uimanager):
        EventHandlers.__init__(self,uimanager)

    def click(self, pos): #User can select start or quit the game
        buttons = self.object.getButtons()
        if buttons["Start"].getRect().collidepoint(pos):
            buttons["Start"].toggleActive(True)
            t = threading.Timer(1,lambda:pygame.event.post(EventManager.Events["Scene Over"])).start()
        elif buttons["Quit"].getRect().collidepoint(pos):
            buttons["Quit"].toggleActive(True)
            pygame.quit()
            sys.exit()
    def hover(self, pos): #used to change button image when button moused over
        buttons = self.object.getButtons()
        if buttons["Start"].getRect().collidepoint(pos):
            buttons["Start"].toggleHover(True)
        elif buttons["Quit"].getRect().collidepoint(pos):
            buttons["Quit"].toggleHover(True)
        else:
            if not buttons["Start"].getHover() and not buttons["Quit"].getHover():
                return
            if buttons["Start"].getHover():
                buttons["Start"].toggleHover(False)
            if buttons["Quit"].getHover():
                buttons["Quit"].toggleHover(False)

    def reset(self):
        buttons = self.object.getButtons()
        buttons["Start"].toggleActive(False)

class SokobanUIManagerEventHandlers(EventHandlers):
    def __init__(self, uimanager):
        EventHandlers.__init__(self,uimanager)

    def click(self, pos): #User clicks one of two buttons to pick resolution for the game window
        buttons = self.object.getButtons()
        if buttons["Pause"].getRect().collidepoint(pos):
            pygame.event.post(EventManager.Events["Pause"])

    def playerMove(self,movesTurple):
        text = self.object.getText()
        text["moves"].updateText("Moves: " + str(movesTurple[0]))
        text["totalMoves"].updateText("Total Moves: " + str(movesTurple[1]))

    def roomOver(self, room):
        text = self.object.getText()
        text["room"].updateText("Room: " + str(room))
        text["moves"].updateText("Moves: 0")

    def reset(self, totalMoves):
        text = self.object.getText()
        text["totalMoves"].updateText("Total Moves: " + str(totalMoves))
        text["moves"].updateText("Moves: 0")

    def restart(self):
        text = self.object.getText()
        text["room"].updateText("Room: 1")
        text["totalMoves"].updateText("Total Moves: 0")
        text["moves"].updateText("Moves: 0")

class ScoreUIManagerEventHandlers(EventHandlers):
    def __init__(self, uimanager):
        EventHandlers.__init__(self,uimanager)

    def click(self, pos): #User can restart the game if they want to
        buttons = self.object.getButtons()
        if buttons["Restart"].getRect().collidepoint(pos):
            buttons["Restart"].toggleActive(True)
            t = threading.Timer(1,lambda:pygame.event.post(EventManager.Events["Scene Over"])).start()

    def hover(self, pos): #used to change button image when button moused over
        buttons = self.object.getButtons()
        if buttons["Restart"].getRect().collidepoint(pos):
            buttons["Restart"].toggleHover(True)
        else:
            if not buttons["Restart"].getHover():
                return
            if buttons["Restart"].getHover():
                buttons["Restart"].toggleHover(False)

    def reset(self):
        buttons = self.object.getButtons()
        buttons["Restart"].toggleActive(False)

#ROOM MANAGER
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

#ROOM
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

#GRID
class Grid(object):
    """Will hold grid positions for drawn grid, and hold what objects are in each grid square"""
    map1 = [["x","x","x","x","x","x","x","x"],
            ["x","x","x","D","x","x","x","x"],
            ["x","x","x","C","C","D","x","x"],
            ["x","D","T","C","P","x","x","x"],
            ["x","x","x","x","C","x","x","x"],
            ["x","x","x","x","D","x","x","x"],
            ["x","x","x","x","x","x","x","x"]]

    map2 = [["x","x","x","x","x","x","x"],
            ["x","T","T","T","D","x","x"],
            ["x","C","x","x","T","x","x"],
            ["x","T","T","P","T","T","x"],
            ["x","T","x","T","C","T","x"],
            ["x","D","T","T","x","x","x"],
            ["x","x","x","x","x","x","x"]]

    map3 = [["x","x","x","x","x","x","x","x"],
            ["x","T","T","x","D","D","D","x"],
            ["x","T","C","C","C","T","T","x"],
            ["x","T","T","P","T","T","T","x"],
            ["x","T","T","x","x","x","x","x"],
            ["x","T","T","x","x","x","x","x"],
            ["x","x","x","x","x","x","x","x"]]

    map4 = [["x","x","x","x","x","x","x","x","x","x","x"],
            ["x","x","x","x","x","x","x","D","T","T","x"],
            ["x","x","x","x","x","x","x","D","x","T","x"],
            ["x","x","x","x","x","x","x","D","x","T","x"],
            ["x","T","T","P","C","T","C","T","C","T","x"],
            ["x","T","x","T","x","T","x","T","x","x","x"],
            ["x","T","T","T","T","T","T","T","x","x","x"],
            ["x","x","x","x","x","x","x","x","x","x","x"]]

    map5 = [["x","x","x","x","x","x","x","x","x"],
            ["x","x","x","T","T","x","x","x","x"],
            ["x","T","T","T","T","T","C","P","x"],
            ["x","T","x","T","C","x","C","T","x"],
            ["x","T","D","D","D","x","T","T","x"],
            ["x","x","x","x","x","x","x","x","x"]]

    def __init__(self, map, screenres=(640,400)):
        #self.surface =
        self.SCREENRATIO = screenres[0]/screenres[1]
        self.rows = len(map)
        self.cols = len(map[0])
        self.surfaceResolution = screenres
        tileSizeX = screenres[0] / self.cols
        tileSizeY = screenres[1] / self.rows
        self.tileSize = (int(tileSizeX), int(tileSizeY))
        self.speed = (0.020833333333 * self.surfaceResolution[0], 0.020833333333 * self.surfaceResolution[1])
        self.gridPositions = []
        for i in range(0,self.rows):
            self.gridPositions.append([])
            for j in range(0,self.cols):
                self.gridPositions[i].append(j)
        self.populateGridPositions() #Populates positions list with coordinates

        if map != None:
            self.gridItems = self.generateGridFromMap(map)
        else:
            self.gridItems = None

    #Getters
    def getPosition(self, coor):
        return self.gridPositions[coor[0]][coor[1]]

    def getItems(self, row, col):
        return self.gridItems[row][col]

    def getPlayer(self): #Returns the one player that should be in the grid
        items = self.gridItems
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, WarehouseKeeper):
                            return k
        return False

    def getCrates(self): #Returns the list of crates.
        items = self.gridItems
        crates = []
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, Crate):
                            crates.append(k)
        return crates

    def getDiamonds(self): #Returns the list of diamonds.
        items = self.gridItems
        diamonds = []
        if items != None:
            for j in range(0,self.rows):
                for i in range(0,self.cols):
                    for k in items[j][i]:
                        if isinstance(k, Diamond):
                            diamonds.append(k)
        return diamonds

    def __getGridPositions__(self):
        return self.gridPostions

    def __getGridItems__(self):
        return self.gridItems

    def __getMovableSprites__(self): #Gets all the movable type sprites, used for drawing later
        items = self.gridItems
        movableSprites = []
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                for k in items[j][i]:
                    if isinstance(k, MovableSprite):
                        movableSprites.append(k)
        return movableSprites

    #Setters
    def __setGridPositions__(self,Value):
        self.gridPositions = Value

    def __setGridItems__(self, value):
        self.gridItems = value

    def __setPos__(self, row, col, value):
        self.gridPostions[row][col] = value

    def __setItems__(self, row, col, value):
        self.gridItems[row][col] = value

    #String
    def toString(self):
        return isinstance.__class__.__name__ + ": Grid " + str(self.Grid)

    #Special
    def draw(self, surface): #Loops through item multi-dim array and calls draw function on each
        movingSprites = [] #Holds moving sprites so they can be animated
        items = self.gridItems
        player = self.getPlayer()
        #Add player to movablesprite list
        if not player.comparePos(self.getPosition(player.getCoordinates())) or (player.getMoving() and player not in movingSprites):
            movingSprites.insert(0, player)
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                for sprite in items[j][i]:
                    if isinstance(sprite, Crate): #Adds crates to movableSprite list
                        if not sprite.comparePos(self.getPosition(sprite.getCoordinates())) or (sprite.getMoving() and sprite not in movingSprites):
                            movingSprites.append(sprite)
                        else:
                            sprite.draw(surface)
                    elif isinstance(sprite, Wall):
                        pass
                    else:
                        sprite.draw(surface)
        if movingSprites != []:
            self.move(movingSprites) #Animates moving sprites
        self.drawMovable(surface) #Draws movable objects

    def drawMovable(self, surface): #Draws movable sprites
        movableSprites = self.__getMovableSprites__()
        for sprite in movableSprites:
            sprite.draw(surface)

    def move(self, sprites): #Takes in movable sprites, moves them if they need to be
        for sprite in sprites:
            currentCoords = sprite.getCoordinates()
            targetPos = self.gridPositions[currentCoords[0]][currentCoords[1]]
            finishedMoving = sprite.move(targetPos)
            if finishedMoving:
                sprites.remove(sprite)
                self.addItem(sprite)

    def getItemByPos(self, pos):
        gridItems = self.gridItems
        for row in gridItems:
            for col in row:
                for sprite in col:
                    if sprite.getRect().collidepoint(pos):
                        return sprite
        return False

    def convertCoordsToDirection(self, coords):
        playerCoords = self.getPlayer().getCoordinates()
        if coords[0] == playerCoords[0] - 1:
            return "UP"
        elif coords[0] == playerCoords[0] + 1:
            return "DOWN"
        elif coords[1] == playerCoords[1] - 1:
            return "LEFT"
        elif coords[1] == playerCoords[1] + 1:
            return "RIGHT"
        else:
            return False

    def predictPlayerPossibleCoords(self):
        player = self.getPlayer()
        currentCoords = player.getCoordinates()
        coords = [(currentCoords[0]+1,currentCoords[1]), (currentCoords[0]-1,currentCoords[1]), (currentCoords[0], currentCoords[1]+1), (currentCoords[0], currentCoords[1]-1)]
        return coords

    def populateGridPositions(self): #Generates rect center positions based tileSize that was generated from the resolution
        xGap = (self.surfaceResolution[0] - (self.tileSize[0] * self.cols) ) / 2
        yGap = (self.surfaceResolution[1] - (self.tileSize[1] * self.rows) ) / 2
        startX = int(self.tileSize[0] / 2 + xGap) #Starting Center value for first square
        startY = int(self.tileSize[1] / 2 + yGap) #Starting Center value for first Square
        X = startX
        Y = startY
        for j in range(0, self.rows): #Loops through each row
            X = startX
            if j != 0:
                Y+=int(self.tileSize[1]) #Gap between each center
            for i in range(0, self.cols): #Goes through each position in self.rows

                if i != 0:
                    X+=int(self.tileSize[0]) #Gap between each center
                self.gridPositions[j][i] = (X,Y)

    def generateGridFromMap(self, map): #Takes in a a map, gets num rows and columns and then creates a list from the map with all the objects
        self.rows = len(map)
        self.cols = len(map[0])
        levelMap = map
        gridItems = []
        for i in range(0, self.rows):
            gridItems.append([])
            for j in range(0, self.cols):
                gridItems[i].append([])
                sprites = self.convertCharToObject(levelMap[i][j], (i,j))
                gridItems[i][j] = sprites
        self.setInitialPosition(gridItems)
        return gridItems

    def convertCharToObject(self, char, pos): #Used to generate a grid from a map, takes in characters and returns an object associated with that character
        if char == "x":
            return [Wall(pos, self.tileSize)]
        elif char == "D":
            return [Diamond(pos, self.tileSize)]
        elif char == "T":
            return [Tile(pos, self.tileSize)]
        elif char == "C":
            return [Tile(pos, self.tileSize), Crate(pos, self.tileSize)]
        elif char == "P":
            return [Tile(pos, self.tileSize),WarehouseKeeper(pos, self.tileSize)]

    def setInitialPosition(self, spriteList): #Sets initial positions for new sprites added from a map
        gridItems = spriteList
        for row in gridItems:
            for col in row:
                for sprite in col:
                    coords = sprite.getOriginalCoordinates()
                    sprite.reset(self.getPosition(coords))

    def addItem(self, item): #Adds a single item
        self.removeItem(item) #Removes item first before adding to a grid square
        coords = item.getCoordinates()
        self.gridItems[coords[0]][coords[1]].append(item)
        item.setPosition(self.gridPositions[coords[0]][coords[1]])

    def removeItem(self, item): #Removes a single item, usually used when re-adding another item so there aren't two copies in the grid
        items = self.gridItems
        for j in range(0,self.rows):
            for i in range(0,self.cols):
                if item in items[j][i]:
                    self.gridItems[j][i].remove(item) #Removes item from 'grid'

    def crateMoving(self): #Checks if any of the crates are moving
        crates = self.getCrates()
        for crate in crates:
            if crate.getMoving():
                return True
        else:
            return False

    def reset(self): #Resets a grid back to its original state
        crates = self.getCrates()
        player = self.getPlayer()
        if crates != []:
            for crate in crates:
                self.removeItem(crate)
                coords = crate.getOriginalCoordinates()
                crate.reset(self.gridPositions[coords[0]][coords[1]])
                crate.toggleActive(False)
                self.addItem(crate)
        if player != None:
            self.removeItem(player)
            playerCoords = player.getOriginalCoordinates()
            player.reset(self.gridPositions[playerCoords[0]][playerCoords[1]])
            self.addItem(player)

    def restart(self):
        self.reset()

#SPRITE BASE
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

#SPRITES
class WarehouseKeeper(MovableSprite):
    """Represents player in the game"""

    def __init__(self, coordinates = (0,0), tileSize = (80,80), imagePath = "Assets/player.png"):
        MovableSprite.__init__(self, coordinates, tileSize, imagePath)

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

class Wall(SpriteBase):
    """Walls that will be placed around level. Player or crates will not be able to pass through."""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize)
        self.surface = None

class Tile(SpriteBase):
    """Base class for grid squares"""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize,"Assets/Tile.png")

class Diamond(SpriteBase):
    """Star square where player must push blocks on to"""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize,"Assets/Diamond.png")

game = Game()



