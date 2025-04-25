#Conway's game of life
import random, time, copy
WIDTH = 60
HEIGHT = 20

#Create a list of list for the cells
nextCells = []
for x in range(WIDTH):
    column = [] #Create new column
    for y in range(HEIGHT):
        if random.randint(0, 1) == 0:
            column.append('#') #add living cell
        else:
            column.append(' ') #add a dead cell
    nextCells.append(column)

while True:
    print('\n\n\n\n\n') #separate each cell with newlines
    currentCells = copy.deepcopy(nextCells)
    #print currentCells on the screen:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(currentCells[x][y], end='') #print # or space
        print() #print a newline at the end of each row

    #calculate the next step's cells based on current step's cells:
    for x in range(WIDTH):
        for y in range(HEIGHT):
            #get neighboring coordinates:
            # '% WIDTH' ensures leftCoord is always between 0 and WIDTH - 1
            leftCoord = (x - 1) % WIDTH
            rightCoord = (x + 1) % WIDTH
            aboveCoord = (y - 1) % HEIGHT
            belowCoord = (y + 1) % HEIGHT

            #count number of living neighbors
            numNeighbors = 0
            if currentCells[leftCoord][aboveCoord] == '#':
                numNeighbors += 1 #top left neighbor alive
            if currentCells[x][aboveCoord] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][aboveCoord] == '#':
                numNeighbors += 1
            if currentCells[leftCoord][y] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][y] == '#':
                numNeighbors += 1
            if currentCells[leftCoord][belowCoord] == '#':
                numNeighbors += 1
            if currentCells[x][belowCoord] == '#':
                numNeighbors += 1
            if currentCells[rightCoord][belowCoord] == '#':
                numNeighbors += 1

            # Set cell based on Conway's Game of Life rules:
            if currentCells[x][y] == '#' and (numNeighbors == 2 or numNeighbors == 3):
                nextCells[x][y] = '#' # Stay alive.
            elif currentCells[x][y] == ' ' and numNeighbors == 3:
                nextCells[x][y] = '#' # Become alive.
            else:
                nextCells[x][y] = ' ' # Die or stay dead.

    time.sleep(0.2) #one second pause to prevent flickering