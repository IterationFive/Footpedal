'''
Created on Dec 8, 2022

@author: Cather Steincamp
'''

import curses
from CursedUtils import ScreenHandler

class WindowHandler(ScreenHandler):
    '''
    classdocs
    '''
    
    def __init__(self, parent:ScreenHandler, height, width, y, x ):
        
        self.parent = parent
        self.config = parent.config
        self.mainScreen = parent.mainScreen
        self.sizeY = height
        self.sizeX = width
        self.offsetY = y + parent.offsetY
        self.offsetX = x + parent.offsetX
        
        self.slot = {}
        
        self.window = curses.newwin( height, width, y, x )
        
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