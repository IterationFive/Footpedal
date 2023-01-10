'''
Created on Jan 5, 2023

@author: Cather Steincamp
'''
import CursedUtils as cu
import os 
class FolderMenu(cu.Window):
    '''
    classdocs
    '''
    def setup(self):
        
        self.menuData = {}
        self.descriptions = {        
            'inbox':'This application will check this folder for new files and subtitles.',
            'staging':'Optional.  If set, files will be moved here pending processing.',
            'outbox':'The default location for converted files.',
            'trash':'Optional.  If set, original files will be moved here after conversion.',
            'temp':'This folder is used for processing.',
            'backup':'Optional.  If set, a second copy of the converted file will be placed here.',
            'log':'This application will check this folder for new files and subtitles.' }
        
        self.setSlot( 'title', 1, 50, 20, cu.CENTER )
        
        self.slotWrite( 'title', 'Folder Settings' )
        
        self.write(  8, 15, 'Inbox:' )        
        self.write( 10, 15, 'Staging:' )        
        self.write( 12, 15, 'Outbox:' )        
        self.write( 14, 15, 'Trash:' )        
        self.write( 16, 15, 'Temp:' )        
        self.write( 18, 15, 'Backup:' )        
        self.write( 20, 15, 'Log:', True )
        
        
        self.setSlot( 'inbox',    8, 32, 80, cu.LEFT)
        self.setSlot( 'staging', 10, 32, 80, cu.LEFT)
        self.setSlot( 'outbox',  12, 32, 80, cu.LEFT)
        self.setSlot( 'trash',   14, 32, 80, cu.LEFT)
        self.setSlot( 'temp',    16, 32, 80, cu.LEFT)
        self.setSlot( 'backup',  18, 32, 80, cu.LEFT)
        self.setSlot( 'log',     20, 32, 80, cu.LEFT)
        
        self.setSlot( 'error', 23, 30, 60, cu.CENTER)
        self.setSlot( 'blurb1', 3, 30, 60, cu.CENTER)
        self.setSlot( 'blurb2', 4, 30, 60, cu.CENTER)
        self.setSlot( 'detail', 6, 10, 90, cu.CENTER)
        
        self.keys = cu.KeyResponder()
        
        self.keys.setResponse( '1', self.editField, args=['inbox'] )
        self.keys.setResponse( '2', self.editField, args=['staging'] )
        self.keys.setResponse( '3', self.editField, args=['outbox'] )
        self.keys.setResponse( '4', self.editField, args=['trash'] )
        self.keys.setResponse( '5', self.editField, args=['temp'] )
        self.keys.setResponse( '6', self.editField, args=['backup'] )
        self.keys.setResponse( '7', self.editField, args=['log'] )
        self.keys.setResponse( 'escape', self.saveAndExit )
        
        self.refresh()
        
    def editField(self, field ):
        
        
        if field in self.slot:
            self.slotBlank( 'error', True)
            self.slotWrite( 'detail', self.descriptions[field], True )
            while True:
                r = self.slotInput( field )
                
                if field in ['inbox','outbox','temp','log']:
                    if os.path.exists( r ):
                        self.menuData[field ]= r
                        self.slotBlank( 'error', True)
                        self.slotBlank( 'detail', True)
                        break
                else:
                    if r=='' or os.path.exists( r ):
                        self.menuData[field ]= r
                        self.slotBlank( 'error', True)
                        self.slotBlank( 'detail', True)
                        break 
                
                self.slotWrite( 'error', "Invalid Path.", True )
                
    
    def firstRun(self):
        
        for field in ['inbox','staging','outbox','trash','temp','backup','log' ]:
            self.editField(field)
            
        self.adjust()
    
    def adjust(self):
        
        for field in self.menuData:
            self.slotWrite( field, self.menuData[field] )
        
        self.slotWrite('blurb1', 'Select a number to change a folder or')
        self.slotWrite('blurb2', 'press [Esc] to save and exit.')
        
        self.write(  8, 10, '[1]' )        
        self.write( 10, 10, '[2]' )        
        self.write( 12, 10, '[3]' )        
        self.write( 14, 10, '[4]' )        
        self.write( 16, 10, '[5]' )        
        self.write( 18, 10, '[6]' )        
        self.write( 20, 10, '[7]', True )
        
        self.keys.keyLoop(self.window)
        
        
        
    def saveAndExit(self):
        pass
    
    
        
        
                
        
        
        
#
#
#         INBOX = 'F:/HandCrank/inbox/'
# STAGE = 'F:/HandCrank/pending/'
# OUTPUT = 'F:/HandCrank/complete/'
# TRASH = "F:/HandCrank/trash/"
# TMP = 'F:/HandCrank/tmp/'
# BACKUP = "I:/"
# LOG = 'F:/HandCrank/'