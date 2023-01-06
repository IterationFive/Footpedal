'''
Created on Jan 5, 2023

@author: Cather Steincamp
'''

import curses
import CursedUtils as cu

class Screen(object):
    '''
    This class creates and a curses screen object and provides a number of tools to 
    simplify the process of rendering text onto it.
    
    The constructor has three parameters, all optional.
        height
            The height of the screen, in lines.  
            default is None, meaning the screen height will not be changed
            This can be changes with setSize()
        width
            The width of the screen, in characters.  
            default is None, meaning the screen width will not be changed
            This can be changes with setSize()
        echo
            determines whether keystrokes appear on the screen.  
            defaults to False, because man, that's a recipe for disaster.
            This setting can be changed with echo()
    
    The following "methods" are really just pointers to the screen object's methods:
    
        nodelay
        getch
        refresh
        write (points to window.addstr)
    
    
    '''

    def __init__(self, height=None, width=None, echo=False, cursor=False):
        '''
        Constructor
        '''
        
        self.cursorState = True
        self.offsetY = 0
        self.offsetX = 0
        self.slot = {}
        
        
        self.window = curses.initscr()
        self.stdscr = self.window
        self.screen = self
        
        self.setEcho(echo)
        self.setCursor(cursor)
        
        if width is not None or height is not None:
            self.setSize( height, width )
        else:             
            self.sizeY, self.sizeX = self.window.getmaxyx()
            
        # rather than recode the wheel
        self.nap = curses.napms
        self.keypad = self.window.keypad
        self.nodelay = self.window.nodelay
        self.getch = self.window.getch 
        self.refresh = self.window.refresh
        self.write = self.window.addstr 
            
        self.setup()   
        
    def setup(self):
        # for the use of child classes
        pass 
        
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
        
    def setCursor(self, state=True):
        if state == True:
            curses.curs_set(1)
            self.screen.cursorState = True
            
        else: 
            curses.curs_set(0)
            self.screen.cursorState = False
        
    def close(self):
        curses.endwin()
        
    def reopen(self):
        self.window.refresh()
        
        if self.sizeY != None :
            curses.resize_term( self.sizeY, self.sizeX )
            
    def writeNow(self, *args, **kwargs):
        self.window.addstr( *args, **kwargs )
        self.refresh()
    
    def lineInput(self, y, x, length, prefill='' ):
        '''
            It is important to note that this should only be executed on the active window,
            otherwise things could get... messy.
        '''
        y += self.offsetY
        x += self.offsetX
        
        if self.screen.cursorState == False:        
            curses.curs_set(1)
            
        inputline = curses.newwin( 1, length, y, x )
        inputline.addstr( 0,0, str(prefill))
        
        i = curses.textpad.Textbox( inputline )
        i.edit()
        
        r = i.gather().strip()
        
        self.window.touchwin()
        if self.screen.cursorState == False:        
            curses.curs_set(0)
        self.refresh()
        
        return r 
    
    def setSlot(self, name, y, x, width, alignment=cu.LEFT):
        self.slot[name] = { 'y':y,'x':x,'w':width,'a':alignment,'c':'' }    
        
    def slotBlank(self, slot, refresh=False ):
        self.window.addstr( self.slot[slot]['y'], self.slot[slot]['x'], ' ' * self.slot[slot]['w'] )
        if refresh:
            self.window.refresh()
        
    def slotWrite(self, slot, text, refresh=False):
        if slot in self.slot:
            self.slotBlank(slot)
            slot = self.slot[slot]
            slot['c'] = text
            
            if len(text) > slot['w']:
                text = text[:slot['w']]                
            
            x = slot['x']
            blanks = slot['w'] - len( text )
            
            if slot['a'] == cu.RIGHT:
                x += blanks
            if slot['a'] == cu.CENTER and blanks > 0:
                x += int( blanks / 2 )
                
            self.write( slot['y'], x, text )
            
            if refresh:
                self.window.refresh()
            
    def slotInput(self, slot ):
        r = self.lineInput( self.slot[slot]['y'], self.slot[slot]['x'], self.slot[slot]['w'], self.slot[slot]['c'])
        self.slotWrite( slot, r, True )
        return r           
            
        