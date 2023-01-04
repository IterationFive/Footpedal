'''
Created on Dec 24, 2022

@author: Cather Steincamp
'''

import CursedUtils as cu

class ColumnHandler(object):
    '''
    classdocs
    '''


    def __init__( self, window:cu.ScreenHandler, y, x, 
                 maxHeight=False, maxWidth=False, spacing=0, wordWrap=True,
                 yAlign=cu.TOP, iAlign=cu.LEFT, xAlign=cu.LEFT):
        '''
        creates a column of text based on a list of strings
        
        window
            This is the screen or window onto which the column will be written.
        contents
            A list of the strings that will be displayed in column form.
            If an item in the list is a list in and of itself, then each item in 
            that list will be on a separate line, but not separated by any
            spacing.
        y,x
            the starting point of the column.  
        maxHeight,maxWidth
            if False, will automatically be set to the maximum available space
            if AUTO will automatically be set to the minimum size dictated by contents and spacing
            These define the area in which the column is displayed and arranged,
            not the dimensions of the column itself, which will be placed in
            this area.
            
            
            
        spacing
            the number of lines separating each item.
            AUTO results in maximum possible spacing unless height is also AUTO
        wordWrap
            if True, then any item that is longer than the max available width
            will be split into lines based on spaces.  if a 'word' is longer than
            the maximum available width, it will be split.
            if False, then any item longer than the max available width will
            be truncated.
            
                      
            
        yAlign
            TOP/UP, MIDDLE/CENTER/CENTRE, DOWN/BOTTOM, AUTO
            How the column is aligned in the available vertical space
            if height is AUTO, this will have no effect
        iAlign
            LEFT, CENTER/CENTRE/MIDDLE, RIGHT
            how the complete text is aligned internally
        xAlign
            LEFT, CENTER/CENTRE/MIDDLE, RIGHT
            How the column itself is aligned in the available space.
            For example, if iAlign is LEFT and xAlign is CENTER,
            the column will appear in the middle of the available space,
            but the text in the column will be aligned to the left.
            
        Note:  To be linguistically flexible,
            
        '''
        self.settings = {'maxHeight':maxHeight, 'maxWidth':maxWidth, 'spacing':spacing, 'wordWrap': wordWrap,
                 'yAlign':yAlign, 'iAlign':iAlign, 'xAlign':xAlign }
        self.window = window
        self.y = y 
        self.x = x
        
        
    def processContents(self, contents):
        
        # convert any content to strings
        
        cu.stringifyList(contents)
        
        # determine maxWidth and actual width 
        
        longestLengthAvailable = self.window.sizeX - self.x
        longestLengthUsed = cu.getLongestLength(contents)
        
        if self.settings[ 'maxWidth' ] == False:
            maxWidth = longestLengthAvailable            
        elif self.settings[ 'maxWidth' ] == cu.AUTO:            
            if longestLengthUsed > longestLengthAvailable:
                maxWidth = longestLengthAvailable
            else:
                maxWidth = longestLengthUsed
        else:
            maxWidth = self.settings[ 'maxWidth' ]
                
        if longestLengthUsed > maxWidth:
            width = longestLengthAvailable
        else:
            width = longestLengthUsed
                
        # now apply wordwrap where needed        
                
        if self.settings['wordWrap'] == True:                
            contents = cu.wrappedList(contents, maxWidth)
        else:
            contents = cu.clippedList(contents, maxWidth)
            
        # get the contents compressed into two dimensions
        
        contents = cu.collapseSubLists(contents)
            
        # now let's figure out height and spacing
        
        usedlines = len( cu.collapseList( contents ))                
        spacesToFill = len( contents ) - 1
        
        if self.settings['maxHeight'] == False:
            maxHeight = self.window.sizeY - self.y
        elif self.settings['maxHeight'] != cu.AUTO:
            maxHeight = self.settings['maxHeight']
            
        if self.settings['spacing'] == cu.AUTO:
            
            if self.settings['maxHeight'] == cu.AUTO:
                spacing = 0
            else:
                available = maxHeight - usedlines
                
                if spacesToFill > available:
                    spacing = 0
                else:
                    spacing = int( available / spacesToFill )
        else:
            spacing = self.settings['spacing']
                    
        height = usedlines + ( spacing * spacesToFill )
        
        if self.settings['maxHeight'] == cu.AUTO:
            maxHeight = height
            
        '''
        
        we have worked out:
        
            maxHeight, maxWidth
                the total area to work in
            height,  width
                the area of the column itself
            spacing
        
        '''
            
        if height > maxHeight:
            yOffset = 0            
        elif self.settings['yAlign'] == cu.MIDDLE:            
            yOffset =  int( ( maxHeight - height ) / 2 )            
        elif self.settings['yAlign'] == cu.BOTTOM:            
            yOffset = maxHeight - height            
        else:
            # TOP or you screwed up            
            yOffset = 0
                
        if maxWidth > width:            
            if self.settings['xAlign'] == cu.CENTER:
                xOffset = int( ( maxWidth - width ) / 2 ) 
            elif self.settings['xAlign'] == cu.RIGHT:
                xOffset = maxWidth - width
            else:
                # LEFT or you screwed up
                xOffset = 0
            
        else:
            xOffset = 0
            
        yOffset += self.y
        xOffset += self.x
        
        #now we know where we're going to put the column.
        
        # and heeeeeeeere we go 
        
        activeY = yOffset
        
        for item in contents:
            if type( item ) == str:
                item = [item]
            
            for line in item:
            
                if self.settings['iAlign'] == cu.CENTER:
                    lineOffset = int( ( width - len( line ) ) / 2 )
    
                elif self.settings['iAlign'] == cu.RIGHT:
                    lineOffset = width - len( line )
                else:
                    # LEFT or you screwed up 
                    lineOffset = 0              
                    
                self.window.write( activeY, xOffset + lineOffset, line )
                activeY += 1
                
                if activeY ==  height + yOffset:
                    # we are outside the available area
                    break
                
            activeY += spacing
                
            if activeY == height + yOffset:
                # we are outside the available area
                break
            
        self.window.refresh()      
        