import math
from cell import Cell

def printPretty(grid):
    for line in grid:
        print(line)

def makeZeroGrid(sz):
    grid = []
    for i in range(0,sz):
        grid.append([])
    for line in grid:
        for i in range(sz):
            line.append(0)
    return grid

def rotateGrid(grid):
    sz = len(grid)
    vlines = makeZeroGrid(sz)
    for i in range(sz):
        for j in range(sz):
            vlines[i][j] = grid[j][i]
    return vlines

def calcBounds(n,base):
    mult = math.floor(n/base)
    lower_bound = base * mult
    upper_bound = lower_bound + 2
    return (lower_bound,upper_bound)

def getVLine(grid,ind):
    vline = []
    for line in grid:
        vline.append(line[ind])
    return vline

def GetMaxIndexes(grid):
    maxval = 0
    maxind = []
    for ind,line in enumerate(grid):
        val = max(line)
        if val >= maxval:
            if val > maxval:
                maxind = []
                maxval = val
            maxind.append((ind,line.index(val)))
    return(maxind)

def GetLeastCouldBeCellsIndexes(cells):
    minlen = 5
    minind = []
    for i,line in enumerate(cells):
        for j,cell in enumerate(line):
            if cell.picked: continue
            if len(cell.couldbe) <= minlen:
                if len(cell.couldbe) < minlen:
                    minind = []
                    minlen = len(cell.couldbe)
                minind.append((i,j))
    return(minind)




def allDifferent1D(lst):
    return len(lst) == len(set(lst))

def CheckForBroken(cells):
    for line in cells:
        linevals = []
        for cell in line:
            if len(cell.couldbe) == 0:
                #print("reason1")
                return True
            if cell.picked: linevals.append(cell.val)
        for cell in line:
            if not cell.picked:
                encounter = 0
                for i,possibility in enumerate(cell.couldbe):
                    if possibility in linevals:
                        encounter += 1
                if encounter == i+1:
                    #print("reason2")
                    return True

        if not allDifferent1D(linevals): 
            #print("reason3")
            return True

    for i in range(len(cells)):
        vline = getVLine(cells,i)
        linevals = []
        for cell in vline:
            if cell.picked: linevals.append(cell.val)
        if not allDifferent1D(linevals): 
            #print("reason4")
            return True
    return False

def CheckCompletion(cells):
    for line in cells:
        for cell in line:
            if not cell.val: return False
    if CheckForBroken(cells): return False
    return True

    

# grid = [[1,9,8,7,6,5,4,3,2]
#        ,[2,1,9,8,7,6,5,4,3]
#        ,[3,2,1,9,8,7,6,5,4]
#        ,[4,3,2,1,9,8,7,6,5]
#        ,[5,4,3,2,1,9,8,7,6]
#        ,[6,5,4,3,2,1,9,8,7]
#        ,[7,6,5,4,3,2,1,9,8]
#        ,[8,7,6,5,4,3,2,1,9]
#        ,[9,8,7,6,5,4,3,2,1]]

# cells = []
# for i,line in enumerate(grid):
#     newline = []
#     for j,member in enumerate(line):
#         newline.append(Cell(i,j,member))
#     cells.append(newline)

# cells[8][2].couldbe = [8]

# print(CheckCompletion(cells))
# print(CheckForBroken(cells))
    