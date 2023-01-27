'''
Created on Jan 24, 2023

@author: Cather Steincamp
                
'''
import curses
import Canvases as cv

class Canvas(object):
    '''    
    A Canvas object provides tools for working with a section or the entirity of a 
    curses window.  It allows you to create a border and margins.
    
    A canvas object works with a set of coordinates that correspond to the 
    available area, after border and margins, that are automatically translated
    by its tools into coordinates on the main screen.
    
    It is possible to have more than one Canvas on a window, but they have 
    no awareness of each other and any overlap will slap back and forth between
    updates.  Also, when a canvas refreshes, it does so by refreshing the screen.
    
    Attempts to define a canvas that exceeds the bounds of the window will throw
    a ValueError exception.
    
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
                
            size
                tuple (height, width)
                
                the area within the window that this object
                is dedicated to.  this object will not attempt 
                to display text outside of this area.
                
                if a value is not specified, then it will be
                retrieved from cursewin.
                
                Note:  the sizes CV.AUTO and CV.MAX are here,
                allowing an object of this class to be resized by
                another canvas, but this class provides no 
                functionality to adjust the position of contents
                based on the size of the Canvas; if the canvas
                is scaled to 
                
            home 
                tuple (x,y)
                
                the cursewin coordinates of the upper left hand corner
                of the area handled by this object
                
                defaults to 0,0                
        
        Properties:
        
            cursewin, margin, border
                the objects and values provided to the constructor            
            yOuter, xOuter 
                The outer dimensions of the canvas
            yHome, xHome
                The curses window coordinate of the upper left hand corner
                of the canvas
            ySize, xSize
                The dimension of the usable area of the canvas 
                after accounting for border and margins
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
                
            Canvas.getMinimumSize()
                returns a tuple of (yOuter,xOuter)
                (this ensures compatibiliy with DynamicCanvas)                    
                
            Canvas.layout()
                This method is empty in this class, but it can be used
                in child classes to put slots on the screen.  It is run 
                once, automatically, by the constructor.  No data should
                be written to the screen
                
            Canvas.build()
                Draws the border
                calculates ySize, xSize, yOffset, and xOffset
                fills any defined slots with their contents
                runs Canvas.Paint()
                
            Canvas.paint()
                Another empty method for use in child classes.  This
                is run every time the screen is cleared.                  
        
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
                
            Canvas.rectangle( y, x, endY, endX, refresh = False, offset = True )
            
                Draws a rectangle at the the given start and end coordinates.
                
                This is just basically a slight modification of curses.textpad.rectangle,
                which has an annoying bug where it will not allow you to draw a box that
                shares a lower-right-hand-corner with the screen.  
                
                By default, will pass the coordinates through Canvas.offset().
                You can use cursewin coordinates if offset is False.  Mainly
                this was to let me use this function to draw the border.
                
            Cancas.textRectangle(config, y, x, endY, endX, refresh=False, offset=True)
            
                Draws a rectangle at the the given start and end coordinates using 
                the string or list provided as config, using the same configuration as
                the border parameter of the constructor (which, in fact, ends up getting
                passed to this method.).
                
        Write Methods:
        
            Canvas.write( y, x, text, refresh=False )
            
                writes the text at the specified coordinates and, if 
                refresh is True, refreshes the window.              
                                
                Additionally, Canvas.write() makes sure that the text is not 
                written outside the available area, either by truncating the text
                or not writing it at all.
                
                If the text falls completely beyond the available area,                    
                then no attempt will be made to write the text.
                
                If the text extends to the left of the available area,
                it will be truncated from the left to fit.
                
                If the text extends to the right of the available area,
                it will be truncated from the right to fit.
                
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
                
        Slot Methods:
        
            The slot functionality allows you to designate a
            part of a given line as a place where text will be 
            written/updated, and stores the contents of the slot.
        
            Canvas.setSlot(name, y, x, width, contents='', alignment=cv.LEFT, refresh=False):
                creates the slot.  erases the area it occupies.
                
                alignment determines how the text is aligned within 
                the slot, and can be cv.LEFT, cv.RIGHT, cv.CENTER, or cv.CENTRE.
                this is a default; a different alignment can be 
                specified when the slot is written to.
                
            Canvas.setSlotContents( slot, data )
                Sets the data in the slot without actually
                writing it to the screen.  
                
            Canvas.slotBlank(slot,refresh=False)
                Erases the area occupied by the slot and sets the
                contents to None.
                
            Canvas.slotWrite(slot, data=None, refresh=False, forceAlign=False):
                
                This method stores the data in the slot, and 
                then writes it to the screen.  id Data is not 
                provided, the existing contents will be written 
                to the screen.  
                
                If forceAlign is provided, it will overwrite the 
                default alignment for the slot.
                
                If the string is larger than the width of the 
                slot, it will be trimmed from the right.  
                
                It should be noted that the data provided is stored
                *as provided*.  If it is a string that exceeds the 
                bounds of the slot, the full string will be stored.
                If the data is not a string-- for example, an integer
                or float-- it will be stored as provided, and then
                converted to a string for writing.

            Canvas.slotGet(slot)            
                Retrieves the data stored in a slot as it was 
                originally provided before converstion to 
                string and/or truncation.
                
            Canvas.slotMove(self, slot, y, x, refresh=False):
                Relocates the slot to the given coordinates.  
                Both the original slot area and the new slot 
                area will be blanked, then the new slot area
                will be filled with contents of the slot.
                
                Note that if alignment was overriden when 
                the data was written, that override will
                not be applied when the slot is moved.
        
    '''

    def __init__(self, cursewin, margin=0, border=False, size=(None,None), home=(0,0)):
        '''
        Constructor
        '''
        
        self.cursewin=cursewin 
        self.margin=margin 
        self.border=border
        
        size = list( size )
        
        yNow, xNow = cursewin.getmaxyx()
            
        if size[0] is None:
            size[0] = yNow 
        if size[1] is None:
            size[1] = xNow
            
        if home[0] < 0 or home[0] >= yNow or home[1] < 0 or home[1] >= xNow:
            raise ValueError('Specified coordinates for home are outside window bounds.' )
        
        if home[0] + size[0] >= yNow or home[1] +size[1] >= xNow:
            raise ValueError('Section defined is outside window bounds.' )            
        
        self.yOuter, self.xOuter = size
        self.ySize, self.xSize = size
        self.yOffset, self.xOffset = home
        self.yHome, self.xHome = home

        self.slot = {}
        
        self.layout()
        
        
    def getActualSize(self):
        return self.yOuter, self.xOuter
        
    def getMinimumSize(self):
        return self.yOuter, self.xOuter
    
    def getAvailableSize(self):
        return self.ySize, self.xSize    
    
    def build(self, clearScreen=True):
        
        if clearScreen:
            self.cursewin.clear()
        
        if self.border != False:
            
            if self.border == True:
                self.rectangle( self.yHome, self.xHome, self.yHome + self.yOuter - 1, self.xHome + self.xOuter - 1, True, False)
            else:
                self.textrectangle(self.border, self.yHome, self.xHome, self.yOuter - 1, self.xHome + self.xOuter - 1, True, False)

            self.refresh()
            border = 1
        else:
            border = 0
        
        self.yOffset=self.yHome
        self.xOffset=self.xHome
        
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
                self.xSize -= ( self.margin[1] + border ) * 

        for slot in self.slots:
            self.slotWrite(slot)

        self.paint()
                
                
    def layout(self):
        pass
    
    def paint(self):
        pass
                
    def inBounds(self,y,x,endY,endX, offset = True ):

        inBounds = True
        
        if x < 0 or y < 0:
            inBounds = False
            
        elif offset:
            if endY >= self.ySize or endX >= self.xSize:
                inBounds = False
        else:
            if endY >= self.yOffset + self.yOuter or endX >= self.xOffset + self.xOuter:
                inBounds = False
                
        return inBounds
                    
                    
    def rectangle(self, y,x, endY, endX, refresh=False, offset = True):
            
        if self.inBounds(y, x, endY, endX, offset):
            self.cursewin.vline(y+1, x, curses.ACS_VLINE, endY - y - 1)                      
            self.cursewin.hline(y, x+1, curses.ACS_HLINE, endX - x - 1)                      
            self.cursewin.hline(endY, x+1, curses.ACS_HLINE, endX - x - 1)                      
            self.cursewin.vline(y+1, endX, curses.ACS_VLINE, endY - y - 1)                      
            self.cursewin.addch(y, x, curses.ACS_ULCORNER)                                    
            self.cursewin.addch(y, endX, curses.ACS_URCORNER)                                         
            self.cursewin.addch(endY, x, curses.ACS_LLCORNER)                              
            self.cursewin.insch(endY, endX, curses.ACS_LRCORNER) 
            self.refresh(refresh)
                
    def textrectangle(self, config, y, x, endY, endX, refresh=False, offset=True):
                
        if self.inBounds(y, x, endY, endX, offset):
            
            if offset:
                y += self.yOffset
                x += self.xOffset
            
            if type( config ) == str and len( config ) == 1:
                config = config*8
                    
            if type( config ) in [list,str] and len( config ) == 3:
                config = config[0] * 2 + config[1] * 2 + config[2] * 4
                    
            if type( config ) in [list,str] and len( config ) == 8:
                # we have a valid list or string and can proceed
                
                self.cursewin.insch( y, x, config[4] )
                self.cursewin.insch( y, endX, config[5] )
                self.cursewin.insch( endY, x, config[6] )
                self.cursewin.insch( endY, endX, config[7] )
                                
                self.cursewin.addstr( y, x+1, config[0]*( ( endX - x ) - 1 ) )
                self.cursewin.addstr( endY, x+1, config[1]*( ( endX - x ) -1 ) )
                
                for i in range( y+1, endY ):
                    self.cursewin.insch( i, 0, config[2] )
                    self.cursewin.insch( i, endX, config[3])

                self.refresh( refresh )  
            
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
        
    def setSlot(self, name, y, x, width, contents='', alignment=cv.LEFT,refresh=False):
        self.slot[name] = { 'y':y,'x':x,'width':width,'alignment':alignment, 'contents':contents }
        self.slotBlank(name, refresh )
        
    def setSlotContents(self, slot, data):
        if slot in self.slots:
            slot[slot] = data
        
    def slotGet(self, slot):
        if slot not in self.slot:
            return False
        else:
            return self.slot[slot]['contents'] 
        
    def slotBlank(self, slot, refresh=False):
        self.window.addstr( self.slot[slot]['y'], self.slot[slot]['x'], ' ' * self.slot[slot]['width'] )
        self.slot[slot]['contents']  = None
        self.window.refresh(refresh)

    def slotMove(self, slot, y, x, refresh=False):
        
        contents = self.slot[slot]['contents']
        self.slotBlank(slot, False )
        self.setSlot(slot, self.slot[slot]['y'],self.slot[slot]['x'],self.slot[slot]['width'],self.slot[slot]['alignment'])
        self.slotWrite( slot, contents, refresh )
        
    def slotWrite(self, slot, data=None, refresh=False, forceAlign=False):
        
        if slot in self.slot:
            self.slotBlank(slot)
            slot = self.slot[slot]
            
            if data is None:
                data = slot['contents']
            else:
                slot['contents'] = data
            
            text = str( data )
            
            if len(text) > slot['width']:
                text = text[:slot['width']]                
            
            x = slot['x']
            
            if forceAlign != False:
                a = forceAlign
            else:
                a = slot['alignment']
                        
            if a == cv.RIGHT:
                x += slot['width'] -1
                self.writeRight( slot['y'], text, x, refresh )
            if a == cv.CENTER:
                midpoint = slot['x'] + ( int( slot['width'] /2 ) - 1 )
                self.writeCenter(slot['y'], text, refresh, midpoint)
            else:
                self.write( slot['y'], x, text, refresh )