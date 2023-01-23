'''
Created on Jan 22, 2023

@author: Cather Steincamp


These classes allow for arranging text in a curses window in a manner similar to,
but not necessarily identical to, a table.

Terminology subject to change.









'''

import CursedUtils as cu

ENTRY = 0
LINE = 1

class WindowManager(cu.Window):
    '''
    
    '''
    def __init__(self, parent:cu.Screen, height=None, width=None, y=0, x=0):
        cu.Window.__init__(self, parent, height=height, width=width, y=y, x=x)
        self.block = []
        
        # calculate parent size without depending on CursedUtils.Screen methods
        # to allow for maximum portability


class Block( object ):
    '''
        A virtual horizontal container that manages one or more cells. 
        It takes up the entire horizontal space available.
        
        
    '''
    def __init__(self, grid, height=cu.AUTO, spacing=0, xAlign=cu.CENTER ):
        '''
            grid
                 the parent grid object
            height
                int or cu.AUTO, cu.MAX
                the height of the block
            spacing 
                int or cu.AUTO, cu.MAX
                the number of horizontal spaces between each cell
                cu.MAX will put the maximum amount of space possible between each cell
                cu.AUTO will distribute the available space among both the spaces and the 
                left and right borders.
            xAlign
                if the combined width of the cells and spaces is less than the width of the 
                grid, then they will be aligned according to this value
                if spacing is cu.AUTO or cu.MAX, this value will determine where 
                extraneous space goes.
            
        
        
        '''
        
        
        # these can be overriden after instantiation
        self.height = height 
        self.spacing = spacing
        self.xAlign = xAlign
        
        self.grid = grid
        self.cells:Cell = []
        
        yOffset = 0  
        # the y coordinate of the top line of the Block.
        # this will be recalculated later
        
    def setHeight(self, height):
        self.height = height
        
    def addCell(self, height=cu.AUTO, width=cu.AUTO, align=cu.LEFT):
        c = Cell( self, height, width, align)
        self.cells.append( c )
        return c
    
    def measure(self):
        # calculates the maximum and minimum sizes of the individual cells,
        # then uses that to calculate the overall minimum and maximum
        # 
        # note that if height is cu.AUTO 
        
        pass
        
    def assemble(self):
        pass
        
class Cell( object ):
    '''
        A virtual container that contains lines of text.  
    
    
    
    
    '''
    
    def __init__(self, block:Block, height=cu.AUTO, width=cu.AUTO, yAlign=cu.TOP, xAlign=cu.CENTER, span=1, padding = None):
        '''
            block
                the parent Block object that manages this container
            height, width
                int, cu.AUTO, cu.MAX
            yAlign
                how the contents are aligned vertically within the cell
            xAlign
                how the contents as a whole (not individual lines) are aligned in the cell
            span
                similar to the rowspan propery in CSS.  
                this is really only useful when there are multiple cells, all being sized automatically.
            padding
                the number of extra spaces on the outer edges. 
                it is important to note that these are strictly enforces and content that 
                would otherwise exceed these boundaries will be truncated and/or omitted
        
        '''
        
        # these can be overriden after instantiation
        self.height = height
        self.width = width
        self.yAlign = yAlign
        self.xAlign = xAlign
        self.span = span
        
        
        self.block = block
        self.grid = block.grid
        self.row = []
        
        xOffset = 0 
        # the x coordinate of the left edge of the block
        # this will be recalculated later
        # compined with .block.yOffset, will be used to determine the actual position 
        # within the total grid
        
    def setPadding(self, padding ):
        
        if padding is None:
            self.padleft = 0
            self.padright = 0
            self.pad 
        
        
    
        
    