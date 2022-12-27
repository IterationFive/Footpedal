'''
Created on Dec 5, 2022

@author: Cather Steincamp
'''
import curses
from curses.textpad import Textbox

class ScreenWrapper( object ):
    
    def __init__(self, y=None, x=None):
        
        self.subwindow = {}
        self.config = {}
        self.mainScreen = self
        self.cursorState = True
        self.offsetY = 0
        self.offsetX = 0
        self.slots = {}
        
        self.window = curses.initscr()
        curses.noecho()
        
        if y != None:
            self.setSize( y, x )
        else:             
            self.sizeY, self.sizeX = self.window.getmaxyx()
            
        self.setup()
        
    def enforceSize(self):
        y, x = self.window.getmaxyx()
        if self.sizeY != y or self.sizeX != x:
            self.setSize( self.sizeY, self.sizeX)
        
        self.refresh()
        
    def setup(self):
        ''' for child classes '''
        
    def setPosition(self, y, x ):
        self.window.move( y, x )
    
    def refresh(self):
        self.window.refresh()
        
    def write(self, *args, refresh=False, **kwargs ):
        self.window.addstr( *args, **kwargs )
        if refresh:
            self.refresh()
            
    def writeNow(self, *args, **kwargs):
        self.write( *args, refresh=True, **kwargs )
        
    def setCursorOn(self, state=True):
        if state == True:
            curses.curs_set(1)
            self.mainScreen.cursorState = True
            
        else: 
            curses.curs_set(0)
            self.mainScreen.cursorState = False
    
    def nap(self, ms):
        curses.napms( ms )
        
    def setSize(self, y, x): 
        self.sizeY = y
        self.sizeX = x
        
        curses.resize_term( y, x )
        
    def close(self):
        curses.endwin()
        
    def reopen(self):
        self.window.refresh()
        
        if self.sizeY != None :
            curses.resize_term( self.sizeY, self.sizeX )
        
    def setSlot(self, name, y, x, z, value='', refresh=False, blank=' '):
        self.slots[name] = [ y, x, z, value ]
        self.slotWrite( name, value, refresh, blank )
        
    def slotWrite(self, name, string, refresh=False, blank=' ' ):
        
        if type( string ) != str:
            string = str( string )
        
        if len( string ) > self.slots[name][2]:
            string = string[:self.slots[name][2]]
        
        if len( self.slots[name][3] ) > len(string):
            pad = ( len( self.slots[name][3] ) - len(string) ) * blank
        else:
            pad = ''
        
        self.slots[name][3] = string    
        self.window.addstr( self.slots[name][0], self.slots[name][1], string + pad)
        

        if refresh:
            self.window.refresh()
    
    def slotWriteNow(self, slot, string, blank=' ' ):
        self.slotWrite( slot, string, True, blank )
        
    def slotBlank(self, slot, refresh=False, blank=' ' ):
        self.window.addstr( self.slots[slot][0], self.slots[slot][1], blank * self.slots[slot][2] )
        if refresh:
            self.window.refresh()
        
    def addWindow(self, name, windowObject ):
        self.subwindow[name] = windowObject
        return windowObject
        
    def getWindow(self, name ):
        if name in self.subwindow:
            return self.subwindow[name]
        else:
            return False 
    
    def lineInput(self, y, x, length, prefill='' ):
        '''
            It is important to note that this should only be executed on the active window,
            otherwise things could get... messy.
        '''
        y += self.offsetY
        x += self.offsetX
        
        if self.mainScreen.cursorState == False:        
            curses.curs_set(1)
            
        inputline = curses.newwin( 1, length, y, x )
        inputline.addstr( 0,0, str(prefill))
        
        i = Textbox( inputline )
        i.edit()
        
        r = i.gather().strip()
        
        self.window.touchwin()
        if self.mainScreen.cursorState == False:        
            curses.curs_set(0)
        self.refresh()
        
        return r 
    
    def slotInput(self, slot ):
        r = self.lineInput( self.slots[slot][0], self.slots[slot][1], self.slots[slot][2], self.slots[slot][3])
        self.slotWriteNow( slot, r )
        return r

