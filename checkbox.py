from vars import *
from dataclasses import dataclass, field
from typing import Callable
import pygame

def PrintTextatLeft(win,text_rect,text,font=NUMBERFONT,fontsize=15,color=(0,0,0)):
    xc = text_rect[0] + text_rect[2]/2
    yc = text_rect[1] + text_rect[3]/2
    myfont = pygame.font.SysFont(font,fontsize)
    text_sur = myfont.render(text,True,color)
    text_rect = text_sur.get_rect(center=(xc, yc))
    text_rect = text_rect.move((text_rect[2] - text_rect[0])*0.05,0)
    win.blit(text_sur,text_rect)

@dataclass
class CheckBox:
    rect: tuple
    text: str

    def __post_init__(self):
        self.active = False
        self.pyRect = pygame.Rect(*self.rect)
        self.circleCenter = list(self.pyRect.midright)
        self.circleCenter[0] -= self.pyRect.width * 0.1
        self.circleCenter = tuple(self.circleCenter)

    def draw(self,win):
        pygame.draw.rect(win,"black",self.rect,3)
        PrintTextatLeft(win,self.rect,self.text,BUTTONFONT,BUTTONFONTSIZE,BUTTONTEXTCOLOR)
        pygame.draw.circle(win,"black",self.circleCenter,5,2)
        if self.active:
            pygame.draw.circle(win,"red",self.circleCenter,5)

    def handle_press(self,pos,cells):
        if self.pyRect.collidepoint(pos[0],pos[1]):
            self.toggleActive()
        return cells

    def toggleActive(self):
        if self.active:
            self.active = False
        else:
            self.active = True