'''
Created on Jan 16, 2023

@author: Cather Steincamp
'''

import CursedUtils as cu

class HandbrakeConfig(cu.ConfigMenu):
    '''
    classdocs
    '''


    def setup(self):
        self.title = 'HandBrake Preferences'
        self.configKey='handbrake'
        self.addField('Handbrake CLI', 75, 'The location of the HandBrakeCLI executable', self.isFile )
        self.addField('Preset', 40, '(Optional) One of the built-in HandPresets' )
        self.addField('GUI Preset', 40, '(Optional) A Preset Created and named using the GUI' )
        self.addField('JSON Config', 75, '(Optional) A JSON file containing Handbrake configuration', self.isFileOrNone )
        self.addField('Subtitle Language', 40, 'The default language code for subtitle files' )
        
    def isFileOrNone(self, validate):
        
        if validate == '': 
            return True
        else:
            return self.isFile( validate )