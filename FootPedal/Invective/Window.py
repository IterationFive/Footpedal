'''
Created on Jan 23, 2023

@author: Cather Steincamp
'''
import curses
from Invective.Screen import Screen

class Window(Screen):
    '''
        Retools Screen to work for a window as well.  
        
        Rewrites the constructor with the following parameters.  
        
            parent
                an Invective Screen object or another object of this class
            height, width
                the height and width of the window in characters
                optional, defaults to extend to the bottom right hand corner
                of the parent window
            y,x
                the position of the upper left hand corner relative to the 
                parent window
                optional, defaults to 0,0
            border, padding
                these function exactly the same as in the invective Screen object
                optional, defaults to None
            subwindow
                boolean 
                if False, then window is created with curses.newwin()
                
                if True, then window is created with parent.cursewin.subwin(),
                which shares memory and updates with the parent window.
                optional, defaults to False
                
                
        This class duplicates the following properties from Screen:
            ySize,xSize
            yOffset,xOffset
            
        The following properties are recreated
            stdscr - refers to the top-level curses screen object
            screen - refers to the top-level invective screen object
            cursewin - refers to the local curses window object
            
        The following property is added
            parent - refers to the parent invective screen or window object
                     (the parent window object can be accessed via parent.cursewin)
        
        
            
        
    
    ''' 
    def __init__(self, parent:Screen, height=None, width=None, y=0, x=0, border=False, padding=False, subwindow=False ):     
        
        if height is None:
            height = parent.sizeY - y
        if width is None:
            width = parent.sizeX - x
            
        self.parent = parent
        self.stdscr = parent.stdscr     # the curses screen object
        self.screen = parent.screen     # the Invective Screen object that encapsulates it
        
        self.sizeY = height
        self.sizeX = width
        
        self.offsetY = 0
        self.offsetX = 0
        
        if subwindow:
            self.cursewin = parent.cursewin.subwin( height, width, y, x )
        else:
            self.cursewin = curses.newwin( height, width, y, x ) 

        self.setup()
    
    def setSize(self, y, x, clear=False ):
        self.sizeY = y
        self.sizeX = x
        self.cursewin.resize( y,x )
        
        if clear:
            self.cursewin.clear()
        
        self.defineBorder()
        self.addPadding()
        
    def close(self):
        self.parent.cursewin.touchwin()
        self.parent.refresh()
        
    def reopen(self):
        self.cursewin.touchwin()
        self.refresh()