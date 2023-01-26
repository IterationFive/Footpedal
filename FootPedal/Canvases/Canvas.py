'''
Created on Jan 24, 2023

@author: Cather Steincamp
                
'''
from curses.textpad import rectangle, Textbox
import Canvases as cv

class Canvas(object):
    '''
    
    A Canvas object provides tools for working with a section or the entirity of a curses window.
    
    The contructor takes the following parameters.  all but the first are optional.  
    
            cursewin
                the actual curses window or screen object
            
            margins
                there are three ways to define margins.  
                
                    margins=int
                        This value will be applied to all four sides.
                        
                    margins=(int vertical,int horizontal)
                        specifies the vertical (top/bottom) and 
                        horizontal (left/right) margins
                        
                    margins=( (int top,int bottom), (int left, int right) )
                        specifies the margins individually
                        
                        It is not actually necessary to specify both 
                        vertical and horizontal individually;
                        "margins=( (2,4), 5)" will result in the
                        top margin being set to 2, the bottom margin
                        to 4, and both left and right will be set 
                        to five.
            
            border
            
                there are four ways to define a border.  Well, five,
                if you count "False".
                
                    True
                        draws a lined box
        
                    string
                        if the string is a single character, that character 
                        will be use for all sides and corners.
                        
                        if the string is three or eight characters, the 
                        characters of that string will be treated as 
                        if they were a list (see below).
                    
                    list
                        if you provide a list (or string) of three characters,
                        then the first character will be used for the top and 
                        bottom, the second character for the left and right 
                        sides.  Example: '-|O'
                        
                        if you provide a list (or string) of eight characters,
                        then they will be used to draw the borders in this order:
                        
                            left, right, top, bottom, top left, top right, bottom left, bottom right 
                
                Using a border will increase the margin on all sides by one.
                
                
            parent
                if this canvas is contained within another canvas,
                that canvas object should be provided here.
                
                if a parent is not supplied, the canvas will assume
                that it is in control of the entire cursewin
                window, and the remaining parameters will be ignored. 
                
                
            size
                tuple (height, width)
                
                the area within the window that this object
                is dedicated to.  this object will not attempt 
                to display text outside of this area.
                
                if a value is not specified, then it will be
                retrieved from cursewin.
                
            home 
                tuple (x,y)
                
                the cursewin coordinates of the upper left hand corner
                of the area handled by this object
                
        
        Properties:
        
            cursewin, margin, border, parent
                the objects and values provided to the constructor
            
            yOuter, xOuter 
                The actual dimensions of the area of the canvas
                for windows, this will be equal to the size of the window
            yHome, xHome
                The curses window coordinate of the upper left hand corner
                of the canvas
            ySize, xSize
                The available area after accounting for windows and padding
            yOffset, xOffset
                The curses coordinates of the upper left hand corner
                of the available area
                
                
            slot
                a dictionary for use by the slot functionality
                
        General Methods:
        
            Canvas.getActualSize()
                returns a tuple of (yOuter,xOuter)
                
            Canvas.getAvailableSize()
                returns a tuple of (ySize, xSize)
                
            Canvas.determineAvailableArea()
            
                uses yHome, xHome, yOuter, xOuter, margin, and border properties
                to calculate ySize, xSize, yOffset, and xOffset
                
            Canvas.drawBorder()
            
                if border is not False, draws the border as configured,
                using cursewin.box(), cursewin.border(), curses.textpad.rectangle(), 
                or by simply writing the provided characters to the screen.
                
                automatically refreshes the screen.
        
            Canvas.offset( y, x )
            
                Translates the local coordinates-- which refer to the available
                area of the screen-- into the coordinates used by curses.
                
                Unless otherwise specified, all methods below run the 
                coordinates through this method, either directly 
                or by calling Canvas.write().
                
            Canvas.moveCursor( y, x )

                Moves the cursor to the specified coordinates within
                the available area
                
            Canvas.refresh( flag=True )
            
                calls cursewin.refresh() so long as flag is true.
                
                It should be noted that any methods that have a "refresh"
                parameter pass that parameter to this function.
            
            
                
        Write Methods:
        
            Canvas.write( y, x, text, refresh=False )
            
                writes the text at the specified coordinates and, if 
                refresh is True, refreshes the window.              
                                
                Additionally, Canvas.write() makes sure that the text is not 
                written outside the available area, either by truncating the text
                or not writing it at all.
                
                If: 
                    the y coordinate is less than zero
                    the y coordinate is equal to or greater than self.ySize
                    the x coordinate is equal to or greater than self.xSize
                    the x coordinate is less than zero by an amount
                        more than the length of the text 
                    
                then no attempt will be made to write the text.
                
                If the x coordinate is less than zero by an amount less than
                the length of the text, the text will be trimmed from the left
                and x will be adusted to zero.
                
                If the x coordinate is otherwise acceptable, but the text 
                would extend outside the allowed area, then the text
                will be trimmed from the right. 
                
            Canvas.writeRight(y, text, x=None, refresh=False)
            
                Aligns the text to the right edge of the screen,
                or if an x-coordinate is given, the text will be 
                positioned so that the last character will be
                at that coordinate.
                
            Canvas.writeCenter(y, text, midpoint=None, refresh=False)
                Centers the text on the given line.
                If a midpoint is specified, the text will be centered
                along that coordinate instead.
                
            Canvas.writeHere(text, refresh=False)
                Writes the text at the current cursor position.
        
    '''


    def __init__(self, cursewin, margin=0, border=False, parent=None, size=(None,None), home=(None,None)):
        '''
        Constructor
        '''
        
        self.cursewin=cursewin 
        self.margin=margin 
        self.border=border
        self.parent=parent
        
        if parent is None:
            
            self.yOuter, self.xOuter = cursewin.getmaxyx()
            self.ySize, self.xSize = self.yOuter, self.xOuter
            self.yHome, self.xHome = 0,0
            self.yOffset, self.xOffset = 0,0
            
        else:
            
            if size[0] is None or size[1] is None:
        
                yNow, xNow = cursewin.getmaxyx()
                
                if size[0] is None:
                    size[0] = yNow 
                if size[1] is None:
                    size[1] = xNow 
            
            self.yOuter, self.xOuter = size
            self.ySize, self.xSize = size
            self.yOffset, self.xOffset = home
            self.yHome, self.xHome = home
    
        
        
    def getActualSize(self):
        return self.yOuter, self.xOuter
    
    def getAvailableSize(self):
        return self.ySize, self.xSize    
    
    def determineAvailableArea(self):
        
        self.yOffset=self.yHome
        self.xOffset=self.xHome
        
        if self.border != False:
            border = 1
        else:
            border = 0
        
        if type( self.margin ) == int:
            self.yOffset += self.margin + border
            self.xOffset += self.margin + border
            self.ySize -= ( self.margin + border ) * 2
            self.xSize -= ( self.margin + border ) * 2
            
        elif type( self.margin ) == tuple:
            
            if type( self.margin[0] ) == tuple :
                self.yOffset = self.margin[0][0] + border
                self.ySize -= self.margin[0][0] + self.margin[0][1] + ( border * 2 )
            elif type( self.margin[0] ) == int:
                self.yOffset = self.margin[0] + border
                self.ySize -= ( self.margin[0] + border ) * 2 
            
            if type( self.margin[1] ) == tuple :
                self.xOffset = self.margin[1][0] + border
                self.xSize -= self.margin[1][0] + self.margin[1][1] + ( border * 2 )
            elif type( self.margin[1] ) == int:
                self.xOffset = self.margin[1] + border
                self.xSize -= ( self.margin[1] + border ) * 2 
            
    def drawBorder(self):
        if self.border != False:
            
            if self.parent is None:
                
                # this canvas is the entire window, so we can use
                # the functionality of cursewin
                
                if self.border == True:
                    self.cursewin.box()
                elif type( self.border ) == str and len( self.border ) == 1:
                    self.cursewin.border( *self.border*8 )
                elif type( self.border ) in [list,str] and len( self.border ) == 3:
                    self.cursewin.border( [*self.border[0] * 2 + self.border[1] * 2 + self.border[2] * 4] )
                elif type( self.border ) in [list,str] and len( self.border ) == 8:
                    self.cursewin.border( *self.border )
                # else: value for border is messed up, no border will be drawn
                
            else:
                # this is a secondary canvas
                
                if self.border == True:
                    rectangle( self.cursewin, self.yHome, self.xHome, self.yHome + self.yOuter - 1, self.xHome + self.xOuter - 2)
                    
                else:
                    if type( self.border ) == str and len( self.border ) == 1:
                        self.border = self.border*8
                    
                    if type( self.border ) == str and len( self.border ) == 3:
                        self.border = self.border[0] * 2 + self.border[1] * 2 + self.border[2] * 4
                        
                    if type( self.border ) in [list,str] and len( self.border ) == 8:
                        # do it the hard way
                        
                        top = self.border[0]
                        bottom = self.border[1]
                        left = self.border[2]
                        right = self.border[3]
                        topleft = self.border[4]
                        topright = self.border[5]
                        bottomleft= self.border[6]
                        bottomright =self.border[7]                        
                        
                        self.cursewin.addstr( self.yHome, self.xHome + 1, top * ( self.xOuter - 2 ) ) #top
                        self.cursewin.addstr( self.yHome + self.yOuter - 1, self.xHome + 1, bottom * ( self.xOuter - 2 ) ) # bottom
                        
                        for i in range( 1, self.ySize - 1 ):
                            self.cursewin.addstr( self.yHome + i, self.xHome, left ) #left
                            self.cursewin.addstr( self.yHome + i, self.xHome + self.xOuter - 1, right ) #right
                    
                        self.cursewin.addstr( self.yHome, self.xHome, topleft ) #top left
                        self.cursewin.addstr( self.yHome, self.xHome + self.xOuter - 1, topright ) #top right
                        self.cursewin.addstr( self.yHome + self.yOuter - 1, self.xHome, bottomleft ) #botom left
                        self.cursewin.insch( self.yHome + self.yOuter - 1, self.xHome + self.xOuter - 1, bottomright ) # bottom right
                        
                    # else: value for border is messed up, no border will be drawn
            self.refresh()
            
    def refresh(self,flag=True):
        if flag:
            self.cursewin.refresh()
                    
    def offset(self,y,x):
        return self.yOffset + y, self.xOffset + x
    
    def moveCursor(self,y,x):
        self.cursewin.move( *self.offset(y, x) )
            
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
            
            self.cursewin.addstr( *self.offset(y,x), text )
    
            self.refresh( refresh )
        
    def writeRight(self, y, text, x=None, refresh=False):
        
        text = str( text )
        
        if x is None:
            x = self.xSize - 1
        
        start = x - len(text) - 1

        self.write( y,start,text,refresh )
        
                
    def writeCenter(self, y, text, refresh=False, midpoint=None):
        
        text = str( text )
        
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
    