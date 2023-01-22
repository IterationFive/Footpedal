'''
Created on Jan 5, 2023

@author: Cather Steincamp
'''

import curses
from curses.textpad import Textbox
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
            This setting can be changed with setEcho()
        cursor
            determines wheter the cursor blinks on screen, and keeps track
            of that state in .cursorState
    
    The following "methods" are really just pointers to the screen object's methods:
    
        .nodelay
        .getch
        .refresh
        .write (points to window.addstr)
        
    The following methods control the behavior of the window itself.
    
        .setSize( y,x )
            sets the size of the window, and keeps track of the values
            for access in sizeY and sizeX
            
        .setEcho( bool )
            disables or enables keyboard echo on the screen.
            tracks state in .echo
            
        .setCursor( bool )
            disables or re-enables the blinking cursor. 
            tracks state in .cursorState
            
        .close()
            ends the curses session
            
        .reopen()
            restores the curses session.
        
    The following methods are provided to assist with text placement.
    
        .writeNow()
            .write(), but with automatic refresh
        .writeCentered( y, text, refresh, midpoint )
            puts the text on line y, centered.
            if midpoint is provided and not None,
            the text will be centered on that point.
            if refresh is True, screen will refresh immediately.
            
    Additionally, one can create 'slots', which are preset locations
    with a specified length and alignment.  
    
        .setSlot(name, y, x, width)
            name
                string, if not unique will override pre-existing values.
            y
                the line where the slot exists.
            x
                the leftmost point of the slot
            width
                the maximum number of characters the slot will display
            alignment
                uses the special variables from CursedUtils.  default is cu.LEFT
                
        .slotWrite(name,text,refresh,forceAlign)
            name
                the predefined slot name.  If the slot does not exist, this 
                method will do nothing.
            text
                the text to be displayed in the slot
            refresh
                defaults to False
                if True, screen will refresh after writing the text.
            forceAlign
                defaults to False
                a special variable from CursedUtils; overrides the predefined
                alignment this time.  (does not change the defined alignment)
                
            Displays the provided text in the slot and stores it for retrieval
            using .slotGet()            
            
            If the length of the text exceeds the width of the slot, the text
            will be truncated, although the full value will be stored.
            
        .slotBlank(name, refresh)
            name
                the predefined slot name.  If the slot does not exist, this
                method will do nothing.
            refresh
                defaults to False
                if True te screen will refresh automatically.
                
        .slotGet(name)
            returns the value stored in the slot named.
            if slot does not exist, will return None.
            
    This class also provides two methods for inputing a block of text
    uses curses' Textbox functionality.
    
        .lineInput( y, x, length, prefill)
            y,x
                the starting position of the textbox
            length
                the total number of characters of the textbox
            prefill
                defaults to blank
                if provided, will be the default value of the textbox
                
            puts a text input box at the screen at the specified 
            coordinates and width.  returns the text entered by the user,
            stripped of leading/trailing spaces.
            
            Once text is entered, the textbox and its contents will
            disappear.
            
        .slotInput( slot )
            uses the contents and location of the slot for the textbox.
            
            once text is entered, the slot will be updated with the 
            provided text and the screen will update automatically.
    
    '''

    def __init__(self, height=None, width=None, echo=False, cursor=False):
        '''
        Constructor
        '''
        
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
            
    def writeNow(self, *args, **kwargs):
        self.window.addstr( *args, **kwargs )
        self.refresh()
        
    def writeCentered(self, y, text:str, refresh=False, midpoint=None):
        if midpoint is None:
            self.write( y, int( ( self.sizeX - len(text) ) / 2 ), text )
        else:
            self.write( y, midpoint - int( len(text) / 2  ), text )
        if refresh:
            self.window.refresh()
    
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
        
        i = Textbox( inputline )
        i.edit()
        
        r = i.gather().strip()
        
        self.window.touchwin()
        if self.screen.cursorState == False:        
            curses.curs_set(0)
        self.refresh()
        
        return r 
    
    def setSlot(self, name, y, x, width, alignment=cu.LEFT):
        self.slot[name] = { 'y':y,'x':x,'w':width,'a':alignment,'c':'' }
        
    def slotGet(self, slot):
        if slot not in self.slot:
            return None
        else:
            return self.slot[slot]['c'] 
        
    def slotBlank(self, slot, refresh=False ):
        self.window.addstr( self.slot[slot]['y'], self.slot[slot]['x'], ' ' * self.slot[slot]['w'] )
        if refresh:
            self.window.refresh()
        
    def slotWrite(self, slot, text, refresh=False, forceAlign=False):
        
        if slot in self.slot:
            self.slotBlank(slot)
            slot = self.slot[slot]
            slot['c'] = text
            
            if len(text) > slot['w']:
                text = text[:slot['w']]                
            
            x = slot['x']
            
            if forceAlign != False:
                a = forceAlign
            else:
                a = slot['a']
            
            blanks = slot['w'] - len( text )
            
            if a == cu.RIGHT:
                x += blanks
            if a == cu.CENTER and blanks > 0:
                x += int( blanks / 2 )
                
            self.write( slot['y'], x, text )
            
            if refresh:
                self.window.refresh()
            
    def slotInput(self, slot ):
        r = self.lineInput( self.slot[slot]['y'], self.slot[slot]['x'], self.slot[slot]['w'], self.slot[slot]['c'])
        self.slotWrite( slot, r, True )
        return r           
            
        