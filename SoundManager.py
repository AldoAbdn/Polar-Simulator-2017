import pygame
from EventHandlers import SoundManagerEventHandlers
from EventManager import EventManager
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






