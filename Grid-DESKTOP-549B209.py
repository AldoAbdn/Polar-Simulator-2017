class Grid(object):
    """Will hold grid positions for drawn grid, and hold what objects are in each grid square"""

    def __init__(self):
        #8X5 Grid. Will store position of CENTER of grid squares
        self.gridPositions = [[0,1,2,3,4,5,6,7],#Row 0
                            [0,1,2,3,4,5,6,7],#Row 1
                            [0,1,2,3,4,5,6,7],#Row 2
                            [0,1,2,3,4,5,6,7],#Row 3
                            [0,1,2,3,4,5,6,7]]#Row 4
        self.populateGridPositions() #Populates Grid with coordinates

        #Grid that will hold items
        self.gridItems = [[[],[],[],[],[],[],[],[]], #Row 0
                          [[],[],[],[],[],[],[],[]], #Row 1
                          [[],[],[],[],[],[],[],[]], #Row 2
                          [[],[],[],[],[],[],[],[]], #Row 3
                          [[],[],[],[],[],[],[],[]]] #Row 4

    #Getters
    def getGridPositions(self):
        return self.gridPostions

    def getGridItems(self):
        return self.gridItems

    def getPosition(self, coor):
        return self.gridPositions[coor[0]][coor[1]]

    def getItems(self, row, col):
        return self.gridItems[row][col]

    #Setters
    def setGridPositions(self,Value):
        self.gridPositions = Value

    def setGridItems(self, value):
        self.gridItems = value

    def setPos(self, row, col, value):
        self.gridPostions[row][col] = value

    def setItems(self, row, col, value):
        self.gridItems[row][col] = value

    #String
    def toString(self):
        return isinstance.__class__.__name__ + ": Grid " + str(self.Grid)

    #Special
    def populateGridPositions(self):
        startX = 40 #Starting Center value for first square
        startY = 40 #Starting Center value for first Square
        for j in range(0,5): #Loops through each row
            startX=40
            if j != 0:
                startY+=80 #Gap between each center
            for i in range(0,8): #Goes through each position in row
                if i != 0:
                    startX+=80 #Gap between each center
                self.gridPositions[j][i] = (startX,startY)

    def addItem(self, coords, item):
        self.removeItem(item) #Removes item first before adding to a grid square
        self.gridItems[coords[0]][coords[1]].append(item)
        item.setPosition(self.gridPositions[coords[0]][coords[1]])

    def addItemsBySpriteManager(self, spriteManager):
        sprites = spriteManager.getSpirtes()
        for i in range(0, len(sprites)):
            temp = sprites[i]
            coordinates = temp.getCoordinates()
            self.gridItems[coordinates[0]][coordinates[1]].append(temp)
            temp.setPosition(self.gridPositions[coordinates[0]][coordinates[1]]

    def removeItem(self, item):
        rows = len(self.gridItems)
        cols = len(self.gridItems[0])
        items = self.gridItems
        for j in range(0,rows):
            for i in range(0,cols):
                if item in items[j][i]:
                    self.gridItems[j][i].remove(item)

    def reset(self): #Resets a grid back to its original state
        self.__init__()



                    
                    




                



