
from vars import *
from copy import deepcopy
from sudoku_functions import *
from cell import Cell
import time
import sys

import pygame

## 
# Evil
# grid = [[5,0,0,4,0,1,0,6,0]
#        ,[0,0,1,0,9,0,0,0,0]
#        ,[0,0,0,0,8,0,4,0,0]
#        ,[6,0,0,0,0,0,0,0,2]
#        ,[0,0,5,3,0,7,9,0,0]
#        ,[0,0,0,0,1,0,0,0,0]
#        ,[0,0,7,5,0,4,3,0,0]
#        ,[0,0,0,8,0,0,0,0,0]
#        ,[0,3,0,0,0,0,0,9,0]]

# # Easy
# grid = [[0,9,4,0,0,0,6,0,0]
#        ,[0,5,3,9,8,6,0,4,1]
#        ,[0,8,2,0,1,3,9,7,5]
#        ,[0,0,0,1,6,0,3,0,7]
#        ,[9,0,0,0,0,2,0,0,0]
#        ,[0,3,0,0,0,0,0,1,2]
#        ,[5,6,0,0,4,1,0,0,0]
#        ,[0,1,0,0,0,0,7,0,0]
#        ,[3,0,0,2,9,0,0,5,0]]

# # Semi-hard
# grid = [[8,6,5,3,0,0,0,0,0]
#        ,[0,0,0,0,0,5,0,2,1]
#        ,[0,0,9,0,0,0,0,0,0]
#        ,[0,0,0,0,7,0,1,3,0]
#        ,[4,0,0,1,0,0,0,0,0]
#        ,[9,0,0,0,0,6,0,0,0]
#        ,[0,9,0,0,0,0,0,5,0]
#        ,[5,0,0,4,0,0,2,6,0]
#        ,[0,0,3,0,6,0,0,0,0]]

# New Evil
grid = [[0,0,8,0,0,0,0,0,0]
       ,[5,0,9,0,1,0,0,0,7]
       ,[0,0,0,0,0,6,0,1,0]
       ,[2,0,5,0,0,4,9,0,0]
       ,[0,8,0,0,5,0,0,0,0]
       ,[0,6,0,0,0,0,0,0,2]
       ,[0,0,0,3,0,0,4,0,0]
       ,[0,2,0,0,0,0,0,0,0]
       ,[7,0,1,0,6,0,0,0,9]]

# New Evil2
grid = [[0,7,0,0,0,4,0,0,0]
       ,[3,0,0,7,0,0,0,9,5]
       ,[0,0,0,0,0,0,0,0,2]
       ,[0,0,0,9,0,0,2,0,0]
       ,[1,0,0,0,0,0,4,0,0]
       ,[0,0,5,0,0,6,0,1,9]
       ,[0,0,6,0,8,0,0,0,0]
       ,[5,0,0,4,0,0,0,3,7]
       ,[0,0,0,0,0,0,1,0,0]]

pygame.init()


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")




def backgroundPicker(val):
    match val:
        case 1:
            return "snow"
        case 2:
            return "dark violet"
        case 3:
            return "navy"
        case 4:
            return "orchid1"
        case 5:
            return "pink1"
        case 6:
            return "coral"
        case 7:
            return "sky blue"
        case 8:
            return "Slategray1"
        case 9:
            return "gold2"




def createCellsFromGrid(grid):
    cells = []
    for i,line in enumerate(grid):
        newline = []
        for j,member in enumerate(line):
            newline.append(Cell(i,j,member))
        cells.append(newline)
    return cells

print("-------------------------------------------------------")
cells = createCellsFromGrid(grid)

def changeCouldbees(cells):
    for i,line in enumerate(cells):
        for j,curcel in enumerate(line):
            if not curcel.picked:
                ## Removing vals on lines according to picked's
                for horcell in line:
                    if horcell.picked:
                        curcel.removeOrInsertCouldbeWithValue(horcell.val)
                verline = getVLine(cells,j)
                if not curcel.picked:
                    for vercell in verline:
                        if vercell.picked:
                            curcel.removeOrInsertCouldbeWithValue(vercell.val)

def check3x3(curcel,cells,i,j):
    base = 3
    hor_bounds = calcBounds(i,base)
    ver_bounds = calcBounds(j,base)
    cellsin3x3 = []
    for k in range (hor_bounds[0],hor_bounds[1]+1):
        for l in range (ver_bounds[0],ver_bounds[1]+1):
            cellsin3x3.append(cells[k][l])


    for possibility in curcel.couldbe:
        possibility_exists_in_grid = False

        if curcel.picked:   return

        for cell in cellsin3x3:
            if (cell.loc == curcel.loc): continue
            if cell.picked:
                if possibility == cell.val:
                    possibility_exists_in_grid = True
            else:
                if possibility in cell.couldbe:
                    possibility_exists_in_grid = True

        if not possibility_exists_in_grid:
            curcel.assignVal(possibility)
            return

def checkForSame_couldbe_InLines(curcel,cells,i,j):
    if len(curcel.couldbe) <= 3:
        hline = cells[i]
        vline = getVLine(cells,j)
        for possibility in curcel.couldbe:
            possibility_exists = False
            for ncell in hline:
                if not ncell.picked:
                    if possibility in ncell.couldbe:
                        possibility_exists = True
            if not possibility_exists:
                curcel.val = possibility
                curcel.picked = True
                return
            
            possibility_exists = False
            for mcell in vline:
                if not mcell.picked:
                    if possibility in mcell.couldbe:
                        possibility_exists = True
            if not possibility_exists:
                curcel.val = possibility
                curcel.picked = True
                return

run = True

def drawGrid(win):
    
    for i in range(10):
        LINEWIDTH = 1
        if i % 3 == 0: LINEWIDTH = 3
        pygame.draw.line(win,LINECOLOR,(0,i * CELLWIDTH),(WIDTH,i * CELLWIDTH),LINEWIDTH)
        pygame.draw.line(win,LINECOLOR,(i * CELLWIDTH,0),(i * CELLWIDTH,WIDTH),LINEWIDTH)

def draw(win,cells):
    win.fill(WINDOW_BACKGROUND)
    drawGrid(win)

    for line in cells:
        for cell in line:
            cell.draw(win)

    pygame.display.update()

def solve(cells):
    c = 0
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        c += 1
        compare_cell = deepcopy(cells)
        # change couldbees
        changeCouldbees(cells)
        draw(win,cells)
        # couldbe sıfırlanınca insert val
        for i,line in enumerate(cells):
            for j,curcel in enumerate(line):
                curcel = cells[i][j]
                ## Assigning if could be length is 1
                curcel.assignValIfLen1()
                if not curcel.picked:
                    checkForSame_couldbe_InLines(curcel,cells,i,j)
                if not curcel.picked:
                    check3x3(curcel,cells,i,j)
        if compare_cell == cells: return(cells)


cells = solve(cells)



def trial_and_error(cells):
    global run 
    ### Recording the initialstate
    initialstate = deepcopy(cells)

    # time.sleep(1)
    ### If completed just return
    if (CheckCompletion(cells)): 
        print("Completed")
        print("return 1")
        return cells

    while run:
        if (CheckCompletion(cells)): break
        leastIndexes = GetLeastCouldBeCellsIndexes(cells)
        
        # Get leastIndexes
        indexes = leastIndexes[0]
        curcel = cells[indexes[0]][indexes[1]]
        ######################################################################
        #### Check if there are no possibilities that gives NotBroken > if there are > return initial state
        ## If there are actual possibilites store them

        possibilities = []
        cell_possibilities = []
        locations = []
        for possibility in curcel.couldbe:
            modifycells = deepcopy(cells)
            modifycell = modifycells[indexes[0]][indexes[1]]
            modifycell.assignVal(possibility)
            modifycells = solve(modifycells)

            if (CheckForBroken(modifycells)): 
                pass
            elif (CheckCompletion(modifycells)): 
                print("Solved!!")
                cells = modifycells
                break
            else:
                newcopy = deepcopy(modifycells)
                possibilities.append(possibility)
                locations.append(modifycell.loc)
                cell_possibilities.append(newcopy)


     
        if (CheckCompletion(cells)): break
        

        if (len(cell_possibilities)) == 0:
            return initialstate
        ########################################################################

        ########################################################################
        ## If there are more than one possibility, recursively search

        for i,cell_possibility in enumerate(cell_possibilities):
        ### Cannot be broken or the solution
            latest_replica = deepcopy(cell_possibility)
            latest_replica = trial_and_error(latest_replica)
            if (CheckCompletion(latest_replica)):
                cells = latest_replica
                break
            else:
                cells = latest_replica

        if (len(cell_possibilities)) == 0:
            return initialstate
    return cells

if not CheckCompletion(cells):
    cells = trial_and_error(cells)

print("-------------DONE------------------")
print(f"Completed = {CheckCompletion(cells)}")
print(f"Broken = {CheckForBroken(cells)}")

