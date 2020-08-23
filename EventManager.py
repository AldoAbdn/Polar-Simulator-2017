#EVENTS
#Between 24 and 32
#25 = game over
#26 = room over
#27 = player move
#28 = reset
#29 =
#30 = track over
import pygame, sys

#TEMPLATE
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