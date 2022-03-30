
from dataclasses import dataclass
from copy import deepcopy
import math


grid = [[5,0,0,4,0,1,0,6,0]
       ,[0,0,1,0,9,0,0,0,0]
       ,[0,0,0,0,8,0,4,0,0]
       ,[6,0,0,0,0,0,0,0,2]
       ,[0,0,5,3,0,7,9,0,0]
       ,[0,0,0,0,1,0,0,0,0]
       ,[0,0,7,5,0,4,3,0,0]
       ,[0,0,0,8,0,0,0,0,0]
       ,[0,3,0,0,0,0,0,9,0]]

# grid = [[0,9,4,0,0,0,6,0,0]
#        ,[0,5,3,9,8,6,0,4,1]
#        ,[0,8,2,0,1,3,9,7,5]
#        ,[0,0,0,1,6,0,3,0,7]
#        ,[9,0,0,0,0,2,0,0,0]
#        ,[0,3,0,0,0,0,0,1,2]
#        ,[5,6,0,0,4,1,0,0,0]
#        ,[0,1,0,0,0,0,7,0,0]
#        ,[3,0,0,2,9,0,0,5,0]]

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


@dataclass
class Cell:
    locx: int
    locy: int
    val: int


    def __post_init__(self):
        if self.val:
            self.picked = True
            self.couldbe = [self.val]
        else:
            self.picked = False
            self.couldbe = [1,2,3,4,5,6,7,8,9]
        self.loc = (self.locx,self.locy)

    def removeOrInsertCouldbeWithValue(self,val):
        # initially = deepcopy(self.couldbe)
        # inlen = len(self.couldbe)
        if self.picked: return
        # if not len(self.couldbe) > 2:
        #     print("before assignment")
        self.assignValIfLen1()
        if self.picked: return
        # after1 = deepcopy(self.couldbe)
        # aflen = len(self.couldbe)

        # If value is in couldbe: remove it 
        if val in self.couldbe:
            # before = len(self.couldbe)
            self.couldbe.remove(val)
            # after2 = deepcopy(self.couldbe)
            # If the new length is 1: assign value 
            self.assignValIfLen1()
            # if len(self.couldbe) == 0 and before == 1:
            #     pass
            #     print(f"1- {initially} -len {inlen}*** 2- {after1} -len {aflen}*** 3- {after2} *** ")

    def assignValIfLen1(self):
        # Assign the could be if its the only one
        if self.picked: return
        if len(self.couldbe) == 1:
            self.val = self.couldbe[0]
            self.picked = True

    def assignVal(self,val):
        self.val = val
        self.picked = True

    def __str__(self):
        if self.picked:
            return f".{self.val}"
        else:
            return f"|{len(self.couldbe)}"

    def __repr__(self):
        if self.picked:
            return f".{self.val}"
        else:
            # return f"|{len(self.couldbe)}"
            return f"{self.couldbe}"

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'val' and value == 0:
            pass
            # print("val changed to zero")
        try:
            if self.loc == (0,8):
                pass
        except:
            pass
        try:
            if not self.picked:
                pass
                # print(f"not picked but assigned: {self.val}, pos : {self.loc}")
                # print(f"{self.couldbe}")
        except:
            pass

    def __eq__(self,other):
        return self.loc == other.loc and self.val == other.val and self.couldbe == other.couldbe


## creating cells
cells = []
for i,line in enumerate(grid):
    newline = []
    for j,member in enumerate(line):
        newline.append(Cell(i,j,member))
    cells.append(newline)

print("-------------------------------------------------------")
    
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

def getVLine(grid,ind):
    vline = []
    for line in grid:
        vline.append(line[ind])
    return vline

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

def calcBounds(n,base):
    mult = math.floor(n/base)
    lower_bound = base * mult
    upper_bound = lower_bound + 2
    return (lower_bound,upper_bound)

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



c = 0

while True:
    c += 1
    compare_cell = deepcopy(cells)
    # change couldbees
    changeCouldbees(cells)
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
    if compare_cell == cells:
        break

### Implement Trial and error


print(c)

import tkinter
from tkinter.font import Font

root = tkinter.Tk()
root.geometry("720x450")
frames = makeZeroGrid(9)
width = 80
height = 50
for i in range (9):
    for j in range (9):
        newfr = tkinter.LabelFrame(root)
        frames[i][j] = newfr
        newfr.place(x = width * i, y= height* j, width = width , height = height)

labels = []
for i,line in enumerate(cells):
    for j,cell in enumerate(line):
        if cell.picked:
            newlab = tkinter.Label(frames[j][i], text = cell.val,font = Font(family="Consolas",size = 25))
        else:
            newlab = tkinter.Label(frames[j][i], text = f"{cell.couldbe}",font = Font(family="Consolas",size = 5))
        newlab.grid(row = cell.locx, column = cell.locy)


first3x3 = makeZeroGrid(3)
for i in range (3):
    for j in range (3):
        first3x3[i][j] = cells[i][j]



poss = makeZeroGrid(3)
for i,line in enumerate(first3x3):
    for j,cell in enumerate(line):  
        if cell.picked:
            poss[i][j] = cell.val
        else:
            poss[i][j] = cell.couldbe

root.mainloop()