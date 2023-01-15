'''
Created on Jan 15, 2023

@author: Cather Steincamp
'''
import CursedUtils as cu
import json
import os 

CONFIGFILE = './footpedal.config'

HEIGHT=25
WIDTH=110
Y=1
X=5

class ConfigMenu(cu.Window):
    '''
    classdocs
    '''

    def __init__(self, parent:cu.Screen, title, key=None):
        cu.Window.__init__(self, parent, HEIGHT, WIDTH, Y, X)
        
        self.configFile=CONFIGFILE
        self.configKey=key
        self.fields = []
        self.maxField = 0
        self.maxLabel = 0
        self.title = title
        self.keys = cu.KeyResponder()
        self.loadConfig()
        
    
    def loadConfig(self):
        f = open( self.configFile, 'r' )
        self.config = json.load( f )
        f.close()
        self.changed = False
        
    def saveConfig(self):
        if self.changed:
            f = open( self.configFile, 'w' )
            json.dump(self.config, f)
            f.close()
        self.changed = False
        
    def addField(self, label, width, description='', validator=None):
        self.fields.append( [label, width, description, validator])
        if width > self.maxField:
            self.maxField = width
        if len( label ) > self.maxLabel:
            self.maxLabel = label
            
    def isFile(self, validate ):
        if os.path.isfile( validate ):
            return True
        else:
            return 'Invalid File Name'
    
    def isDir(self, validate):
        if os.path.isdir( validate ):
            return True 
        else:
            return 'Invalid Path Name'
    
    def layout(self):
        
        self.write( 1, int( ( self.sizeX - len( self.title ) ) / 2 ), self.title )
        
        leftpoint = int( ( self.sizeX - ( self.maxLabel + self.maxField + 5 ) ) / 2 )
        # The five is to account for the option key + 2 spaces each between columns
        
        labelanchor = leftpoint + 3 + self.maxLabel
        # The three is to account for the option key and the two spaces after it.
        # note that this is a RIGHT anchor 
        
        fieldanchor = labelanchor + 2 
        
        self.setSlot('detail', 3, 1, self.sizeX - 2, cu.CENTER)
        self.setSlot('error', 5, 1, self.sizeX - 2, cu.CENTER)
        
        y = 7
        
        i = 0
        
        while i < len( self.fields ):
            
            field = self.fields[i]
            
            self.write( y, labelanchor - len( field[0]), field[0])
            self.setSlot( y, fieldanchor, field[0], field[1] )
            # add keyresponder
            
            self.keys.setResponse( str(i+1), self.editField, args=[i] )
            i += 1
            y += 2
        
        self.fillSlots()
            
            
        
            


    def editField(self, index ):
        # we have been conveniently provided the index of the field in self.fields.
        
        field = self.fields[index]
        slot = self.slot[field[0]]
        
        if self.configKey is None:
            if field[0] not in self.config:
                self.config[field[0]] = ''
            
            prefill = self.config[field[0]]
        else:
            if self.configKey not in self.config:
                self.config[self.configKey] = {}
            if field[0] not in self.config[self.configKey]:
                self.config[self.configKey][field[0]] = ''
                
            prefill = self.config[self.configKey][field[0]]
            
        self.slotWrite(field[0], field[2], True )
        
        while True:
        
            r = self.lineInput( slot['y'], slot['x'],slot['w'], prefill )
            
            if field[3] is not None:
                
                validate = field[3](r)
                
                if validate == False:
                    self.slotWrite( 'error', validate, True )
                    prefill = r
                    continue
            
            # either there is no validation or we've passed it
            break
        
        if self.configKey is None:
            if self.config[field[0]] != r:
                self.config[field[0]] = r
                self.changed = True
        else:
            if self.config[self.configKey][field[0]] != r:
                self.config[self.configKey][field[0]] = r
                self.changed = True 
                
        self.slotBlank('error')
        self.slotBlank('detail')
        self.slotWrite(field[0], r, True ) 

        
        
        
        
        
        
        
    def fillSlots(self):
        
        if self.configKey is None:
            for field in self.config:
                if type( field ) == str:
                    self.slotWrite( field, self.config[field] )
                    
        elif self.configKey in self.config:
            for field in self.config[self.configKey]:
                self.slotWrite(field, self.config[self.configKey][field])
                
        else:
            # if we're being asked for it, we'll need it.
            self.config[self.configKey] = {}
                
            
        
        