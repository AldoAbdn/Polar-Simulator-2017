class SpriteManager(object):
    """Used to contain a large group of sprites and coresponding coordinates"""

    def __init__(self, sprites=[], coords=[]):
        self.sprites = sprites
        self.coords = coords
        self.matchCoordinates()

    #Getters
    def getSprites(self):
        return self.sprites

    def getCoordinates(self):
        return self.coords

    #Setters
    def setSprites(self, value):
        self.sprites = value

    def setCoordinates(self, value):
        self.coords = value

    #Special
    def setup(self, sprites, coords):
        self.sprites = sprites
        self.coords = coords
        self.matchCoordinates()

    def add(self, sprite, coords):
        self.sprites.append(sprite)
        self.coords.append(coords)
        self.matchCoordinates()

    def matchCoordinates(self):
        for i in range(0, len(self.sprites)):
            self.sprites[i].setCoordinates(self.coords[i])

    #String
    def toString(self):
        return isinstance.__class__.__name__ + ": Sprites="+self.sprites+", Coordinates="+self.coords


