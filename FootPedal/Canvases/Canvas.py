'''
Created on Jan 24, 2023

@author: Cather Steincamp
        
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
                
'''
import curses.textpad.rectangle as rectangle
import curses.textpad.Textbox as Textbox
import Canvases as can

class Canvas(object):
    '''
     classdocs
    '''


    def __init__(self, cursewin, margin=0, border=False, parent=None, size=(None,None), home=(None,None)):
        '''
        Constructor
        
        properties
            
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
            
        
            
        '''
        
        self.cursewin=cursewin 
        self.margin=margin 
        self.border=border
        self.parent=parent
        
        if parent is None:
            
            self.yOuter, self.xOuter = cursewin.getmaxxy()
            self.ySize, self.xSize = self.yOuter, self.xOuter
            self.yHome, self.xHome = 0,0
            self.yOffset, self.xOffset = 0,0
            
        else:
            
            if size[0] is None or size[1] is None:
        
                yNow, xNow = cursewin.getmaxxy()
                
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
    
    def calculateOffsets(self):
        
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
            if self.parent == False:
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
                    rectangle( self.cursewin, self.yHome, self.xHome, self.yHome + self.yOuter - 1, self.xHome + self.yOuter - 1)
                    
                else:
                    if type( self.border ) == str and len( self.border ) == 1:
                        self.border = self.border*8
                    
                    if type( self.border ) == str and len( self.border ) == 3:
                        self.border = self.border[0] * 2 + self.border[1] * 2 + self.border[2] * 4
                        
                    if type( self.border ) in [list,str] and len( self.border ) == 8:
                        # do it the hard way
                        
                        self.cursewin.addstr( self.yHome, self.xHome + 1, self.border[0] * [ self.xSize - 2 ] ) #top
                        self.cursewin.addstr( self.yHome + self.Outer - 1, self.xHome + 1, self.border[1] * [ self.xSize - 2 ] ) # bottom
                        
                        for i in range( 1, self.ySize - 1 ):
                            self.cursewin.addstr( self.yHome + i, self.xHome, self.border[2] ) #left
                            self.cursewin.addstr( self.yHome + i, self.xHome + self.xSize - 1, self.border[3] ) #right
                    
                        self.cursewin.addstr( self.yHome, self.xHome, self.border[4] ) #top left
                        self.cursewin.addstr( self.yHome, self.xHome + self.xSize - 1, self.border[5] ) #top right
                        self.cursewin.addstr( self.yHome + self.Outer - 1, self.xHome, self.border[6] ) #botom left
                        self.cursewin.addstr( self.yHome + + self.Outer - 1, self.xHome + self.xSize - 1, self.border[7] ) # bottom right
                        
                    # else: value for border is messed up, no border will be drawn
            
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
    