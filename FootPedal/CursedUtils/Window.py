'''
Created on Dec 8, 2022

@author: Cather Steincamp
'''

import curses
from CursedUtils import Screen

class Window(Screen):
    '''
    classdocs
    '''
    
    def __init__(self, parent:Screen, height=None, width=None, y=0, x=0 ):
        
        
        if height is None:
            height = parent.sizeY
        if width is None:
            width = parent.sizeX
        
        self.parent = parent
        self.screen = parent.screen
        self.sizeY = height
        self.sizeX = width
        self.offsetY = y + parent.offsetY
        self.offsetX = x + parent.offsetX
        
        self.slot = {}
        
        self.window = curses.newwin( height, width, y, x )
        
        # rather than recode the wheel
        self.nap = curses.napms
        self.keypad = self.window.keypad
        self.nodelay = self.window.nodelay
        self.getch = self.window.getch 
        self.refresh = self.window.refresh
        self.write = self.window.addstr 
        
        self.setup()
    
    def setSize(self, y, x ):
        self.sizeY = y
        self.sizeX = x
        self.window.resize( y,x )
        
    def move(self, y, x ):
        self.locY = y
        self.locX = x
        self.window.mvwin( y, x )
        
    def close(self):
        self.parent.window.touchwin()
        self.parent.refresh()
        
    def reopen(self):
        self.window.touchwin()
        self.refresh()