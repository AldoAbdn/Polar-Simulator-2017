import pygame, sys
from EventManager import EventManager
import threading

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






