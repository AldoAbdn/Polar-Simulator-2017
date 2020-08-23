import pygame
from SpriteBase import MovableSprite

class WarehouseKeeper(MovableSprite):
    """Represents player in the game"""

    def __init__(self, coordinates = (0,0), tileSize = (80,80), imagePath = "Assets/player.png"):
        MovableSprite.__init__(self, coordinates, tileSize, imagePath)



#TESTING
#def test():
#    print "Warehouse Keeper Test"
#    DISPLAY = pygame.display.set_mode((640,460))
#    sprite = WarehouseKeeper()
#    sprite.setPosition((40,40))
#    print sprite.rect.width, sprite.rect.height, sprite.rect.center
#    while True:
#        DISPLAY.blit(sprite.getSurface(), sprite.getRect())
#        events = pygame.event.get()
#        for event in events:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#        pygame.display.update()
#test()


