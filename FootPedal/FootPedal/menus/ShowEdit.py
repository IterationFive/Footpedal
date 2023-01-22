'''
Created on Jan 20, 2023

@author: Cather Steincamp
'''

import CursedUtils as cu 
from FootPedal import SHOWCONFIG
from lib.ShowLookup import TVShow

class ShowEdit(cu.ConfigMenu):
    '''
    classdocs
    '''
    
    def __init__(self, parent:cu.Screen, show):
        self.show = show
        cu.ConfigMenu.__init__(self, parent, configFile=SHOWCONFIG)
    
    def setup(self):
        
        if self.show is None:
            go = self.createProfile()
        else:
            go = True
        
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
            
            # add key responses for R and D
            
            self.runMenu()
            
            
        
    def createProfile(self):
        
        y = int( self.sizeY / 2 ) - 2        
        midpoint = int( self.sizeX / 2 )
        
        self.setSlot( 'blurb1', y - 3, midpoint-30, 60, cu.CENTER )
        self.setSlot( 'blurb2', y - 2, midpoint-30, 60, cu.CENTER )
        
        self.setSlot( 'input', y, midpoint -25, 50  )
        
        self.setSlot( 'response1', y + 2, midpoint - 25, 50, cu.CENTER )
        self.setSlot( 'response2', y + 3, midpoint - 25, 50, cu.CENTER )
        
        if self.config['API Key'] != '' and self.config['PIN'] != '' :
            self.createTVDBprofile()
        else:
            # no lookup involved
            pass
        # cleanup display and drop back to setup(), which will launch runMenu() 
        
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
                        self.config[show.name] = { 'tvdb': int(r),'rgx':show.name, 'Outbox':'', 'Backup':'', 
                                                  'Preset':'', 'GUI Preset':'', 'JSON Config':'', 'Subtitle Language':'' }
                    else:
                        continue
            else:
                # manual setup
                if self.confirmShowTitle(r):
                        self.config[r] = { 'rgx':r, 'Outbox':'', 'Backup':'', 'Preset':'', 'GUI Preset':'', 'JSON Config':'', 'Subtitle Language':'' }
                else:
                    continue

        self.saveConfig()
        return False
    
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
            
        self.slotBlank('response1')
        self.slotBlank('response2', True )
        
        return x
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        '''
        prompt = 'Enter the show\'s name (as you want it in the filename)'
        self.write( y, midpoint - int( prompt/2 ), prompt )
        y += 1
        
        if len( self.config['API Key'] ) > 30:
            prompt = 'or the TVDB id number'
            self.write( y, midpoint - int( prompt/2 ), prompt )
            y += 1
            
        y+1
        
        self.setSlot( 'response1', y + 3, midpoint - 20, 40  )
        self.setSlot( 'response2', y + 4, midpoint - 20, 40  )
        self.setSlot( 'response2', y + 4, midpoint - 20, 40  )
        
        prefill = ''
            
        while True:
            r:str = self.lineInput(y, midpoint -10, 20, prefill )
            
            if r.isdigit() and len( self.config['API Key'] ) > 30:
                
                show = TVShow( int(r), self.config['API Key'], self.config['PIN'] )'''
                
                