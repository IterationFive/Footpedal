'''
Created on Jan 19, 2023

@author: Cather Steincamp
'''

from FootPedal import SHOWCONFIG
import os, json

import CursedUtils as cu

class ShowMenu(cu.Window):
    '''
    classdocs
    '''
    def __init__(self, parent:cu.Screen):
        self.configFile = SHOWCONFIG
        self.loadConfig()
        cu.Window.__init__(self, parent, 25, 110, 1, 5)
    
    def loadConfig(self):
        if os.path.isfile( self.configFile):
            f = open( self.configFile, 'r' )
            self.config = json.load( f )
            f.close()
        else:
            #create an empty file
            self.config = {}
            self.saveConfig()
        
    def saveConfig(self):
        if self.changed:
            f = open( self.configFile, 'w' )
            json.dump(self.config, f, indent=1)
            f.close()
        
    def setup(self):
        
        midpoint = int( self.window.sizeX / 2 )
        
        self.window.setSlot('title',1, midpoint - 20, 40, cu.CENTER )
        self.window.slotWrite( 'title', 'Shows Menu' )
        
        self.window.setSlot('tvdblabel',3, midpoint - 20, 40, cu.CENTER )
        self.window.slotWrite( 'tvdblabel', 'TVDB API Information' )
        
        xAnchor = midpoint - 28
        
        self.write( 5, xAnchor, 'API Key: ')
        
        xAnchor += 13
        
        self.window.setSlot( 'API Key', 5, xAnchor, 36 )
        
        xAnchor += 38
        self.window.write( 5, xAnchor, 'PIN: ')
        self.window.setSlot( 'PIN', 5, xAnchor + 8, 8 )
        
        for field in ['API Key','PIN']:
            if field in self.config:
                self.window.slotWrite(field, self.config[field])
            else:
                self.config[field] = ''
                
        # show list template
        self.window.write( 7, midpoint - 9, 'Configured Shows' )
        
        self.window.setSlot( 'pagecount', 8, midpoint, 22, cu.RIGHT )
        
        for i in range( 0, 10 ):
            if i == 9:
                key = "0"
            else:
                key = str( i+1 )                
        
                self.window.setSlot( 'key' + key, i + 9, midpoint - 22 )
                self.window.setSlot( 'name' + key, i + 9, midpoint - 20 )
                
        self.setSlot( 'navUp', 19, midpoint - 21, 20 )
        self.setSlot( 'navDown', 19, midpoint + 1, 20, cu.RIGHT )
                
        self.setSlot( 'blurb1', 21, midpoint - 25, 50, cu.CENTER )  
        self.setSlot( 'blurb2', 22, midpoint - 25, 50, cu.CENTER )  
        self.setSlot( 'blurb3', 23, midpoint - 25, 50, cu.CENTER )        
                
        self.slotWrite( 'blurb2', 'Press C to change TVDB Configuration' )
        self.slotWrite( 'blurb3', 'Press Escape to Exit' )
                
        
                
        
        
        
        
        
        