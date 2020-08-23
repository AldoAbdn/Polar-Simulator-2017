import pygame
from SpriteBase import SpriteBase

class Wall(SpriteBase):
    """Walls that will be placed around level. Player or crates will not be able to pass through."""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize)
        self.surface = None


        




