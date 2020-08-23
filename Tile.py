import pygame
from SpriteBase import SpriteBase

class Tile(SpriteBase):
    """Base class for grid squares"""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize,"Assets/Tile.png")

class Diamond(SpriteBase):
    """Star square where player must push blocks on to"""
    def __init__(self, coordinates=(0,0), tileSize=(80,80)):
        SpriteBase.__init__(self, coordinates,tileSize,"Assets/Diamond.png")
        

##TESTING
#def test():
#    print "Tile test"
#    display = pygame.display.set_mode((640,460))
#    sprite = Tile()
#    sprite.setPosition((40,40))
#    print sprite.rect.width, sprite.rect.height, sprite.rect.center
#    while True:
#        display.blit(sprite.getSurface(), sprite.getRect())
#        events = pygame.event.get()
#        for event in events:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#        pygame.display.update()
#test()




