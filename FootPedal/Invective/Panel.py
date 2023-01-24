'''
Created on Jan 23, 2023

@author: Cather Steincamp
'''
import curses
from Invective.Window import Window


class Panel(Window):
    '''
    This class adds and encapsulates a Panel to manage the window.
    '''
    
    def __init__(self, parent:Screen, height=None, width=None, y=0, x=0, border=False, padding=False, subwindow=False):
        Window.__init__(self, parent, height=height, width=width, y=y, x=x, border=border, padding=padding, subwindow=subwindow)
        self.panel = curses.panel.new_panel( self.cursewin )
        
    def close(self):
        self.panel.hide()
        
    def reopen(self):
        self.panel.show()
        self.panel.top()
        
    def move(self, y, x ):
        self.panel.move(y,x)
        
    

        