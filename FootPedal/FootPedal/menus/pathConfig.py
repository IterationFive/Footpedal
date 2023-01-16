'''
Created on Jan 15, 2023

@author: Cather Steincamp
'''

import CursedUtils as cu

class pathConfig(cu.ConfigMenu):
    '''
    classdocs
    '''
    
    def setup(self):
        self.addField('Inbox', 75, 'This application will check this folder for new files and subtitles.', self.isDir )
        self.addField('Staging', 75, 'Optional.  If set, files will be moved here pending processing.', self.isDir )
        self.addField('Outbox', 75, 'The default location for converted files.', self.isDir )
        self.addField('Trash', 75, 'Optional.  If set, original files will be moved here after conversion.', self.isDir )
        self.addField('Temp', 75, 'This folder is used for processing.', self.isDir )
        self.addField('Backup', 75, 'Optional.  If set, a second copy of the converted file will be placed here.', self.isDir )
        self.addField('Log', 75, 'Logfiles will be stored here.', self.isDir )