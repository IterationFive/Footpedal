'''
Created on Jan 20, 2023

@author: Cather Steincamp
'''

import CursedUtils as cu 
from FootPedal import SHOWCONFIG
from lib.ShowLookup import TVShow

class ShowEdit(cu.ConfigMenu):
    '''
    Gives the ability to create and/or edit a television show profile.
    
    The constuctor requires a cu.Screen or cu.Window object, and
    optionally the name of the show.  If the name of the show is not
    provided, the user will be prompted to set up the profile
    for the first time, either manually or with a TVDB id.
    
    
    '''
    
    def __init__(self, parent:cu.Screen, show=None):
        self.show = show
        cu.ConfigMenu.__init__(self, parent, configFile=SHOWCONFIG)
    
    def setup(self):
        
        if self.show is None:
            go = self.createProfile()
        else:
            go = True
            
        # if go is False, that means that the user started to setup a profile
        # then changed their mind.  So, we don't have to go to all 
        # the trouble below.
        
        if go:    
            self.configKey=self.show
            self.title = self.show
            
            self.addField('rgx', 75, 'A regular expression to match the title in scanned filenames.' )
            self.addField('Outbox', 75, 'Optional.  Overrides default HandBrake setting.', self.isDirOrNone )
            self.addField('Backup', 75, 'Optional.  Overrides default HandBrake setting.', self.isDirOrNone )
            self.addField('Preset', 40, 'Optional.  Overrides default HandBrake setting.' )
            self.addField('GUI Preset', 40, 'Optional.  Overrides default HandBrake setting.' )
            self.addField('JSON Config', 75, 'Optional.  Overrides default HandBrake setting.', self.isFileOrNone )
            self.addField('Subtitle Language', 40, 'Optional.  Overrides default HandBrake setting.' )
            self.addText('')
            self.addText('Press R to Rename Show     Press D to Delete Show' )
            
            self.keys.setResponse('r', self.renameShow )
            self.keys.setResponse('d', self.deleteShow )
            
            self.runMenu()
            
    def renameShow(self):
        
        r = self.slotInput( 'menutitle' )
        
        self.config[r] = self.config[self.configKey]
        del self.config[self.configKey]
        self.configKey = r
        self.title = r 
        
        self.saveConfig(True)
    
    def deleteShow(self):
        del self.config[self.configKey]
        self.saveAndExit(True)
        
    def createProfile(self):
        
        y = int( self.sizeY / 2 ) - 2        
        midpoint = int( self.sizeX / 2 )
        
        self.setSlot( 'blurb1', y - 3, midpoint-30, 60, cu.CENTER )
        self.setSlot( 'blurb2', y - 2, midpoint-30, 60, cu.CENTER )
        
        self.setSlot( 'input', y, midpoint -25, 50  )
        
        self.setSlot( 'response1', y + 2, midpoint - 25, 50, cu.CENTER )
        self.setSlot( 'response2', y + 3, midpoint - 25, 50, cu.CENTER )
        
        if self.config['API Key'] != '' and self.config['PIN'] != '' :
            r = self.createTVDBprofile()
        else:
            r = self.createManualProfile()
    
        self.window.clear()
        self.slot = {}
        return r
         
        
    def createManualProfile(self):
        
        self.slotWrite('blurb2', 'Enter the show name as you want it to appear in file names.', True )
        
        while True:
            
            r:str = self.slotInput('input')
            self.slotBlank('response1')
            self.slotBlank('response2')
            
            if r=='':
                return False
            
            if self.confirmShowTitle(r):
                self.show = r
                self.config[r] = { 'rgx':r, 'Outbox':'', 'Backup':'', 'Preset':'', 'GUI Preset':'', 'JSON Config':'', 'Subtitle Language':'' }
                self.saveConfig(True)
                return True
        
    def createTVDBprofile(self):
        
        self.slotWrite('blurb1', 'Enter a TVDB ID Number for automatic episode naming or' )
        self.slotWrite('blurb2', 'the show name as you want it to appear in file names.', True )
        
        while True:
            
            r:str = self.slotInput('input')
            self.slotBlank('response1')
            self.slotBlank('response2')
            
            if r=='':
                return False
            
            if r.isdigit():
                # run TVDB profile check
                show = TVShow( int(r), self.config['API Key'], self.config['PIN'] )
                
                if show.name == False:
                    self.slotWrite( 'response1', 'Invalid Id number.')
                    continue
                else:
                    if self.confirmShowTitle(show.name):
                        self.show = show.name
                        self.config[show.name] = { 'tvdb': int(r),'rgx':show.name, 'Outbox':'', 'Backup':'', 
                                                  'Preset':'', 'GUI Preset':'', 'JSON Config':'', 'Subtitle Language':'' }
                        self.saveConfig(True)
                        return True
                    else:
                        continue
            else:
                # manual setup
                if self.confirmShowTitle(r):
                    self.show = r
                    self.config[r] = { 'rgx':r, 'Outbox':'', 'Backup':'', 'Preset':'', 'GUI Preset':'', 'JSON Config':'', 'Subtitle Language':'' }
                    self.saveConfig(True)
                    return True
                else:
                    continue
    
    def confirmShowTitle(self, title ):
        
        self.slotWrite( 'response1', 'Title is: ' + title )
        self.slotWrite( 'response2', 'Is this correct? (y/n)', True )
        
        while True:
            self.window.nodelay( False )
            x = self.getch()
            
            if x == ord('y') or x == ord('Y'):
                x = True
            elif x == ord('n') or x == ord('N'):
                x = False
            else:
                continue
            
            break
            
        self.slotBlank('response1')
        self.slotBlank('response2', True )
        
        return x
    
        
        
                