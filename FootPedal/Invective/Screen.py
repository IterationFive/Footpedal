'''
Created on Jan 23, 2023

@author: Cather Steincamp
'''

import curses
from pip._vendor.typing_extensions import Self

class Screen(object):
    '''
        This class creates and encapsulates a curses screen, and provides
        basic management and informational tools.  
    '''


    def __init__(self, height=None, width=None, echo=False, showCursor=False):
        '''
        Constructor
        '''
        
        self.stdscr = curses.initscr()
        self.cursewin = self.stdscr
        self.screen = self
        
        self.setEcho(echo)
        self.showCursor(showCursor)
        
        if width is not None or height is not None:
            self.setSize( height, width )
        else:             
            self.sizeY, self.sizeX = self.window.getmaxyx()
        
    def setSize(self, y, x): 
        self.sizeY = y
        self.sizeX = x
        
        curses.resize_term( y, x )
        
    def setEcho(self, echo ):
        if echo == False:
            curses.noecho()
            self.echo = False
        else:
            curses.echo()
            self.echo = True
        
    def showCursor(self, state=True):
        if state == True:
            curses.curs_set(1)
            self.cursorState = True
            
        else: 
            curses.curs_set(0)
            self.cursorState = False
        
    def close(self):
        curses.endwin()
        
    def reopen(self):
        self.window.refresh()
        
        if self.sizeY != None :
            curses.resize_term( self.sizeY, self.sizeX )