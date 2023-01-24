'''
Created on Jan 23, 2023

@author: Cather Steincamp
'''

import curses

class Screen(object):
    '''
        This class creates and encapsulates a curses screen, and provides
        basic management and informational tools.  
        
        The constructor has six optional parameters:
        
            height
                the height of the window, in lines
                default is None, meaning the height will not change
            width
                The width of the screen, in chracters.
                default is None, meaning the height will not change
            echo
                boolean.  Determines whether keystrokes will appear on screen
                default is False
            showCursor
                boolean.  Determines whether the cursor is initially visible.  
                default is False
            border
                draws a border around the window/screen
                there are four ways to do this.
                
                    If you set this to True(), the border will be a lined box.
                    
                    If you provide a single character, that character will be used
                    for all four sides and all four corners
                    
                    If you provide a list of eight characters, those will be used to
                    draw the box (see below).
                    
                    If you provide a string of eight characters, it will be converted
                    to a list, and used to draw the box (see below).
                
                The eight positions in the string or list correspond to the sides in this
                order:
                    
                    left side
                    right side
                    top 
                    bottom
                    upper left corner
                    upper right corner
                    bottom left corner
                    
                additionally, padding will automatically be applied to prevent accidental 
                overwriting of the border.  
                
            padding
                allows you to specify margins.  
                Again, there are several ways to do this.  
                
                If you provide a single number, that number of spaces will be applied to all four borders.
                
                If you provide a tuple of (y,x), the first value will set equal padding on the top
                and bottom, and the second value will set equal padding for left and right.
                
                alternately, you can provide one or both of the values above as a tuple:
                    ( (top, bottom), (left, right) ) 
                    ( x, (left, right ) 
                    
                see write() for more details
                
                
        Each object has the following properties:
        
            stdscr
                this is the curses screen object.  
            cursewin
                this is also the curses screen object.
                the redundancy is so that methods provided in this class
                do not have to be rewritten in the Window class, 
                which will actually have the curses window in 
                this spot.
            screen
                A pointer back to this object.
                Again, this will be useful in the window class, 
                where the window "parent" may be another window,
                but this value will always point to the main screen object
            ySize,xSize
                the available dimensions of the screen
            height, width
                the actual dimensions of the screen
            echo
                boolean, reflects whether keystrokes are currently echoing
                note that this property does not exist in Window objects,
                which instead paint back to the parent screen.
            cursorState
                boolean, reflects whether the cursor is visible
                note that this property does not exist in Window objects,
                which instead paint back to the parent screen.
            xOffset, yOffset
                Used here to adjust for border and/or padding.
            slot
                a dictionary to be used by the slot functionality.
                
        The following methods have been provided for screen management:
        
            (Note: any method with a parameter of refresh will automatically
            refresh the screen upon completion if that value is provided as True.)
        
            setup()
            
                Does nothing, but allows for child classes to have startup 
                instructions without messing with the constructor.
                
            refresh(refresh)
                defaults to True
                This executes cursewin.refresh() if "refresh" is True 
                
            setSize(y, x, refresh)
                Used to resize the screen object.  also calls .defineBorder() and .addPadding() 

            showCursor( state )
                boolean, defaults to True
                determines if the cursor is on or off
                notes change in .cursorstate
                
            setEcho( echo )
                boolean, defaults to True
                enables or disables keyboard echo
                notes the change in .echo
                
            close()
                shuts down the curses screen and returns the user to the terminal
                
            reopen()
                repoens the terminal screen and, if necessary, readjusts the size.
                
        
        The following methods are simply wrappers for window or curses functionality.
        
            keypad( flag )
            nodelay( flag )
            getch()
            napms( ms)
            
        The following methods are used for displaying text on the screen.  
        
        In all cases, the y and x coordinates are adjusted using yOffset and xOffset,
        so they refer not to the position on the window, but to the position within the
        usable area of the window.  For example, a 30x120 window with a border and 
        padding of 1 on all four sides has a usuable area of 26x116, and 0,0 
        refers to the top left corner of the usable area-- which in this case is 
        actually 2,2 on the window itself.
        
        Additionally, none of these functions will allow text to be written outside 
        this usable are. Text that falls partially within the usable area will be 
        truncated.
        
            write(y,x,text,refresh)
                writes the provided text at the given coordinates            
        
            setCursor(y,x)
                moves the cursor to the given coordinates
                
            writeHere( text, refresh )
                writes the text at the current location.
                
            writeRight( y, text, x, refresh )
                aligns text to the right on the specified line, using x as the ending point.  
                if x is not provided, uses the rightmost edge of the screen
                
            writeCenter(y, text, midpoint, refresh )
                centers the text along the provided midpoint or, if no midpoint is
                provided, the center most point of the screen.
        
        
    '''


    def __init__(self, height=None, width=None, echo=False, showCursor=False, border=False, padding=False):
        '''
        Constructor
        '''
        
        self.stdscr = curses.initscr()
        self.cursewin = self.stdscr
        self.screen = self
        
        self.setEcho(echo)
        self.showCursor(showCursor)
        
        self.border = border
        self.padding = padding
        
        self.yOffset = 0
        self.xOffset = 0
        
        self.slot = {}
        
        yNow, xNow = self.cursewin.getmaxyx()
        
        if height is None and width is None:
            self.ySize, self.xSize = yNow, xNow
            self.height, self.width = yNow, xNow
        elif height is None: 
            self.setSize( yNow, width )
        elif width is None:
            self.setSize( height, xNow )
        else:
            self.setSize( height, width )
            
        self.setup()
            
            
    def defineBorder(self):
        
        if self.border != False:
            if self.border == True:
                self.cursewin.box()
            elif type( self.border ) == list and len( self.border ) == 8 :
                self.cursewin.self.border( *self.border )
            elif type( self.border ) == str:
                if len( self.border ) == 1:
                    self.cursewin.self.border( *self.border*8 )
                elif len( self.border ) == 8:
                    self.cursewin.self.border( *self.border )
            
    def addPadding(self):
        
        if self.border != False:
            border = 1
        else:
            border = 0
        
        if type( self.padding ) == int:
            self.yOffset += self.padding + border
            self.xOffset += self.padding + border
            self.ySize -= ( self.padding + border ) * 2
            self.xSize -= ( self.padding + border ) * 2
            
        elif type( self.padding ) == tuple:
            
            if type( self.padding[0] ) == tuple :
                self.yOffset = self.padding[0][0] + border
                self.ySize -= self.padding[0][0] + self.padding[0][1] + ( border * 2 )
            elif type( self.padding[0] ) == int:
                self.yOffset = self.padding[0] + border
                self.ySize -= ( self.padding[0] + border ) * 2 
            
            if type( self.padding[1] ) == tuple :
                self.xOffset = self.padding[1][0] + border
                self.xSize -= self.padding[1][0] + self.padding[1][1] + ( border * 2 )
            elif type( self.padding[1] ) == int:
                self.xOffset = self.padding[1] + border
                self.xSize -= ( self.padding[1] + border ) * 2 
                
                
        
    def setup(self):
        '''
            for use in child classes.  
        '''
        
    def setSize(self, y, x, clear=False): 
        self.ySize = y
        self.xSize = x
        self.height = y 
        self.width = x
        
        curses.resize_term( y, x )
        
        if clear:
            self.cursewin.clear()
        
        self.defineBorder()
        self.addPadding()
        
    def refresh(self, refresh=True):
        if refresh:
            self.window.refresh()
        
    def napms(self, ms):
        curses.napms( ms )
        
    def keypad(self, flag):
        self.cursewin.keypad( flag )
        
    def nodelay(self, flag ):
        self.cursewin.nodelay( flag )
        
    def getch(self):
        self.cursewin.getch()
        
    def setEcho(self, echo=True ):
        if echo == False:
            curses.noecho()
            self.screen.echo = False
        else:
            curses.echo()
            self.screen.echo = True
        
    def showCursor(self, state=True):
        if state == True:
            curses.curs_set(1)
            self.screen.cursorState = True
            
        else: 
            curses.curs_set(0)
            self.screen.cursorState = False
            
    def setCursor(self, y,x):
        self.cursewin.move(y + self.yOffset, x+self.xOffset )
        
    def close(self):
        curses.endwin()
        
    def reopen(self):
        self.window.refresh()
        
        yNow, xNow = self.cursewin.getmaxyx()
        
        if self.height != yNow or self.width != xNow :
            curses.resize_term( self.height, self.width )
            
    def write(self, y, x, text, refresh=False ):
        
        text = str( text )
            
        if x < 0 and len( text ) > 0 - x:
            # truncate from the left
            text = text[0-x:]
            x = 0
        
        if y < self.ySize and y >= 0 and x < self.xSize and x >= 0:
        # we are at least starting within the border of the screen
        
            if x + len( text ) >= self.xSize:
                # truncate from the right
                overshot = x + len(text) - self.xSize
                text = text[0:-overshot]
            
            self.cursewin.addstr( self.yOffset + y, self.xOffset + x, text )
    
            if refresh:
                self.cursewin.refresh()
                
                
        
    def writeRight(self, y, text, x=None, refresh=False):
        
        if x is None:
            x = self.xSize - 1
        
        start = x - ( len(text) - 1 )

        self.write( y,start,text,refresh )
        
                
    def writeCenter(self, y, text, refresh=False, midpoint=None):
        
        if midpoint is None:
            x = int( ( self.xSize - len(text) ) / 2 )
        else:
            x = midpoint - int( len( text ) / 2 )
            
            if len( text ) % 2 == 1:
                # restores the conventional bias of rounding
                # to the left, rather than the right
                x -= 1
            
        self.write( y,x, text, refresh )
        
    def writeHere(self, text, refresh=False):
        
        y,x = self.cursewin.getyx()
        
        y -= self.yOffset
        x -= self.xOffset
        
        self.write( y,x, text, refresh)
        
        