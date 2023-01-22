'''
Created on Jan 19, 2023

@author: Cather Steincamp
'''

from FootPedal import SHOWCONFIG
import os, json
import FootPedal.menus as menu
import CursedUtils as cu

class ShowMenu(cu.Window):
    '''
    classdocs
    '''
    def __init__(self, parent:cu.Screen):
        self.configFile = SHOWCONFIG
        self.loadConfig()
        self.keys = cu.KeyResponder()
        cu.Window.__init__(self, parent)
    
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
        f = open( self.configFile, 'w' )
        json.dump(self.config, f, indent=1)
        f.close()
        
    def setup(self):
        
        midpoint = int( self.sizeX / 2 )
        
        self.setSlot('title',1, midpoint - 20, 40, cu.CENTER )
        self.slotWrite( 'title', 'Shows Menu' )
        
        self.setSlot('tvdblabel',3, midpoint - 20, 40, cu.CENTER )
        self.slotWrite( 'tvdblabel', 'TVDB API Information' )
        
        xAnchor = midpoint - 24        
        self.write( 4, xAnchor, 'API Key: ')
        self.setSlot( 'API Key', 4, xAnchor + 9, 38 )
        
        self.write( 5, xAnchor, 'PIN: ')
        self.setSlot( 'PIN', 5, xAnchor + 8, 10 )
        
        for field in ['API Key','PIN']:
            if field not in self.config:
                self.config[field] = ''
            self.slotWrite(field, self.config[field])
                
        # show list template
        self.write( 7, midpoint - 9, 'Configured Shows' )
        
        self.setSlot( 'pagecount', 8, midpoint + 11, 12, cu.RIGHT )
        
        for i in range( 0, 10 ):
            if i == 9:
                key = "0"
            else:
                key = str( i+1 )                
        
                self.setSlot( 'key' + key, i + 9, midpoint - 22, 1 )
                self.setSlot( 'name' + key, i + 9, midpoint - 20, 42 )
                
        self.setSlot( 'navUp', 19, midpoint - 21, 20 )
        self.setSlot( 'navDown', 19, midpoint + 1, 20, cu.RIGHT )
                
        self.setSlot( 'blurb1', 21, midpoint - 25, 50, cu.CENTER )  
        self.setSlot( 'blurb2', 22, midpoint - 25, 50, cu.CENTER )  
        self.setSlot( 'blurb3', 23, midpoint - 25, 50, cu.CENTER )  
        self.setSlot( 'blurb4', 24, midpoint - 25, 50, cu.CENTER )
           
        self.slotWrite( 'blurb2', 'Press A to add a show')        
        self.slotWrite( 'blurb3', 'Press C to change TVDB Configuration' )
        self.slotWrite( 'blurb4', 'Press Escape to Exit' )
        
        self.listStart = 0
        
        self.setupListMenu()
        self.keys.keyLoop(self)
    
    
    def setupListMenu(self):
        
        self.keys.clearAll()
        self.loadConfig()
        # this gets rebuilt every time.
        
        shows = []
        for show in self.config:
            if type( self.config[show] ) == dict:
                shows.append( show )
            
        # this also gets rebuilt every time.  
            
        totalShows = len( shows )
            
        if totalShows > 0:
            #great!  we have work to do
            
            pageEnd = self.listStart + 9
            
            if pageEnd >= totalShows:
                pageEnd = totalShows - 1
                
            if totalShows > 10:
                self.slotWrite( 'pagecount', str( self.listStart + 1 ) + '-' + str( pageEnd + 1 ) + ' of ' + str( totalShows ))
                
            if self.listStart > 1:
                self.slotWrite( 'navUp', 'Up/PageUp')
                self.keys.setResponse( 'pageup', self.listPageUp )
                self.keys.setResponse( 'up', self.listUp )
                
            if pageEnd < ( totalShows - 1 ):
                self.SlotWrite( 'navDown', 'Down/PageDown')
                self.keys.setResponse( 'pagedown', self.listPageDown )
                self.keys.setResponse( 'down', self.listDown )                
            
            i = 0
            
            while i < 10 :
                if i == 9:
                    key = "0"
                else:
                    key = str( i+1 )  
                    
                showname = shows[ self.listStart + i ]
                
                self.slotWrite( 'key' + key, key )
                self.slotWrite( 'name' + key, showname )
                
                self.keys.setResponse( key, self.editShow, args=[showname] )
                
                i += 1
                
                if self.listStart + i > pageEnd:
                    break
                
                    
            
        # setup other menu keys
        self.keys.setResponse( 'A', self.addShow )
        self.keys.setResponse( 'C', self.tvdbConfig )
        
        
        
    def editShow(self, showname):
        x =  menu.ShowEdit( self, showname )
        x.close()
        self.setupListMenu()
    
    def addShow(self):
        x = menu.ShowEdit( self )
        x.close()
        self.setupListMenu()
        
    def listUp(self):
        showcount = len( self.config['shows'] )
        self.listStart += 1
        
        if self.listStart > showcount - 10:
            self.listStart = showcount - 10
            
        self.setupListMenu()
    
    def listDown(self):
        self.listStart -= 1
        
        if self.listStart < 0:
            self.listStart = 0
            
        self.setupListMenu()
    
    def listPageUp(self):
        showcount = len( self.config['shows'] )
        self.listStart += 10
        
        if self.listStart > showcount - 10:
            self.listStart = showcount - 10
            
        self.setupListMenu()
    
    def listPageDown(self):
        self.listStart -= 10
        
        if self.listStart < 0:
            self.listStart = 0
            
        self.setupListMenu()
        
    def tvdbConfig(self):
                
        for field in ['API Key','PIN']:
            self.config[field] = self.slotInput(field)

        self.saveConfig()
        
        