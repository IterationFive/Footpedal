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
                    
                additionally, padding will automatically be added to prevent accidental 
                overwriting of the border.  
            padding
                allows you to specify margins.  
                Again, there are several ways to do this.  
                
                If you provide a single number, that number of spaces will be applied to all four borders.
                
                Alternately you can provide a list or tuple of (y,x).
                
                    if y is a single value, that number of spaces will be applied to both top and bottom.
                    if y is a tuple, the first number will be applied to the top, and the second to the bottom.
                    for x, it works the same way, except the first number is left and the second is right.
                    
                see write() for more details
                
                
        Each Object has the following properties:
        
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
            echo
                boolean, reflects whether keystrokes are currently echoing
            cursorState
                boolean, reflects whether the cursor is visible
            xOffset, yOffset
                Used here to adjust for border and/or padding.
                
        The following methods have been provided:
        
            setup()
            
                Does nothing, but allows for child classes to have startup 
                instructions without messing with the constructor.
                
            refresh(refresh)
                defaults to True
                This is a wrapper for curses' 
                
            setSize(y, x, refresh)
            
                Used to resize the screen object.  A

                
            showCursor( state )
                boolean, defaults to True
                determines if the cursor is on or off
        
        
        
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
        
        # this is lazy, fix this
        
        if width is not None or height is not None:
            self.setSize( height, width )
        else:             
            self.ySize, self.xSize = self.window.getmaxyx()
            
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
        
        curses.resize_term( y, x )
        
        if clear:
            self.cursewin.clear()
        
        self.defineBorder()
        self.addPadding()
        
    def refresh(self, refresh=True):
        if refresh:
            self.window.refresh()
        
    # the following functions are just pointers to curses or window functionality.
            
    def napms(self, ms):
        curses.napms( ms )
        
    def keypad(self, val):
        self.cursewin.keypad( val )
        
    def nodelay(self, val ):
        self.cursewin.nodelay( val )
        
    def getch(self):
        self.cursewin.getch()
        
    def setEcho(self, echo ):
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
        self.cursewin.move(y,x)
        
    def close(self):
        curses.endwin()
        
    def reopen(self):
        self.window.refresh()
        
        if self.sizeY != None :
            curses.resize_term( self.sizeY, self.sizeX )
        
        