from vars import *
from dataclasses import dataclass
import pygame


def PrintTextatCenter(win,text_rect,text,font=NUMBERFONT,fontsize=15,color=(0,0,0)):
    xc = text_rect[0] + text_rect[2]/2
    yc = text_rect[1] + text_rect[3]/2
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    text_rect = text_sur.get_rect(center=(xc, yc))
    win.blit(text_sur,text_rect)


@dataclass(unsafe_hash = True)
class Cell:
    locx: int
    locy: int
    val: int


    def __post_init__(self):
        self.active = False
        self.color = "black"
        self.fontsize = 15
        if self.val:
            self.picked = True
            self.couldbe = [self.val]
        else:
            self.picked = False
            self.couldbe = [1,2,3,4,5,6,7,8,9]
        self.loc = (self.locx,self.locy)
        self.pyRect = pygame.Rect(self.locx * CELLWIDTH, self.locy * CELLWIDTH, CELLWIDTH, CELLWIDTH)

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

    def draw(self,win):
        if self.picked:
            text_rect = (self.locx * CELLWIDTH, self.locy * CELLWIDTH , CELLWIDTH , CELLWIDTH)
            PrintTextatCenter(win,text_rect,str(self.val),font=NUMBERFONT,fontsize=self.fontsize,color=self.color)
        else:
            pass


    def assignValIfLen1(self):
        # Assign the could be if its the only one
        if self.picked: return
        if len(self.couldbe) == 1:
            self.val = self.couldbe[0]
            self.picked = True

    def handle_press(self,pos):
        if self.pyRect.collidepoint(pos[0],pos[1]):
            self.active = True
        else:
            self.active = False

    def assignVal(self,val):
        if val == 0: return
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
            return f"|{len(self.couldbe)}"
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