'''
Created on Jan 26, 2023

@author: Cather Steincamp
'''

import Canvases as cv
import curses
from lib.Dictionary import Dictionary

class DynamicCanvas(cv.Canvas):
    '''
    DynamicCanvas extends Canvas by adding the awareness of the potential of other canvases 
    on the window or contained within itself, and the ability to communicate with them, as 
    well as more advanced interactions with the window.
    
    
    DynamicCanvas adds the following parameters to the constructor:
        parent
            The DynamicCanvas (if any) on which this DynamicCanvas is displayed.
            If there is no parent, this will be considered the main canvas.
        yAlign,xAlign
            How automatically generated content (if any) is positioned within the 
            available area.
        spacing
            the number of spaces between automatically managed 
            canvases
        orientation
            cv.HORIZONTAL or cv.VERTICAL
            the orientation by which managed canvases are aligned
    
    DynamicCanvas adds the follwing properties:
    
        parent 
        yAlign, xAlign
        spacing
        orientation
            provide by constructor
        mainCanvas
            The DynamicCanvas object that manages the window or screen.
        cvEnv
            A shared dictionary.  Is created by the mainCanvas and passed to all 
            canvases within it.
        _allowUpdates
            (mainCanvas only)
            boolean.  This can be checked by automatically updating things to see if 
            it's safe to proceed.  For example, if one is working in a textbox and 
            another canvas updates the screen, it causes the cursor to move out of the
            textbox (which is still otherwise working normally).
        canvases
            Canvases contained in, and managed by, this DynamicCanvas.
            Note that this refers to Canvases and any any object with that
            class as parent.
            
    DynamicCanvas overrides the following methods:
        
        DynamicCanvas.getMinimumSize()   
            if size is hardcoded, returns that size if not, polls the canvases within 
            it and determines the minimum height and width.
        DynamicCanvas.write()
            if mainCanvas, calls Canvas.write()
            if not, runs text through Canvas.writeCheck(), then passes the results to 
            the self.parent.write().  This ensures all offset are provided and 
            prevents a misconfigured Canvas from reaching outside the area
            of the canvas that contain it.

        DynamicCanvas.rectangle(), DynamicCanvas.textrectangle()
            if mainCanvas, calls Canvas.rectangle or Canvas.textrectangle.
            if not, verifies that the rectangle is within its boundaries,
            offsets the coordinates, and passes the command to the
            parent.
            
    
            
    DynamicCanvas adds the following methods:
    
        DynamicCanvas.allowUpdates(state=True)
            boolean
            sets _allowUpdates to state
            
        DynamicCanvas.canUpdate()
            returns _allowUpdates
            
        DynamicCanvas.layout()
            while empty in this class, it allows child classes to automate the
            addition of subcanvases.  
            
            Use of this class is not required; Canvases can be added through
            external command; in fact, this command can be used to exactly that
            to its subcanvases.
            
            Additionally, this 
            
    
    
    '''


    def __init__(self, cursewin, parent=None, margin=0, border=False, size=(None, None), home=(0, 0),
                 yAlign=cv.TOP, xAlign=cv.LEFT, spacing=0, orientation=cv.VERTICAL):
        cv.Canvas.__init__(self, cursewin, margin=margin, border=border, size=size, home=home)
        
        self.parent = parent
        self.yAlign = yAlign
        self.xAlign = xAlign
        self.spacing = spacing
        self.orientation = orientation
        
        if parent is None:
            
            # this is the main canvas; it will have a shared dictionary 
            # for use by all canvases on the screen.
            
            self.cvEnv ={}
            self._allowUpdates = True
            self.mainCanvas = self
        else:
            self.cvEnv = parent.cvEnv
            self.mainCanvas = parent.mainCanvas
            
        self.canvases = []            
            
        self.layout()
            
    def allowUpdates(self, state=True):
        self.mainCanvas._allowUpdates = state

    def canUpdate(self):
        return self.mainCanvas._allowUpdates
        
    def getMinimumSize(self):
                
        if self.yOuter > 0: 
            minY= self.yOuter
        else:
            minY = 0
               
        if self.xOuter > 0: 
            minX = self.xOuter
        else:
            minX = 0
        
        if self.yOuter < 0 or self.xOuter < 0 : # cv.AUTO and cv.MAX are negatives
            
            for canvas in self.canvases:
                cY, cX = canvas.getMinimumSize()
                
                if self.yOuter < 0:
                    if self.orientation == cv.VERTICAL:
                        minX += cX
                        if cY > minY: 
                            minY = cY
                    else:
                        minY += cY
                        if cX > minX:
                            minX = cX
                
                if self.xOuter < 0:
                    if self.orientation == cv.VERTICAL:
                        minY += cY
                        if cX > minX: 
                            minY = cX
                    else:
                        minX += cX
                        if cY > minY:
                            minY = cY
                        
                
        if self.xOuter < 0 and self.spacing > 0:
            # AUTO may end up zero
            minX + ( ( len( self.canvases ) - 1 ) * self.spacing )
                
        return minY, minX 
    
    def write(self, y, x, text, refresh=False):
                
        if self.parent is None:
            cv.Canvas.write(self, y, x, text, refresh)
        else:   
            y, x, text = self.writeCheck(y, x, text)
            if y != False:
                self.parent.write( y, x, text, refresh )
            
    def rectangle(self, y, x, endY, endX, refresh=False, offset=True):
        if self.parent is None:
            cv.Canvas.rectangle(self, y, x, endY, endX, refresh=refresh, offset=offset)
        else:
            if self.inBounds(y, x, endY, endX, offset):
                self.parent.rectangle( y, x, endY, endX, refresh=refresh, offset=offset )
            
    def textrectangle(self, config, y, x, endY, endX, refresh=False, offset=True):
        if self.parent is None:
            cv.Canvas.textrectangle(self, config, y, x, endY, endX, refresh=refresh, offset=offset)
        else:
            if self.inBounds(y, x, endY, endX, offset):
                self.parent.textrectangle( config, y, x, endY, endX, refresh=refresh, offset=offset)
    
                
    def hline(self, y, x, length, refresh=False):
        if self.parent is None:
            cv.Canvas.hline(self, y, x, length, refresh=refresh)
        else:
            y,x,length = self.hlineCheck(y, x, length)
            if y!= False:
                self.parent.hline( y, x, length, refresh )
                
    def vline(self, y, x, length, refresh=False):
        if self.parent is None:
            cv.Canvas.vline(self, y, x, length, refresh=refresh)
        else:
            y,x,length = self.vlineCheck(y, x, length)
            if y!= False:
                self.parent.vline( y, x, length, refresh )
        
    
    
    
    
    