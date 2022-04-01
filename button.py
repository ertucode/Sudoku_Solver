from vars import *
from dataclasses import dataclass, field
from typing import Callable
import pygame


def PrintTextatCenter(win,text_rect,text,font=NUMBERFONT,fontsize=15,color=(0,0,0)):
    xc = text_rect[0] + text_rect[2]/2
    yc = text_rect[1] + text_rect[3]/2
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    text_rect = text_sur.get_rect(center=(xc, yc))
    win.blit(text_sur,text_rect)

@dataclass
class Button:
    rect: tuple
    text: str
    color: str
    func: Callable
    args: list = field(default_factory=list)
    needsCell: bool = False

    def __post_init__(self):
        self.pyRect = pygame.Rect(*self.rect)

    def draw(self,win):
        pygame.draw.rect(win,pygame.Color(self.color),self.rect,3)
        PrintTextatCenter(win,self.rect,self.text,BUTTONFONT,BUTTONFONTSIZE,BUTTONTEXTCOLOR)

    def handle_press(self,pos,cells):
        if self.pyRect.collidepoint(pos[0],pos[1]):
            if self.needsCell:
                self.args.insert(0,cells)
            cells = self.func(*self.args)
            if self.needsCell:
                del self.args[0]
            return cells
        else:
            return cells



    