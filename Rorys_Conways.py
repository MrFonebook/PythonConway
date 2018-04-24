#Conway's Game of Life in Python by Rory McDougal 3/18/2017

from graphics import *
import random

#Name of window
GAME_NAME = "Conway's Game of Life"
#Color to represent age or just B&W
IN_COLOR = True
#Size of the game board in pixel width
GAME_SIZE = 500
#Size of cells in pixel width
CELL_SIZE = 10
#Choose a seed file or random fill
READ_FILE = False                   
#Provide name of seed file
FILE_NAME = 'gosper_glider_gun.txt'         
#Number of cells to offset seed file pattern from origin
FILE_OFFSET = 5
#Percentage chance that each cell will live at start
RANDOM_PERCENT = 50                 
#Time in seconds between steps
TIME_STEP = 0                       

#Color Lists
if IN_COLOR:
    COLORS = ['white','grey','violet','aqua','palegreen','lemonchiffon','lightsalmon','hotpink']
else:
    COLORS = ['white','black']

class Cell:
    #Cell constructor
    def __init__(self, x, y, size, win):
        self.age = 0
        self.agetemp = 0
        self.neighbors = 0
        self.square = Rectangle(Point(x,y), Point(x + size, y + size))
        self.square.setFill(COLORS[self.age])
        self.square.draw(win)

    def applyrules(self):
        #Dead cell with exactly 3 neighbors comes to life
        if self.age == 0 and self.neighbors == 3:
            self.agetemp += 1
        #Cell with 2 or 3 neighbors keeps living
        elif self.neighbors > 1 and self.neighbors < 4 and self.age > 0:
            self.agetemp += 1
        #All other cells die from over or under population
        else:
            self.agetemp = 0
        #Correct an age out of range of COLOR list
        if self.agetemp > len(COLORS) - 1:
            self.agetemp = len(COLORS) - 1

    def update(self):
        self.neighbors = 0
        self.age = self.agetemp
        self.square.setFill(COLORS[self.age])

class Game:
    #Game constructor
    def __init__(self, name, size, cellsize):
        self.steps = int(size / cellsize)
        self.window = GraphWin(name, size, size)
        self.window.autoflush = False
        self.cells = [[] for i in range(self.steps)]
        #Create 2-Dimensional list of cells
        for i in range(self.steps):
            for j in range(self.steps):
                self.cells[i].append(Cell(i * cellsize, j * cellsize, cellsize, self.window))
        #Populate from a file
        if READ_FILE:
            with open(FILE_NAME) as file:
                j = 0
                for line in file:
                    for i in range(len(line)):
                        if line[i] == '*':
                            self.cells[i + FILE_OFFSET][j + FILE_OFFSET].agetemp = 1
                    j += 1
        #Populate randomly
        else:
            for i in range(self.steps):
                for j in range(self.steps):
                    if random.randrange(100) < RANDOM_PERCENT:
                        self.cells[i][j].agetemp = 1
        self.cellupdate()

    def cellupdate(self):
        #Apply updates to all Cells
        for i in range(self.steps):
            for j in range(self.steps):
                self.cells[i][j].update()
        self.window.flush()

    def neighbors(self):
        #Using i and j to index through 2D list of Cells
        for i in range(self.steps):
            for j in range(self.steps):
                #Using k and l to iterate through all neighbor Cells
                for k in range(3):
                    for l in range(3):
                        #Check neighbors and exclude self
                        if self.cells[(i + (k - 1)) % self.steps][(j + (l - 1)) % self.steps].age > 0:
                            if k == 1 and l == 1:
                                self.cells[i][j].neighbors += 0
                            else:
                                self.cells[i][j].neighbors += 1
                self.cells[i][j].applyrules()
            
#main function definition
def main():
    myGame = Game(GAME_NAME, GAME_SIZE, CELL_SIZE)
    while True:
        myGame.neighbors()
        myGame.cellupdate()
        time.sleep(TIME_STEP)
#execute the main function
main()
