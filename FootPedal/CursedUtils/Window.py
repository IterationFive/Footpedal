'''
Created on Dec 8, 2022

@author: Cather Steincamp
'''

import curses
from CursedUtils import Screen

class Window(Screen):
    '''
    This class encapsulates and manageds a curses window object, and provides 
    the additional functionality the CursedUtils.Screen object, making them
    functionally almost interchangeable.
    
    The constructor has the following arguments:
    
        parent
            Either the CursedUtils.Screen object or another object of this class.
        height
            height of the window in lines
            optional, defaults to the size of the parent window
        width
            width of the the window in characters
            optional, defaults to the size of the parent window
        y,x
            The position of this window within the parent window
            
            
    The move( y, x ) method has been added.
    
    The following methods provide the window version of the functionality
    of the methods from the screen.
    
    setSize()
    reopen()
    close()
    
    It should be noted that close() automatically reopens the parent window and refreshes it.
    
    
    '''
    
    def __init__(self, parent:Screen, height=None, width=None, y=0, x=0 ):        
        
        if height is None:
            height = parent.sizeY
        if width is None:
            width = parent.sizeX
        
        self.parent = parent            # can be the CursedUtils.Screen or another object of this class
        self.stdscr = parent.stdscr     # will always point to the curses screen object
        self.screen = parent.screen     # will always be the CursedUtils.Screen
        self.sizeY = height
        self.sizeX = width
        self.offsetY = y + parent.offsetY
        self.offsetX = x + parent.offsetX
        self.locY = y
        self.locX = x
        
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